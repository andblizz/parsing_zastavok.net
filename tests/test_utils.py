import unittest
from unittest.mock import patch, MagicMock
from scraper.settings import TIMEOUT
from scraper.utils import get_html, download_image, requests
import os


class TestModule(unittest.TestCase):

    @patch('scraper.utils.requests.get')
    @patch('scraper.utils.random.choice', side_effect=lambda x: x[0])
    def test_get_html_success(self, mock_random_choice, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.encoding = 'utf-8'
        mock_response.text = '<html>Test</html>'
        mock_requests_get.return_value = mock_response

        url = 'https://example.com'
        result = get_html(url)

        self.assertEqual(result, mock_response)
        mock_requests_get.assert_called_once_with(
            url, headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                                        "like Gecko) Chrome/91.0.4472.124 Safari/537.36"}, params=None,
            proxies=None, timeout=TIMEOUT
        )

    @patch('scraper.utils.requests.get')
    @patch('scraper.utils.random.choice', side_effect=lambda x: x[0])
    def test_get_html_error(self, mock_random_choice, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.RequestException("Connection error")
        url = 'https://example.com'
        result = get_html(url)

        self.assertIsNone(result)
        mock_requests_get.assert_called_once()

    @patch('scraper.utils.requests.get')
    def test_download_image_success(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'content-disposition': 'attachment; filename="test_image.jpg"'}
        mock_response.iter_content = MagicMock(return_value=[b'test data'])
        mock_requests_get.return_value = mock_response

        pic_url = 'https://example.com/test_image.jpg'

        output_dir = 'test_output'
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, 'test_image.jpg')

        if os.path.exists(filepath):
            os.remove(filepath)

        download_image(pic_url, output_dir)
        self.assertTrue(os.path.exists(filepath))

        if os.path.exists(filepath):
            os.remove(filepath)
            os.rmdir(output_dir)

    @patch('scraper.utils.requests.get')
    def test_download_image_404_error(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = '404 Not Found'
        mock_response.headers = {}
        mock_requests_get.return_value = mock_response

        pic_url = 'https://example.com/test_image.jpg'
        output_dir = 'test_output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        download_image(pic_url, output_dir)

        mock_requests_get.assert_called_with(pic_url, stream=True)

        if os.path.exists(output_dir):
            os.remove(output_dir + "/test_image.jpg")
            os.rmdir(output_dir)

    @patch('scraper.utils.requests.get')
    def test_download_image_no_filename(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.iter_content = MagicMock(return_value=[b'test data'])
        mock_requests_get.return_value = mock_response

        pic_url = 'https://example.com/test_image.jpg'
        output_dir = 'test_output'
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, 'test_image.jpg')

        if os.path.exists(filepath):
            os.remove(filepath)

        download_image(pic_url, output_dir)
        self.assertTrue(os.path.exists(filepath))

        if os.path.exists(filepath):
            os.remove(filepath)


if __name__ == '__main__':
    unittest.main()
