import mechanize
import argparse
import sys
from downloader import ImageDownloader

def main():
    # Set up commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('query', help='item to download images for')
    parser.add_argument('count', help='number of images to download', default=20)
    parser.add_argument('type', help='extension to save images as', default='jpg')

    # Set up browser
    browser = mechanize.Browser()
    user_agent = 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
    browser.addheaders = [('User-agent', user_agent)]
    browser.set_handle_robots(False)

    # Extract commandline arguments
    args = parser.parse_args()

    query = args.query
    count = int(args.count)
    extension = args.type

    # Run downloads
    downloader = ImageDownloader(browser, query)

    try:
        print 'Bringing your imaginations to reality...'
        downloader.download_images(count, extension)
    except KeyboardInterrupt:
        print '\nBye. See you soon :)'
        sys.exit(0)

if __name__ == '__main__':
    main()
