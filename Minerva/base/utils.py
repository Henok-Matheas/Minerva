from matplotlib.image import thumbnail
from preview_generator.manager import PreviewManager
import os
from pathlib import Path

book_format_list = [".pdf", ".docx", ".odt"]
format_dict = {
    ".pdf" : "book",
    ".docx" : "book",
    ".odt" : "book",
    ".mp4" : "video",
    ".mkv" : "video"
}
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

def thumbnailer(file):
    for format in book_format_list:
        if str(file).endswith(format):
            dest = str(BASE_DIR) + "/materials" + "/thumb"
            manager = PreviewManager(dest, create_folder = True)
            thumbnail = manager.get_jpeg_preview(str(BASE_DIR) + "/materials/" + str(file))
            return thumbnail


def fileTypeFinder(file):
    for format in format_dict:
        if str(file).endswith(format):
            return format_dict[format]
    return "Not Known"