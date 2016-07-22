This project is a helper to start a webpagetest task through WebpageTest
RESTful API. Download and save test result into given file path.

```
usage: main.py [-h] [-w WEBPAGETEST] [-t TARGET] [-k KEY] [-r RESULT]

WebPagetest helper to run test on WebPagetest instance.

optional arguments:
  -h, --help            show this help message and exit
  -w WEBPAGETEST, --webpagetest WEBPAGETEST
                        runtest url which offered by WebPagetest instance.
  -t TARGET, --target TARGET
                        target url which will be tested.
  -k KEY, --key KEY     WebPagetest api key.
  -r RESULT, --result RESULT
                        Result file path where the result files will be stored.
```
