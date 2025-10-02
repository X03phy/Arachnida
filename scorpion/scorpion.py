import argparse
from colorama import Fore, Style
from PIL import Image
from PIL.ExifTags import TAGS
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')


def extract_metadata(image_path):
	try:
		img = Image.open(image_path)

	except Exception as e:
		print(Fore.RED + f'{img}: cannot open file' + Style.RESET_ALL)
		return

	info_dict = {
		'Filename': img.filename,
		'Image Size': img.size,
		'Image Height': img.height,
		'Image Width': img.width,
		'Image Format': img.format,
		'Image Mode': img.mode,
		'Image is Animated': getattr(img, 'is_animated', False),
		'Frames in Image': getattr(img, 'n_frames', 1)
	}

	output = ''
	for k, v in info_dict.items():
		output += f"{k:15}: {v}\n"
	
	exifdata = img.getexif()
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


def delete_metadata(image_path):
	try:
		img = Image.open(image_path)
		img.info.pop("exif", None)  # delete EXIF
		img.save(image_path)
		messagebox.showinfo("EXIF deleted", f"Image saved without EXIF : {image_path}")
	except Exception as e:
		messagebox.showerror("Error", str(e))


def modify_metadata(image_path, tag, new_value):
	try:
		img = Image.open(image_path)
		exif = img.getexif()
		exif[306] = new_value # EXIF 306 DateTime
		img.save(image_path, exif=exif)
		messagebox.showinfo("EXIF modified", f"{tag} modified")
	except Exception as e:
		messagebox.showerror("Error", str(e))


def create_interface(args):
	root = tk.Tk()           # Create window
	root.title("scorpion")   # Title
	root.geometry("700x500") # Size

	notebook = ttk.Notebook(root)
	notebook.pack(expand=True, fill="both")

	for image in args.images:
		if any(image.endswith(ext) for ext in VALID_EXTENSIONS):
			title = image.split("/")[-1]
			frame = ttk.Frame(notebook)
			notebook.add(frame, text=title)

			left_frame = tk.Frame(frame)
			left_frame.pack(side="left", fill="both", expand=True)

			right_frame = tk.Frame(frame, width=150)
			right_frame.pack(side="right", fill="y", padx=10, pady=10)

			metadata_text = tk.Text(left_frame, width=100, height=50)
			metadata_text.pack(padx=10, pady=10, fill="both", expand=True)

			metadata_text.insert(tk.END, f"--- {title} ---\n")
			metadata_text.insert(tk.END, extract_metadata(image))
			metadata_text.insert(tk.END, "\n\n")

			if args.modify:
				btn_frame = tk.Frame(frame)
				btn_frame.pack(side="right", padx=10, pady=10)

				# button deletion EXIF
				del_btn = tk.Button(right_frame, text="Supprimer EXIF",
										command=lambda path=image: delete_metadata(path))
				del_btn.pack(pady=5)

				# button modification EXIF
				mod_btn = tk.Button(right_frame, text="Modifier DateTime",
										command=lambda path=image: modify_metadata(path, "DateTime", datetime.now().strftime("%Y:%m:%d %H:%M:%S")))
				mod_btn.pack(pady=5)

	root.mainloop()


def scorpion():
	parser = argparse.ArgumentParser(prog='spider.py', description='Parse image files for metadata')
	parser.add_argument('images', nargs='+', help='Image files to analyze')
	parser.add_argument('-m', '--modify', action='store_true', help='Modify or delete metadata of images')

	args = parser.parse_args()

	create_interface(args)


if __name__ == '__main__':
	scorpion()
