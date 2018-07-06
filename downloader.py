import io
import os
import json
import random
import urllib
import mechanize
from PIL import Image
from bs4 import BeautifulSoup

class ImageDownloader:
    def __init__(self, browser, query):
        """
        Create a new instance of this class
        """
        # Mechanize browser instance
        self.browser = browser

        # URL template for google image searches
        self.url = 'https://www.google.com.gh/search?q={}&tbm=isch'.format(urllib.quote_plus(query))

        # Downloads folder
        self.folder = 'downloads/{}'.format(query)

        # Mapping of given extensions to mime types
        self.image_type_map = {
            'jpg': 'JPEG',
            'png': 'PNG',
            'bmp': 'BMP',
            'gif': 'GIF'
        }

        # Create downloads folder
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def download_images(self, quantity, extension):
        """
        Download images from Google
        """
        html = ""

        if not extension in self.image_type_map:
            extension = 'jpg'
            print 'Unsupported image extension. Images will be saved in jpg format'

        try:
            res = self.browser.open(self.url)
            html = res.read()
        except mechanize.HTTPError as http_error:
            self.print_http_error(http_error)
        except mechanize.URLError as url_error:
            self.print_url_error(url_error)
        finally:
            if not html:
                return

        image_urls = self.get_image_urls(html, quantity)

        for index, url in enumerate(image_urls):
            save_path = self.folder + "/image_{}.{}".format(str(index + 1), extension)

            try:
                res = self.browser.open(url)
                image_data = io.BytesIO(res.read())
                image = Image.open(image_data)
                image.save(save_path, self.image_type_map[extension])

            except mechanize.HTTPError as http_error:
                self.print_http_error(http_error)
            except mechanize.URLError as url_error:
                self.print_url_error(url_error)

    def get_image_urls(self, html, quantity):
        """
        Select n images at random as candidates for download
        """
        soup = BeautifulSoup(html, "html.parser")
        image_urls = []

        for a in soup.find_all("div", {"class":"rg_meta"}):
            url = json.loads(a.text)["ou"]
            image_urls.append(str(url))

        quantity = min(quantity, len(image_urls))
        chosen = random.sample(image_urls, quantity)

        return chosen

    def print_http_error(self, error):
        """
        Print an error message for http errors
        """
        print "Encountered an HTTP error with status code {} :(".format(error.code)

    def print_url_error(self, error):
        """
        Print an error message for URL errors
        """
        print "Unable to download images :(\nPlease try again"