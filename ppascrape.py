#!/usr/bin/env python3
import csv
import glob
import os

from bs4 import BeautifulSoup

script_directory = os.path.dirname(os.path.abspath(__file__))
folder_path = f"{script_directory}/alltenders"


all_titles = []
all_values = []
allfiles = glob.glob(f"{folder_path}/*")
allfiles.sort()


for file_path in allfiles:
    with open(file_path, "r") as html_file:
        html_content = html_file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    dt_elements = soup.find_all("dt")
    dd_elements = soup.find_all("dd")
    titles = []
    values = []
    for dt, dd in zip(dt_elements, dd_elements):
        titles.append(dt.get_text(strip=True).replace("\n", " "))
        values.append(dd.get_text(strip=True).replace("\n", " "))
    all_titles.append(titles)
    all_values.append(values)

all_values.sort()

csv_file_path = f"{script_directory}/csv/alltenders.csv"

with open(csv_file_path, "w") as csv_file:
    csv_writer = csv.writer(csv_file, dialect="unix")
    csv_writer.writerow(all_titles[0])
    for values in all_values:
        csv_writer.writerow(values)
print(f"CSV file saved as '{csv_file_path}'")
