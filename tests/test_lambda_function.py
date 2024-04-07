import unittest
import sys
import os
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lambda_function import lambda_handler, fetch_pokemon_list, fetch_pokemon_details

class TestLambdaHandler(unittest.TestCase):
    @patch('lambda_function.requests.get')
    def test_fetch_pokemon_list_success(self, mock_requests_get):
        expected_result = [{"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1", "id": 1}]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": expected_result}
        mock_requests_get.return_value = mock_response
        
        result = fetch_pokemon_list()
        self.assertEqual(result, expected_result)

    @patch('lambda_function.requests.get')
    def test_fetch_pokemon_list_failure(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response
        
        result = fetch_pokemon_list()
        self.assertEqual(result, {"error": "Failed to fetch data from PokeAPI."})

    @patch('lambda_function.requests.get')
    def test_fetch_pokemon_details_success(self, mock_requests_get):
        expected_result = {"stat": [{"name": "speed", "base_stat": 45}], "weight": 69, "species": {"name": "bulbasaur"}, "abilities": [{"name": "overgrow"}], "moves": [{"name": "razor-wind"}, {"name": "swords-dance"}]}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_result
        mock_requests_get.return_value = mock_response
        
        result = fetch_pokemon_details(1)
        self.assertEqual(result, expected_result)

    @patch('lambda_function.requests.get')
    def test_fetch_pokemon_details_failure(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response
        
        result = fetch_pokemon_details(1)
        self.assertEqual(result, {"error": "Failed to fetch data from PokeAPI."})

    def test_lambda_handler_summary(self):
        event = {'path': '/summary', 'httpMethod': 'GET'}
        result = lambda_handler(event, {})
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('body', result)
        self.assertTrue(len(result['body']) > 0)

    def test_lambda_handler_details(self):
        event = {'path': '/details/1', 'httpMethod': 'GET'}
        result = lambda_handler(event, {})
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('body', result)
        self.assertTrue(len(result['body']) > 0)

    def test_lambda_handler_invalid_endpoint(self):
        event = {'path': '/invalid', 'httpMethod': 'GET'}
        result = lambda_handler(event, {})
        self.assertEqual(result['statusCode'], 404)
        self.assertIn('body', result)
        self.assertTrue(len(result['body']) > 0)

if __name__ == '__main__':
    unittest.main()
