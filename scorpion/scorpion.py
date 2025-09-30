import argparse
from colorama import Fore, Style
from PIL import Image
from PIL.ExifTags import TAGS
import tkinter as tk


VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')


def extract_metadata(image):
	try:
		image = Image.open(image)

	except Exception as e:
		print(Fore.RED + f'{image}: cannot open file' + Style.RESET_ALL)
		return

	info_dict = {
		'Filename': image.filename,
		'Image Size': image.size,
		'Image Height': image.height,
		'Image Width': image.width,
		'Image Format': image.format,
		'Image Mode': image.mode,
		'Image is Animated': getattr(image, 'is_animated', False),
		'Frames in Image': getattr(image, 'n_frames', 1)
	}

	output = ''
	for k, v in info_dict.items():
		output += f"{k:15}: {v}\n"
	
	exifdata = image.getexif()
	for tag_id in exifdata:
		tag = TAGS.get(tag_id, tag_id) # get the tag name, instead of human unreadable tag id
		data = exifdata.get(tag_id)    # decode bytes 
		if isinstance(data, bytes):
			try:
				data = data.decode(errors='ignore')
			except:
				data = "<binary>"
		output += f"{tag:15}: {data}\n"
	return output


def create_interface(args):
	root = tk.Tk()           # Create window
	root.title("scorpion")   # Title
	root.geometry("700x500") # Size

	metadata_text = tk.Text(root, width=80, height=25)
	metadata_text.pack(padx=10, pady=10)

	for image in args.images:
		if any(image.endswith(ext) for ext in VALID_EXTENSIONS):
			metadata_text.insert(tk.END, f"--- {image} ---\n")
			metadata_text.insert(tk.END, extract_metadata(image))
			metadata_text.insert(tk.END, "\n\n")

	root.mainloop()



def scorpion():
	parser = argparse.ArgumentParser(prog='spider.py', description='Parse image files for metadata')
	parser.add_argument('images', nargs='+', help='Image files to analyze')
	parser.add_argument('-m', '--modify', action='store_true', help='Modify or delete metadata of images')

	args = parser.parse_args() #! Attention aux Doublons

	create_interface(args)


if __name__ == '__main__':
	scorpion()
