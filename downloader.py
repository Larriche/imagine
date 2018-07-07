import io
import os
import json
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

        # Google image search url built from query
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
            self.print_http_error(http_error, exiting=True)
        except mechanize.URLError as url_error:
            self.print_url_error(url_error, exiting=True)
        finally:
            if not html:
                return

        image_urls = self.get_image_urls(html)

        # Truncate quantity if needed to fit within results count
        quantity = min(quantity, len(image_urls))
        downloaded = 0

        while (downloaded < quantity) and len(image_urls):
            save_path = self.folder + "/image_{}.{}".format(str(downloaded + 1), extension)
            url = image_urls.pop()

            try:
                res = self.browser.open(url)
                image_data = io.BytesIO(res.read())
                image = Image.open(image_data)
                image.save(save_path, self.image_type_map[extension])
                downloaded += 1
                self.print_status(downloaded, quantity)
            except mechanize.HTTPError as http_error:
                self.print_http_error(http_error)
            except mechanize.URLError as url_error:
                self.print_url_error(url_error)
            except Exception as e:
                self.print_image_error()

    def get_image_urls(self, html):
        """
        Extract image urls from search results
        """
        soup = BeautifulSoup(html, "html.parser")
        image_urls = []

        for a in soup.find_all("div", {"class":"rg_meta"}):
            url = json.loads(a.text)["ou"]
            image_urls.append(str(url))

        return image_urls

    def print_http_error(self, error, exiting=False):
        """
        Print an error message for http errors
        """
        message = "Encountered an HTTP error with status code {} :(".format(error.code)

        if exiting:
            message += "\nPlease try again."

        print message

    def print_url_error(self, error, exiting=False):
        """
        Print an error message for URL errors
        """
        message = "Unable to download images :("

        if exiting:
            message += "\nPlease try again"

        print message

    def print_image_error(self):
        """
        Print an error message for errors occurring during download and save of image
        """
        print "An error occurred while saving image. Image skipped"

    def print_status(self, downloaded, quantity):
        """
        Print status of downloads so far
        """
        print '{} out of {} images downloaded'.format(str(downloaded), str(quantity))