import unittest
from unittest.mock import patch, MagicMock, call
from scraper.scraper import scrape_images, get_links, get_pic
import os


class TestScraper(unittest.TestCase):

    def test_get_links(self):
        html = '''
        <div class='short_prev'>
            <a href='/wallpaper1.html'><img src='img1.jpg'></a>
        </div>
        <div class='short_prev'>
            <a href='/wallpaper2.html'><img src='img2.jpg'></a>
        </div>
        '''
        links = get_links(html)
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

    @patch('scraper.scraper.get_pic')
    @patch('scraper.scraper.get_links')
    @patch('scraper.scraper.get_html')
    @patch('scraper.scraper.download_image')
    def test_scrape_images(self, mock_download_image, mock_get_html, mock_get_links, mock_get_pic):
        mock_get_html.side_effect = [
            MagicMock(text="<div class='short_prev'><a href='/image_page1'></a></div>"
                           "<div class='short_prev'><a href='/image_page2'></a></div>"),
            MagicMock(text='<a id="orig_size" href="/image1.jpg"></a>'),
            MagicMock(text='<a id="orig_size" href="/image2.jpg"></a>')
        ]
        mock_get_links.return_value = [
            'https://zastavok.net/image_page1',
            'https://zastavok.net/image_page2'
        ]
        mock_get_pic.side_effect = [
            'https://zastavok.net/image1.jpg',
            'https://zastavok.net/image2.jpg'
        ]

        test_dir = 'test_dir'
        os.makedirs(test_dir, exist_ok=True)

        scrape_images(1, 1, test_dir)

        self.assertEqual(mock_download_image.call_count, 2)
        mock_download_image.assert_has_calls([
            call('https://zastavok.net/image1.jpg', test_dir),
            call('https://zastavok.net/image2.jpg', test_dir)
        ], any_order=True)

        os.rmdir(test_dir)

    @patch('scraper.scraper.get_html')
    def test_scrape_images_error_handling(self, mock_get_html):
        mock_get_html.side_effect = [None]

        test_dir = 'test_dir'
        os.makedirs(test_dir, exist_ok=True)

        scrape_images(1, 1, test_dir)

        mock_get_html.assert_called_once()
        os.rmdir(test_dir)


if __name__ == '__main__':
    unittest.main()