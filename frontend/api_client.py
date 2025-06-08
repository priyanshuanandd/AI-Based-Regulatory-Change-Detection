import requests

BASE_URL = "http://localhost:8000"

def compare_sections(old_file, new_file):
    files = {
        "old_version": ("old.txt", old_file.getvalue()),
        "new_version": ("new.txt", new_file.getvalue())
    }
    response = requests.post(f"{BASE_URL}/compare/sections", files=files)
    return response.json() if response.status_code == 200 else None

def compare_paragraphs(old_file, new_file):
    files = {
        "old_version": ("old.txt", old_file.getvalue()),
        "new_version": ("new.txt", new_file.getvalue())
    }
    response = requests.post(f"{BASE_URL}/compare/paragraphs", files=files)
    return response.json() if response.status_code == 200 else None

def analyze_added_sections(old_file, new_file):
    files = {
        "old_version": ("old.txt", old_file.getvalue()),
        "new_version": ("new.txt", new_file.getvalue())
    }
    response = requests.post(f"{BASE_URL}/added/ai", files=files)
    return response.json() if response.status_code == 200 else None

def analyze_modified_sections(old_file, new_file):
    files = {
        "old_version": ("old.txt", old_file.getvalue()),
        "new_version": ("new.txt", new_file.getvalue())
    }
    response = requests.post(f"{BASE_URL}/modified/ai", files=files)
    return response.json() if response.status_code == 200 else None