# coding:utf8

import argparse
import sys

from wpt_helper import WPTHelper


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
        '-r', '--result', type=str,
        help='Result file path where the result files will be stored.'
    )

    parameters = parser.parse_args()

    helper = WPTHelper()
    sucess = helper.get_resource_details(parameters.webpagetest,
                                         parameters.key,
                                         parameters.target,
                                         parameters.result)
    return 0 if sucess else -1

if __name__ == '__main__':
    sys.exit(main())
