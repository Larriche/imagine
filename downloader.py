import os
import json
import mechanize
import urllib
import random
from bs4 import BeautifulSoup

class ImageDownloader:
    def __init__(self, browser, query, count):
        """
        Create a new instance of this class
        """
        # Mechanize browser instance
        self.browser = browser

        # URL template for google image searches
        self.url = 'https://www.google.com.gh/search?q={}&tbm=isch'.format(urllib.quote_plus(query))

        # Downloads folder
        self.folder = 'downloads/{}'.format(query)

        # Number of items to download
        self.count = count

        # Create downloads folder
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def download_images(self, quantity):
        """
        Download images from Google
        """
        res = self.browser.open(self.url)
        html = res.read()

        image_urls = self.get_image_urls(html, quantity)

        for index, image_url in enumerate(image_urls):
            url, ext = image_url
            save_path = self.folder + "/image_{}.{}".format(str(index + 1), ext)
            urllib.urlretrieve (url, save_path)

    def get_image_urls(self, html, quantity):
        """
        Select n images at random as candidates for download
        """
        soup = BeautifulSoup(html, "html.parser")
        image_urls = []

        for a in soup.find_all("div", {"class":"rg_meta"}):
            url, extension = json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
            image_urls.append((str(url), str(extension)))

        quantity = min(quantity, len(image_urls))
        chosen = random.sample(image_urls, quantity)

        return chosen