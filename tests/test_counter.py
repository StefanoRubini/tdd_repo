"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status

from src import counter


class CounterTest(TestCase):
    """Counter tests"""

    def setUp(self):
        self.client = app.test_client()

    # this works 100% (provided to us)
    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    # this works 100% (provided to us)
    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/baz')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/baz')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    # this is unique implementation
    def test_update_a_counter(self):
        """It should update a counter"""
        # 1. Make a call to create_counter(name)
        create_counter = self.client.post('/counters/bar')
        # 1a. Checking that the counter was successfully created
        self.assertEqual(create_counter.status_code, status.HTTP_201_CREATED)

        # 2. Ensure that it returned a successful return code
        base_value = create_counter.json['bar']

        # 3. Check the counter value as a baseline
        updated_value = self.client.put('/counters/bar')

        # 4. Make a call to Update the counter that you just created
        self.assertEqual(updated_value.status_code, status.HTTP_200_OK)

        # 5. Ensure that it returned a successful return code
        updated_counter_value = updated_value.json['bar']

        # 6. Check that the counter value is one more than the baseline you measured in Step 3
        self.assertGreater(updated_counter_value, base_value)

    def test_update_a_non_existent_counter(self):
        """It should return an error for updating a nonexistent counter"""
        # 1. Make a call to update a counter that does not exist
        result = self.client.put('/counters/non_existent')

        # 2. Make sure that a 404 error is returned
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    # this is unique implementation
    def test_read_a_counter(self):
        """It should read a counter"""
        # 1. Make a call to read_counter(name)
        counter_call = self.client.post('/counters/bax')
        self.assertEqual(counter_call.status_code, status.HTTP_201_CREATED)

        # 2. Ensure that it returned a successful return code
        counter_response = self.client.get('/counters/bax')
        self.assertEqual(counter_response.status_code, status.HTTP_200_OK)

        # 3. Read the value of the counter and store it in a variable
        counter_value = counter_response.json['bax']

        # 4. Ensure that it returned a successful return code
        self.assertEqual(counter_value, 0)

    def test_read_a_non_existent_counter(self):
        """It should return an error for reading a nonexistent counter"""
        # 1. Make a call to read a counter that does not exist
        result = self.client.get('/counters/non_existent')

        # 2. Make sure that a 404 error is returned
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_a_counter(self):
        """It should delete a counter"""
        # 1. Make a call to create_counter(name)
        create_counter = self.client.post('/counters/deleted')
        # 1a. Checking that the counter was successfully created
        self.assertEqual(create_counter.status_code, status.HTTP_201_CREATED)

        # 2. Deleting the recently created counter
        create_counter = self.client.delete('/counters/deleted')

        # 3. Making sure that the counter was successfully deleted
        self.assertEqual(create_counter.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_a_non_existent_counter(self):
        """It should return an error for deleting a nonexistent counter"""
        # 1. Make a call to delete a counter that does not exist
        result = self.client.delete('/counters/non_existent')

        # 2. Make sure that a 404 error is returned
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
