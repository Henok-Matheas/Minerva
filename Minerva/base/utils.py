# from preview_generator.manager import PreviewManager
from thumbnail import generate_thumbnail
import os
from pathlib import Path

book_format_list = [".pdf", ".docx", ".odt"]
video_format_list = [".mp4", ".mkv"]
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
            dest = str(BASE_DIR) + "/materials" + "/thumbnails"
            manager = PreviewManager(dest, create_folder = True)
            thumbnail = manager.get_jpeg_preview(str(BASE_DIR) + "/materials/files/" + str(file))
            return thumbnail
    for format in video_format_list:
        if str(file).endswith(format):
            options = {
                'trim': False,
                'height': 256,
                'width': 256,
                'quality': 85,
                'type': 'thumbnail'
                }
            name = str(file)[:str(file).index(format)] + ".jpg"
            dest = "/materials" + "/thumbnails/" + name
            generate_thumbnail(file,dest,options)
            return dest


def fileTypeFinder(file):
    for format in format_dict:
        if str(file).endswith(format):
            return format_dict[format]
    return "Not Known"