import hashlib
import io
import json
import logging
import os
import time
from urllib import quote
from url_fetcher import URLFetcher


class WPTHelper(object):

    def __init__(self):
        pass

    def get_resource_details(self,
                             wpt_base_url,
                             api_key,
                             test_target,
                             result_file_path):
        json_data_url = self._start_test_task(wpt_base_url,
                                              api_key,
                                              test_target)
        if len(json_data_url) <= 0:
            print "Start test task error."
            return False

        sucess = self._get_test_result(test_target,
                                       json_data_url,
                                       result_file_path)

        return sucess

    def _start_test_task(self, wpt_base_url, api_key, test_target):
        test_url = wpt_base_url
        test_url += "?url=" + quote(test_target)
        test_url += "&runs=1&fvonly=1&requests=1&f=json"
        test_url += "&k=" + api_key
        print test_url
        url_fetcher = URLFetcher(test_url)
        json_data_url = ""
        if url_fetcher.fetch(1):
            url, page_source = url_fetcher.get_data()
            response = json.loads(page_source)
            if response["statusCode"] == 200:
                json_data_url = response["data"]["jsonUrl"]
                print "josn_data_url : %s" % json_data_url
        return json_data_url

    def _get_test_result(self, test_target, json_data_url, result_file_path):
        retry_count = 0
        while retry_count <= 20:
            json_data_fetcher = URLFetcher(json_data_url)
            if json_data_fetcher.fetch(1):
                retry_count += 1
                url, json_data = json_data_fetcher.get_data()
                response = json.loads(json_data)
                formatted_json_data = unicode(json.dumps(response, indent=4))
                if response['statusCode'] == 200:
                    self._save_test_result(test_target,
                                           formatted_json_data,
                                           result_file_path)
                    print "Get test result of %s successfully!" % test_target
                    return True
                else:
                    print "statusCode: %s, statusText: %s"\
                        % (response['statusCode'], response['statusText'])
                    time.sleep(5 * 60)
        return False

    def _save_test_result(self, test_target, result, result_file_path):
        with io.open(result_file_path, "w") as file_handle:
            file_handle.write(result)
