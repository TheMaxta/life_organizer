import unittest
from unittest.mock import patch, MagicMock
from utils.llm_integration import get_llm_guidance

class TestLLMIntegration(unittest.TestCase):
    @patch('utils.llm_integration.requests.post')
    def test_get_llm_guidance(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'Test guidance'}}]
        }
        mock_post.return_value = mock_response

        result = get_llm_guidance('{"actions": []}', 'Test query')
        self.assertEqual(result, 'Test guidance')

    @patch('utils.llm_integration.requests.post')
    def test_get_llm_guidance_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = 'Error'
        mock_post.return_value = mock_response

        with self.assertRaises(Exception):
            get_llm_guidance('{"actions": []}', 'Test query')

if __name__ == '__main__':
    unittest.main()