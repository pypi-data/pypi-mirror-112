import csv
import json
import sys
import time
import tempfile
import singer
from singer import metrics
from tap_salesforce.salesforce.exceptions import (TapSalesforceException)

JOB_STATUS_POLLING_SLEEP = 20
ITER_CHUNK_SIZE = 1024

LOGGER = singer.get_logger()


class BulkV2:

    BULK_V2_API_VERSION = '51.0'
    BULK_V2_URL = "{}/services/data/v{}/{}"


    def __init__(self, sf):
        csv.field_size_limit(sys.maxsize)
        self.sf = sf


    def query(self, catalog_entry, state):
        job_id = self._create_job(catalog_entry, state)
        for result in self._get_job_results(job_id):
            yield result
        self.sf.jobs_completed += 1


    def _get_job_results(self, job_id):
        job_status = self._poll_on_job_status(job_id)
        if job_status['state'] in ('Failed', 'Aborted'):
            raise TapSalesforceException(job_status)
        else:
            url = self.BULK_V2_URL.format(self.sf.instance_url, self.BULK_V2_API_VERSION, "jobs/query/{}/results".format(job_id))
            headers = self.sf.auth.rest_headers
            resp = self.sf._make_request('GET', url, headers=headers, stream=True)
            resp_headers = resp.headers
            for rec in self._yield_records(resp):
                yield rec
            while resp_headers['Sforce-Locator'] != 'null':
                url = self.BULK_V2_URL.format(
                    self.sf.instance_url, self.BULK_V2_API_VERSION, "jobs/query/{}/results?locator={}".format(job_id, resp_headers['Sforce-Locator'])
                )
                resp = self.sf._make_request('GET', url, headers=headers, stream=True)
                resp_headers = resp.headers
                for rec in self._yield_records(resp):
                    yield rec


    def _yield_records(self, resp):
        with tempfile.NamedTemporaryFile(mode="w+", encoding="utf8") as csv_file:
            for chunk in resp.iter_content(chunk_size=ITER_CHUNK_SIZE, decode_unicode=True):
                if chunk:
                    # Replace any NULL bytes in the chunk so it can be safely given to the CSV reader
                    csv_file.write(chunk.replace('\0', ''))

            csv_file.seek(0)
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
            column_name_list = next(csv_reader)
            for line in csv_reader:
                rec = dict(zip(column_name_list, line))
                yield rec

    def _poll_on_job_status(self, job_id):
        job_status = self._get_job_status(job_id=job_id)
        while job_status['state'] not in ['JobComplete', 'Failed', 'Aborted']:
            time.sleep(JOB_STATUS_POLLING_SLEEP)
            job_status = self._get_job_status(job_id=job_id)
        return job_status


    def _get_job_status(self, job_id):
        url = self.BULK_V2_URL.format(self.sf.instance_url, self.BULK_V2_API_VERSION, "jobs/query/{}".format(job_id))
        headers = self.sf.auth.rest_headers
        resp = self.sf._make_request('GET', url, headers=headers)
        resp_json = resp.json()
        return resp_json


    def _create_job(self, catalog_entry, state):
        url = self.BULK_V2_URL.format(self.sf.instance_url, self.BULK_V2_API_VERSION, "jobs/query")
        start_date = self.sf.get_start_date(state, catalog_entry)
        query = self.sf._build_query_string(catalog_entry, start_date)
        body = {"operation": "queryAll", "query": query, "contentType": "CSV"}
        headers = self.sf.auth.rest_headers
        headers["Content-Type"] = "application/json"

        with metrics.http_request_timer("create_job") as timer:
            timer.tags['sobject'] = catalog_entry['stream']
            resp = self.sf._make_request('POST', url, headers=headers, body=json.dumps(body))
        job = resp.json()
        return job['id']
