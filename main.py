# coding:utf8

import argparse
import hashlib
import io
import json
import logging
import os
import sys
import threading
import time
from urllib import quote
from url_fetcher import URLFetcher


def start_test_task(wpt_base_url, api_key, test_target):
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


def get_test_result(test_target, json_data_url, result_file_path):
    retry_count = 0
    while retry_count <= 20:
        json_data_fetcher = URLFetcher(json_data_url)
        if json_data_fetcher.fetch(1):
            retry_count += 1
            url, json_data = json_data_fetcher.get_data()
            response = json.loads(json_data)
            if response['statusCode'] == 200:
                save_test_result(test_target, json_data, result_file_path)
                print "Get test result of %s successfully!" % test_target
                return True
            else:
                print "statusCode: %s, statusText: %s"\
                    % (response['statusCode'], response['statusText'])
                time.sleep(5 * 60)
    return False


def save_test_result(test_target, result, result_file_path):
    hashed_file_name =\
        hashlib.new("md5", test_target).hexdigest() + ".json"
    result_file_path = os.path.join(result_file_path, hashed_file_name)
    with io.open(result_file_path, "w") as file_handle:
        file_handle.write(result)


def main():
    parser = argparse.ArgumentParser(
        description='WebPagetest helper to run test on WebPagetest instance.')
    parser.add_argument(
        '-w', '--webpagetest', type=str,
        default='http://www.webpagetest.org/runtest.php',
        help='runtest url which offered by WebPagetest instance.'
    )

    parser.add_argument(
        '-t', '--target', type=str,
        help='target url which will be tested.'
    )

    parser.add_argument(
        '-k', '--key', type=str,
        help='WebPagetest api key.'
    )

    parser.add_argument(
        '-o', '--output', type=str,
        help='Output directory where the result files will be stored'
    )

    parameters = parser.parse_args()

    json_data_url = start_test_task(parameters.webpagetest,
                                    parameters.key,
                                    parameters.target)
    if len(json_data_url) <= 0:
        print "Start test task error."
        return -1

    sucess = get_test_result(parameters.target,
                             json_data_url,
                             parameters.output)
    return sucess

if __name__ == '__main__':
    sys.exit(main())
