import argparse
from colorama import Fore, Style
from bs4 import BeautifulSoup
import requests

# def crawl():


def arachnida():
	parser = argparse.ArgumentParser(prog='spider.py', description='Extract all the images from a website.', epilog='Luigi\'s mansion')

	parser.add_argument('url', help='URL to crawl.')
	parser.add_argument('-r', action='store_true', help='Recursively downloads the images.')
	parser.add_argument('-l', type=int, default=5, help='Maximum depth level of the recursive download.')
	parser.add_argument('-p', default='./data/', help='The path where the downloaded files will be saved.')

	args = parser.parse_args()

	print(Fore.GREEN + "URL:" + Style.RESET_ALL, args.url)
	print(Fore.GREEN + "Recursive:" + Style.RESET_ALL, args.r)
	print(Fore.GREEN + "Depth:" + Style.RESET_ALL, args.l)
	print(Fore.GREEN + "PATH:" + Style.RESET_ALL, args.p)

	response = requests.get(args.url)
	print(response.text)


if __name__ == '__main__':
	arachnida()
