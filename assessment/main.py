import unittest
from unittest import TestCase

import curlify
import pytest
import requests
import json
import logging
import socket
import os

## Global variables and functions
from pytest import fail

scores = {}
logs_directory = '/home/ubuntu/'

def check_server(address, port):
    # Create a TCP socket
    s = socket.socket()
    # print("Attempting to connect to {} on port {}".format(address, port))
    try:
        s.connect((address, port))
        # print( "Connected to %s on port %s" % (address, port))
        return True
    except socket.error:
        # print ("Connection to %s on port %s failed" % (address, port))
        return False
    finally:
        s.close()
        
def clean_db():
    os.system('mongo Xmeme --eval "db.dropDatabase()"')

class XMemeAssessment(TestCase):

    HEADERS = None

    def __init__(self, *args, **kwargs):
        # os.system('mongo Xmeme --eval "db.dropDatabase()"')
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.HEADERS = {"Content-Type": "application/json"} # "X-Firebase-Auth": "INTERNAL_IMPERSONATE_USER_" + str(user),
        self.localhost = 'http://localhost:8081/'

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
        # print('Making a GET request to ' + endpoint)
        response = requests.get(self.localhost + endpoint, headers=self.HEADERS)
        self.print_curl_request_and_response(response)
        return response

    def post_api(self, endpoint, body):
        # print('Making a POST request to ' + endpoint + ' with body ')
        # print(body)
        response = requests.post(self.localhost + endpoint, headers=self.HEADERS, data=body)
        self.print_curl_request_and_response(response)
        return response

    def print_curl_request_and_response(self, response):
        # print("Making curl request - ")
        # print(curlify.to_curl(response.request))
        # print('Received response with status code:' + str(response.status_code))
        if(response.status_code in self.POSITIVE_STATUS_CODES):
            # print("Actual response received ")
            self.decode_and_load_json(response)

    def patch_api(self, endpoint, body):
        # print('Making a PATCH request to ' + endpoint + ' with body ')
        # print(body)
        response = requests.patch(self.localhost + endpoint, headers = self.HEADERS, data = body)
        self.print_curl_request_and_response(response)
        return response

    def decode_and_load_json(self, response):
        try:
            text_response = response.content.decode('utf-8')
            data = json.loads(text_response)
        except Exception as e:
            # print("Except")
            logging.exception(str(e))
            return response
        return data
    ### Helper functions end here

    @pytest.fixture(scope="session", autouse=True)
    def db_cleanup(self, request):
        clean_db()
        request.addfinalizer(clean_db)

    @pytest.mark.run(order=1)
    def test_0_get_on_empty_db_test(self):
        """When run with empty database, get calls should return success, and response should be empty"""
        # print("test_get_on_empty_db_test")
        endpoint = 'memes/'
        response_with_slash = self.get_api(endpoint)
        self.assertEqual(response_with_slash.status_code, 200)
        # print(self.decode_and_load_json(response_with_slash))
        response_length = len(self.decode_and_load_json(response_with_slash))
        # print("length of the response received = {}".format(response_length))
        self.assertEqual(response_length, 0)

    # First Post
    @pytest.mark.run(order=2)
    def test_1_first_post_test(self):
        """Post first MEME and verify that it returns id in the response"""
        endpoint = 'memes/'
        body = {
            'name': 'crio-user',
            'caption': 'crio-meme',
            'url': self.SAMPLE_URL + self.FIRST_POST
        }
        response = self.post_api(endpoint, json.dumps(body))
        # print("verify that response status code is one of " + str(self.POSITIVE_STATUS_CODES))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        # print('First post data: ', data)
        self.FIRST_POST_ID = data['id']
        # print('Assigned successfully' + str(self.FIRST_POST_ID))

    @pytest.mark.run(order=3)
    def test_2_get_single_meme(self):  # Score 6
        """Post a new MEME, capture its Id, and verify its GET /meme/{id} returns correct MEME"""
        endpoint = 'memes/'
        body = {
            'name': 'crio-user' + "9999",
            'caption': 'crio-meme' + "9999",
            'url': self.SAMPLE_URL + self.FIRST_POST
        }
        response = self.post_api(endpoint, json.dumps(body))
        # print("verify that response status code is one of " + str(self.POSITIVE_STATUS_CODES))
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        # print('First post data: ', data)

        # inserted, now get it using get api.
        endpoint = 'memes/{}'.format(data["id"])
        response = self.get_api(endpoint)
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)
        data = self.decode_and_load_json(response)
        # print('get single: ', data)
        self.assertEqual(data['name'], 'crio-user' + "9999")
        self.assertEqual(data['caption'], 'crio-meme' + "9999")
        self.assertEqual(data['url'], self.SAMPLE_URL + self.FIRST_POST)


    @pytest.mark.run(order=4)
    def test_3_get_single_meme_non_existent_test(self):
        """Try to access MEME with some random id, and verify that it returns 404"""
        endpoint = 'memes/0909'
        response = self.get_api(endpoint)
        # print('Status code for non existent meme: ', response.status_code)
        self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)

    @pytest.mark.run(order=5)
    def test_4_post_duplicate_test(self):
        """Verify that posting duplicate MEME return 409"""
        endpoint = 'memes/'
        body = {
            'name': 'crio-user',
            'caption': 'crio-meme',
            'url': self.SAMPLE_URL + self.FIRST_POST
        }
        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)

    @pytest.mark.run(order=6)
    def test_5_post_empty_test(self):
        """Verify that API doesnt accept empty data in POST call"""
        endpoint = 'memes/'
        body = {}
        response = self.post_api(endpoint, json.dumps(body))
        self.assertIn(response.status_code, self.NEGATIVE_STATUS_CODES)


    @pytest.mark.run(order=7)
    def test_6_less_than_100_post_test(self):
        """Insert 50 MEMEs and try accessing them to confirm that all of them are returned back"""
        endpoint = 'memes/'
        for i in range(1, 50):
            body = {
                'name': 'crio-user-' + str(i),
                'caption': 'crio-meme-' + str(i),
                'url': self.SAMPLE_URL + str(i) + '.png'
            }
            response = self.post_api(endpoint, json.dumps(body))
            self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)

        get_response = self.get_api(endpoint)
        data = self.decode_and_load_json(get_response)
        self.assertGreater(len(data), 50)

    @pytest.mark.run(order=8)
    def test_7_more_than_100_post_test(self): # Score 5
        """Post more than 100 MEME, make a GET call and ensure that it returns only latest 100 MEME"""
        endpoint = 'memes/'
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
        self.assertIn(response.status_code, self.POSITIVE_STATUS_CODES)

        data = self.decode_and_load_json(new_response)
        # print("length ", len(data))
        self.assertEqual(len(data), 100)
        self.assertEqual(data[99]["name"], 'crio-user-3')
        self.assertEqual(data[0]["name"], 'A103')

if __name__ == '__main__':
    unittest.main()