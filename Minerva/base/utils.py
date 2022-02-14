
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



def fileTypeFinder(file):
    for format in format_dict:
        if str(file).endswith(format):
            return format_dict[format]
    return "Not Known"