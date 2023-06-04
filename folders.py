import requests
import os
import xml.etree.ElementTree as ET
import re

url = "https://archive.org/advancedsearch.php?q=paris&fl%5B%5D=description&fl%5B%5D=downloads&fl%5B%5D=source&sort%5B%5D=&sort%5B%5D=&sort%5B%5D=&rows=50&page=1&callback=callback&save=yes&output=xml"

response = requests.get(url)
xml_data = response.text

root = ET.fromstring(xml_data)
def process_element(element, path):
    if len(element) > 0:
        new_path = os.path.join(path, sanitize_filename(element.tag))
        os.makedirs(new_path, exist_ok=True)
        for child in element:
            process_element(child, new_path)
    else:
        file_path = os.path.join(path, sanitize_filename(element.tag) + ".txt")
        with open(file_path, "w") as file:
            file.write(element.text)
def sanitize_filename(filename):
    cleaned_filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    return cleaned_filename
for child in root:
    process_element(child, ".")

print("Opération terminée.")
