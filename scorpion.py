import argparse
from colorama import Fore, Style

def scorpion():
	parser = argparse.ArgumentParser(prog='spider.py', description='Parse image files for metadata')
	parser.add_argument('files', nargs='+', help='Image files to analyze')
	
	args = parser.parse_args() #! Attention aux Doublons

	for file in args.files:
		print(Fore.GREEN + 'File:' + Style.RESET_ALL, file)


if __name__ == '__main__':
	scorpion()
