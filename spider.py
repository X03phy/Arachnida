# https://www.geeksforgeeks.org/python/implementing-web-scraping-python-beautiful-soup/

# https://www.42network.org/42-schools/\?r\=europe
# https://42.fr/

import argparse
from colorama import Fore, Style
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import base64
import hashlib


HEADERS = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
					'AppleWebKit/537.36 (KHTML, like Gecko) '
					'Chrome/120.0 Safari/537.36'
}

VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

NB_DOWNLOADS = 0


def download_image(img_url, path): # download an image from its url
	try: # requests and response code can fail, makedirs can also fail (permissions or path)
		response = requests.get(img_url,  headers=HEADERS, timeout=5)
		response.raise_for_status()

		filepath = os.path.join(path, urlparse(img_url).path.lstrip('/')) # /path/url
		if os.path.isfile(filepath):
			return
		os.makedirs(os.path.dirname(filepath), exist_ok=True)

		with open(filepath, 'wb') as f:
			f.write(response.content)

		global NB_DOWNLOADS
		NB_DOWNLOADS += 1
		print(Fore.GREEN + '[+] Downloaded ' + Style.RESET_ALL + filepath)

	except Exception as e:
		print(Fore.RED + '[-] Failed ' + Style.RESET_ALL + f'{img_url}: {e}')


def download_base64_image(src, path):
	# "data:image/png;base64,asdasd..."
	header, base64_data = src.split(',', 1)

	mime_type = header.split(':')[1].split(';')[0] # image/png
	extension = '.' + mime_type.split('/')[-1] # .png
	if not any(extension == ext for ext in VALID_EXTENSIONS):
		return

	digest = hashlib.md5(base64_data.encode()).hexdigest()
	filename = f'base64_{digest}{extension}' # base64_0.png
	filepath = os.path.join(path, filename) # /path/base64_0.png

	if os.path.isfile(filepath):
		return

	os.makedirs(os.path.dirname(filepath), exist_ok=True)

	with open(filepath, 'wb') as f:
		f.write(base64.b64decode(base64_data)) # write in the created file the decoded base64 image

	global NB_DOWNLOADS
	NB_DOWNLOADS += 1
	print(Fore.GREEN + '[+] Downloaded ' + Style.RESET_ALL + filepath)


def download_images_from_page(page_url, path):
	try:
		response = requests.get(page_url, headers=HEADERS, timeout=5)
		response.raise_for_status()

	except Exception as e:
		print(Fore.RED + '[-] Failed ' + Style.RESET_ALL + f'{page_url}: {e}')
		return

	soup = BeautifulSoup(response.text, 'html.parser') # parse HTML

	for img in soup.find_all('img'):
		src = img.get('src')
		if not src:
			continue

		if src.startswith('data:image'): # base64 encoded image
			download_base64_image(src, path)

		else: # url image
			img_url = urljoin(page_url, src)
			if not any(img_url.lower().endswith(ext) for ext in VALID_EXTENSIONS):
				continue
			download_image(img_url, path)

def is_valid_url(url):
	parsed = urlparse(url)
	return parsed.scheme in ("http", "https")


def crawl(page_url, path, depth, max_depth, visited):
	if depth > max_depth or page_url in visited:
		return

	visited.add(page_url)

	try:
		response = requests.get(page_url, headers=HEADERS, timeout=5)
		response.raise_for_status()

	except Exception as e:
		print(Fore.RED + '[-] Failed ' + Style.RESET_ALL + f'{page_url}: {e}')
		return

	soup = BeautifulSoup(response.text, 'html.parser')

	for img in soup.find_all('img'):
		src = img.get('src')
		if not src:
			continue

		if src.startswith('data:image'): # base64 encoded image
			download_base64_image(src, path)

		else: # url image
			img_url = urljoin(page_url, src)
			if not any(img_url.lower().endswith(ext) for ext in VALID_EXTENSIONS):
				continue
			download_image(img_url, path)

	for link in soup.find_all('a'):
		href = link.get('href')
		if not href or href.startswith('#'):
			continue
		
		next_url = urljoin(page_url, href)
		if not is_valid_url(next_url):
			print(Fore.RED + '[-] Skipping non-http link:' + Style.RESET_ALL, next_url)
			continue
		crawl(next_url, path, depth + 1, max_depth, visited)


def arachnida():
	parser = argparse.ArgumentParser(prog='spider.py', description='Extract all the images from a website', epilog='Luigi\'s mansion')

	parser.add_argument('url', help='URL to crawl')
	parser.add_argument('-r', action='store_true', help='Recursively downloads the images')
	parser.add_argument('-l', type=int, default=5, help='Maximum depth level of the recursive download')
	parser.add_argument('-p', default='./data/', help='The path where the downloaded files will be saved')

	args = parser.parse_args()

	print(Fore.GREEN + 'URL:' + Style.RESET_ALL, args.url)
	print(Fore.GREEN + 'Recursive:' + Style.RESET_ALL, args.r)
	print(Fore.GREEN + 'Depth:' + Style.RESET_ALL, args.l)
	print(Fore.GREEN + 'PATH:' + Style.RESET_ALL, args.p)

	if args.r:
		crawl(args.url, args.p, 0, args.l, set())
	else:
		download_images_from_page(args.url, args.p)
	
	global NB_DOWNLOADS
	print(Fore.GREEN + 'Downloads:' + Style.RESET_ALL, NB_DOWNLOADS)


if __name__ == '__main__':
	arachnida()
