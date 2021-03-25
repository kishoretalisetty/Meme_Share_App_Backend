
import unittest
from unittest import TestCase

import curlify
import requests
import json
import logging
import time
import socket

## Global variables and functions
from pytest import fail

scores = {}
logs_directory = '/home/ubuntu/'

def check_server(address, port):
    # Create a TCP socket
    s = socket.socket()
    print("Attempting to connect to {} on port {}".format(address, port))
    try:
        s.connect((address, port))
        print( "Connected to %s on port %s" % (address, port))
        return True
    except socket.error:
        print ("Connection to %s on port %s failed" % (address, port))
        return False
    finally:
        s.close()

class ScoreGenerate(TestCase):

    HEADERS = None

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.HEADERS = {"Content-Type": "application/json"} # "X-Firebase-Auth": "INTERNAL_IMPERSONATE_USER_" + str(user),
        self.localhost = 'http://localhost:8081/'
        self.score = 0
        self.list = {
            'timestamp': time.time(),
            'swagger': 0,
            'get-on-empty-db': 0,
            'first-post': 0,
            'get-single-meme': 0,
            'update-meme-url': 0,
            'post-lt-100-memes': 0,
            'get-single-non-existent-meme': 0,
            'post-duplicate': 0,
            'post-empty-body': 0,
            'post-incomplete-meme': 0,
            'patch-update-name': 0,
            'patch-update-both': 0,
            'patch-non-existent': 0,
            'scoretotal': 0,
            'test-results': '',
            'status': False
        }

        self.SAMPLE_URL = 'https://cwod-assessment-images.s3.ap-south-1.amazonaws.com/images/'
        self.FIRST_POST_ID = ''
        self.FIRST_POST = '130.png'

        self.SECOND_POST_ID = ''
        self.SECOND_POST = '132.png'
        self.UPDATED_POST = '133.png'

        self.POSITIVE_STATUS_CODES = [200, 201, 202, 203]
        self.NEGATIVE_STATUS_CODES = [400, 401, 402, 403, 404, 405, 409]

    ### Helper functions
    def get_api(self, endpoint):
        print('Making a GET request to ' + endpoint)
        response = requests.get(self.localhost + endpoint, headers=self.HEADERS)
        self.print_curl_request_and_response(response)
        return response

    def post_api(self, endpoint, body):
        print('Making a POST request to ' + endpoint + ' with body ')
        print(body)
        response = requests.post(self.localhost + endpoint, headers=self.HEADERS, data=body)
        self.print_curl_request_and_response(response)
        return response

    def print_curl_request_and_response(self, response):
        print("Making curl request - ")
        print(curlify.to_curl(response.request))
        print('Received response with status code:' + str(response.status_code))
        if(response.status_code in self.POSITIVE_STATUS_CODES):
            print("Actual response received ")
            self.decode_and_load_json(response)

    def patch_api(self, endpoint, body):
        print('Making a PATCH request to ' + endpoint + ' with body ')
        print(body)
        response = requests.patch(self.localhost + endpoint, headers = self.HEADERS, data = body)
        self.print_curl_request_and_response(response)
        return response

    def decode_and_load_json(self, response):
        try:
            data = json.loads(response.content.decode('utf-8'))
        except Exception as e:
            print("Except")
            logging.exception(str(e))
            return response
        return data
    ### Helper functions end here

    def test_get_on_empty_db_test(self):
        print("test_get_on_empty_db_test")
        try:
            endpoint = 'memes'
            response = self.get_api(endpoint)
            endpoint = 'memes/'
            response_with_slash = self.get_api(endpoint)
            self.assertFalse(response.status_code != 200)
            self.assertEqual(response_with_slash.status_codem, 200)
            if response.status_code in self.POSITIVE_STATUS_CODES:
                self.list['status'] = True
                data = self.decode_and_load_json(response)
                print(data)
            else:
                self.fail('Localhost not running- status false. ')
        except Exception as e:
            logging.exception(str(e))

    # First Post
    def test_first_post_test(self):
        endpoint = 'memes'
        body = {
            'name': 'crio-user',
            'caption': 'crio-meme',
            'url': self.SAMPLE_URL + self.FIRST_POST
        }
        response = self.post_api(endpoint, json.dumps(body))
        print("verify that response status code is one of " + str(self.POSITIVE_STATUS_CODES))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        print('First post data: ', data)
        self.FIRST_POST_ID = data['id']
        print('Assigned successfully' + str(self.FIRST_POST_ID))
        self.list['first-post'] = 10
        self.list['test-results'] += 'Score 2 Test(First Post) successful. '

    def test_get_single_meme(self):  # Score 6
        try:
            endpoint = 'memes/{}'.format(self.FIRST_POST_ID)
            response = self.get_api(endpoint)
            self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
            data = self.decode_and_load_json(response)
            print('get single: ', data)
            self.assertEqual(data['name'], 'crio-user')
            self.assertEqual(data['caption'], 'crio-meme')
            self.assertEqual(data['url'], self.SAMPLE_URL + self.FIRST_POST)
        except Exception as e:
            self.list['test-results'] += 'Score 6 test(Get single meme) failed. '
            logging.exception(str(e))

    def test_get_single_meme_non_existent_test(self):
        try:
            endpoint = 'memes/0909'
            response = self.get_api(endpoint)
            print('Status code for non existent meme: ', response.status_code)
            self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)
            self.score += 4
            print('Meme not found')
            self.list['test-results'] += 'Score 7 test(Get single non existent meme) Passed. '
            self.list['get-single-non-existent-meme'] = 4
        except Exception as e:
            self.list['test-results'] += 'Score 7 test(Get single non existent meme) failed. '
            logging.exception(str(e))

    def test_post_duplicate_test(self):
        try:
            endpoint = 'memes'
            body = {
                'name': 'crio-user-1',
                'caption': 'crio-meme-1',
                'url': self.SAMPLE_URL + self.FIRST_POST
            }
            response = self.post_api(endpoint, json.dumps(body))
            self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)
            self.score += 4
            self.list['test-results'] += 'Score 8 test(Post duplicate) Passed. '
            self.list['post-duplicate'] = 4

        except Exception as e:
            self.list['test-results'] += 'Score 8 test(Post duplicate) failed. '
            logging.exception(str(e))

    def test_post_empty_test(self):
        try:
            endpoint = 'memes'
            body = {}
            response = self.post_api(endpoint, json.dumps(body))
            self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)
            self.score += 2
            self.list['post-empty-body'] = 2
            self.list['test-results'] += "Score 9 test(empty body) passed. "

        except Exception as e:
            self.list['test-results'] += "Score 9 test(empty body) failed. "
            logging.exception(str(e))

    def test_post_incomplete_test(self):
        try:
            endpoint = 'memes'
            body = {
                'name': 'crio-go-9',
                'caption': 'sam-cap'
            }
            response = self.post_api(endpoint, json.dumps(body))
            self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)
            self.score += 1
            self.list['test-results'] += 'Score 10 test(Post incomplete meme) Passed. '
            self.list['post-incomplete-meme'] = 1

        except Exception as e:
            self.list['test-results'] += 'Score 10 test(Post incomplete meme) failed. '
            logging.exception(str(e))

    def test_less_than_100_post_test(self):
        try:
            endpoint = 'memes'
            for i in range(1, 50):
                body = {
                    'name': 'crio-user-' + str(i),
                    'caption': 'crio-meme-' + str(i),
                    'url': self.SAMPLE_URL + str(i) + '.png'
                }
                response = self.post_api(endpoint, json.dumps(body))
                self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        except Exception as e:
            self.list['test-results'] += 'Score 4 test(Post less than 100 memes) failed. '
            logging.exception(str(e))

    def test_more_than_100_post_test(self): # Score 5
        try:
            endpoint = 'memes'
            for i in range(51, 104):
                body = {
                    'name': 'A' + str(i),
                    'caption': 'B' + str(i),
                    'url': self.SAMPLE_URL + str(i) + '.png'
                }
                response = self.post_api(endpoint, json.dumps(body))
            ## Finally, after posting all 50
            self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
            data = self.decode_and_load_json(response)
            new_response = self.get_api(endpoint)
            flag = True
            self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)

            data = self.decode_and_load_json(new_response)
            print("length ", len(data))
            self.assertEqual(len(data), 100)

            if flag:
                print('good')
                self.list['post-gt-100-memes'] = 8
                self.list['test-results'] += 'Score 5 test(Post > 100) passed. '
                self.score += 8
        except Exception as e:
            self.list['test-results'] += 'Score 5 test(Post > 100) failed. '
            logging.exception(str(e))

    # Patch existing meme
    def test_update_existing_meme_url_test(self):
        try:
            endpoint = 'memes/{}'.format(self.SECOND_POST_ID)
            body = {
                'url': self.SAMPLE_URL + self.UPDATED_POST
            }
            response = self.patch_api(endpoint, json.dumps(body))
            self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
            print("Patch URL stage 1")
            # data = self.decode_and_load_json(response)
            new_response = self.get_api(endpoint)

            self.assertIn(new_response.status_code, self.POSITIVE_STATUS_CODES)
            print("Patch URL stage 2")
            data = self.decode_and_load_json(new_response)
            print('Patch Data: ', data)
            self.assertEqual(data['name'], 'crio-user')
            self.assertEqual(data['caption'], 'crio-meme')
            self.assertEqual(data['url'], self.SAMPLE_URL + self.UPDATED_POST)
            self.score += 3
            print('new update works: ', data['id'])
            self.list['test-results'] += 'Score 3 test(Update meme URL) passed. '
            self.list['update-meme-url'] = 3

        except Exception as e:
            self.list['test-results'] += 'Score 3 test(Update meme URL) failed. '
            logging.exception(str(e))

    def test_update_existing_meme_name_test(self):
        try:
            endpoint = 'memes/{}'.format(self.SECOND_POST_ID)
            body = {
                'name': 'update_meme_name',
            }
            response = self.patch_api(endpoint, json.dumps(body))
            self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)

            new_response = self.get_api(endpoint)
            self.assertIn(new_response.status_code, self.POSITIVE_STATUS_CODES)
            data = self.decode_and_load_json(new_response)
            print('Patch Name Data: ', data)
            self.assertEqual(data['name'], 'update_meme_name')
            self.assertEqual(data['caption'], 'crio-meme')
            self.assertEqual(data['url'], self.SAMPLE_URL + self.UPDATED_POST)
            self.score += 4
            print('Name not updated, as expected')
            self.list['test-results'] += 'Score 11 test(Update name) Passed. '
            self.list['patch-update-name'] = 4

        except Exception as e:
            self.list['test-results'] += 'Score 11 test(Update name) failed. '
            logging.exception(str(e))

    def test_update_existing_meme_caption_test(self):
        try:
            endpoint = 'memes/{}'.format(self.SECOND_POST_ID)
            body = {
                'caption': 'update-crio-caption'
            }
            response = self.patch_api(endpoint, json.dumps(body))
            self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
                # data = self.decode_and_load_json(response)
            new_response = self.get_api(endpoint)
            self.assertIn(new_response.status_code, self.POSITIVE_STATUS_CODES)
            data = self.decode_and_load_json(new_response)
            print('Patch Data: ', data)
            self.assertEqual(data['caption'] == 'update-crio-caption')
            self.score += 2
            print('new update works')
            self.list['test-results'] += 'Score 12 test(Update caption) Passed. '
            self.list['patch-update-caption'] = 2

        except Exception as e:
            self.list['test-results'] += 'Score 12 test(Update caption) failed. '
            logging.exception(str(e))

    def test_update_existing_meme_caption_and_url_test(self):
        try:
            endpoint = 'memes/{}'.format(self.SECOND_POST_ID)
            body = {
                'caption': 'update-caption-2',
                'url': self.SAMPLE_URL + self.SECOND_POST
            }
            response = self.patch_api(endpoint, json.dumps(body))
            self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
            # data = self.decode_and_load_json(response)
            new_response = self.get_api(endpoint)
            self.assertIn(new_response.status_code, self.POSITIVE_STATUS_CODES)
            data = self.decode_and_load_json(new_response)
            print('Update C and U Data: ', data)
            self.assertEqual(data['caption'], 'update-caption-2')
            self.assertEqual(data['url'] == self.SAMPLE_URL + self.SECOND_POST)
            self.score += 2
            print('Patch both works')
            self.list['test-results'] += 'Score 13 test(Update both) Passed. '
            self.list['patch-update-both'] = 2

        except Exception as e:
            self.list['test-results'] += 'Score 13 test(Update caption) failed. '
            logging.exception(str(e))

    ## Calling function
    def test_patch_meme_non_existent_test(self):
        try:
            body = {
                'name':'crio-user-09099',
                'caption': 'crio-meme-09099',
                'url': self.SAMPLE_URL + '09099'
            }
            endpoint = 'memes/09099'
            response = self.patch_api(endpoint, json.dumps(body))
            print('Status code for patch non existent meme: ', response.status_code)
            self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)
            self.score += 2
            print('Patch meme when not found')
            self.list['test-results'] += 'Score 14 test(Patch single non existent meme) Passed. '
            self.list['patch-non-existent'] = 2

        except Exception as e:
            self.list['test-results'] += 'Score 14 test(Patch single non existent meme) failed. '
            logging.exception(str(e))

    def base_score_generator(self):
        logging.info('Getonemptydbtest')
        self.get_on_empty_db_test()
        logging.info('FirstPostTest')
        self.first_post_test()
        logging.info('GetSingleMeme')
        self.get_single_meme()
        self.list['scoretotal'] = self.score
        return self.list

    def test_create_post_for_update_operations(self):
        try:
            endpoint = 'memes'
            body = {
                'name': 'crio-user',
                'caption': 'crio-meme',
                'url': self.SAMPLE_URL + self.SECOND_POST
            }
            response = self.post_api(endpoint, json.dumps(body))
            self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
            data = self.decode_and_load_json(response)
            print('Second post data: ', data)
            self.SECOND_POST_ID = data['id']
            print('Assigned successfully' + str(self.SECOND_POST_ID))

        except Exception as e:
            logging.exception(e)

    def bonus_score_generator(self):
        logging.info('PostDuplicate')
        self.post_duplicate_test()
        logging.info('SingleMemeNonExistent')
        self.get_single_meme_non_existent_test()
        logging.info('PostIncomplete')
        self.post_incomplete_test()
        logging.info('PostEmpty')
        self.post_empty_test()

        logging.info('LessThan100Post')
        # self.less_than_100_post_test()
        logging.info('GreaterThan100Post')
        # self.more_than_100_post_test()

        # Create a post to get an id.
        logging.info('CreatePostForUpdateOperations')
        self.create_post_for_update_operations()
        logging.info('UpdateExistingMemeURL')
        self.update_existing_meme_url_test()
        logging.info('UpdateExistingMemeName')
        self.update_existing_meme_name_test()
        logging.info('UpdateExistingMemeCaption')
        self.update_existing_meme_caption_test()
        logging.info('UpdateExistingMemeCaptionAndURL')
        self.update_existing_meme_caption_and_url_test()
        logging.info('PatchMemeNonExistent')
        self.patch_meme_non_existent_test()
        # logging.info('Swagger')
        # self.swagger_test()
        self.list['scoretotal'] = self.score
        return self.list

if __name__ == '__main__':
    unittest.main()