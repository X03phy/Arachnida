import argparse
from colorama import Fore, Style
from PIL import Image
from PIL.ExifTags import TAGS


VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')


def extract_metadata(image):
	image = Image.open(image)

	info_dict = {
		"Filename": image.filename,
		"Image Size": image.size,
		"Image Height": image.height,
		"Image Width": image.width,
		"Image Format": image.format,
		"Image Mode": image.mode,
		"Image is Animated": getattr(image, "is_animated", False),
		"Frames in Image": getattr(image, "n_frames", 1)
	}

	for label,value in info_dict.items():
		print(f"{label:25}: {value}")
	
	exifdata = image.getexif()

	for tag_id in exifdata:
		# get the tag name, instead of human unreadable tag id
		tag = TAGS.get(tag_id, tag_id)
		data = exifdata.get(tag_id)
		# decode bytes 
		if isinstance(data, bytes):
			data = data.decode()
		print(f"{tag:25}: {data}")

def scorpion():
	parser = argparse.ArgumentParser(prog='spider.py', description='Parse image files for metadata')
	parser.add_argument('images', nargs='+', help='Image files to analyze')
	
	args = parser.parse_args() #! Attention aux Doublons

	for image in args.images:
		print(Fore.GREEN + 'File:' + Style.RESET_ALL, image)
	
	for image in args.images:
		extract_metadata(image)


if __name__ == '__main__':
	scorpion()
