import unittest
from unittest.mock import patch, MagicMock
from scraper.scraper import scrape_images, get_links, get_pic


class TestScraper(unittest.TestCase):

    @patch('scraper.utils.get_html')
    def test_get_links(self, mock_get_html):
        mock_html = '''
        <div class='short_prev'>
            <a href='/wallpaper1.html'><img src='img1.jpg'></a>
        </div>
        <div class='short_prev'>
            <a href='/wallpaper2.html'><img src='img2.jpg'></a>
        </div>
        '''
        mock_get_html.return_value = MagicMock(text=mock_html)
        links = get_links(mock_html)
        expected_links = [
            'https://zastavok.net/wallpaper1.html',
            'https://zastavok.net/wallpaper2.html'
        ]
        self.assertEqual(links, expected_links)

    def test_get_pic(self):
        html = '''
        <a id="orig_size" href='/images/original.jpg'>Download</a>
        '''
        pic_url = get_pic(html)
        expected_url = 'https://zastavok.net/images/original.jpg'
        self.assertEqual(pic_url, expected_url)

    @patch('scraper.scraper.get_links')
    @patch('scraper.scraper.get_html')
    @patch('scraper.utils.download_image')
    def test_scrape_images(self, mock_download_image, mock_get_html, mock_get_links):
        mock_get_html.return_value = MagicMock(text='html content')
        mock_get_links.return_value = ['https://zastavok.net/image_page1', 'https://zastavok.net/image_page2']

        scrape_images(1, 1, 'test_dir')

        mock_get_html.assert_called()
        mock_get_links.assert_called_once_with('html content')
        self.assertEqual(mock_download_image.call_count, 2)


if __name__ == '__main__':
    unittest.main()
