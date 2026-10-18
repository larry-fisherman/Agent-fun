import re 
from pathlib import Path


def extract_lessons(review_text: str) -> str:
    match = re.search(r"<lessons>(.*?)</lessons>", review_text, re.DOTALL)
    if match is None:
        raise ValueError("No lessons block found in the review")
    return match.group(1).strip()

def save_lessons(lessons: str, path) -> None:
    path = Path(path)
    path.write_text(lessons)

def load_lessons(path) -> str:
    return Path(path).read_text()
