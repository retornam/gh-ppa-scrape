#!/usr/bin/env python3
import csv
import glob
import os

import requests
from bs4 import BeautifulSoup

script_directory = os.path.dirname(os.path.abspath(__file__))
folder_path = f"{script_directory}/alltenders"


all_titles = []
all_values = []
allfiles = glob.glob(f"{folder_path}/*")
allfiles.sort()

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "sec-ch-ua": "Chromium;v=116, Not)A;Brand;v=24, Google Chrome;v=116",
}
urls = [
    "https://www.ghaneps.gov.gh/epps/viewAllAwardedContracts.do?d-3998960-p=1&selectedItem=viewAllAwardedContracts.do&T01_ps=50000"
]

for url in urls:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    table_header_elements = soup.select("table>thead>tr>*")
    table_body_elements = soup.select("table>tbody>tr")
    all_titles.append(
        [
            i.text.replace("\n", "").replace("\t", "").replace("\r", "")
            for i in table_header_elements
        ]
    )
    for tb in table_body_elements:
        tb_item = tb.findAll("td")
        values = [
            i.text.replace("\n", "").replace("\t", "").replace("\r", "")
            for i in tb_item
        ]
        all_values.append(values)
    all_titles.append(table_header_elements)
all_values.sort()

csv_file_path = f"{script_directory}/csv/tenders-ghanaeps.csv"
with open(csv_file_path, "w") as csv_file:
    csv_writer = csv.writer(csv_file, dialect="unix")
    csv_writer.writerow(all_titles[0])
    for values in all_values:
        csv_writer.writerow(values)
print(f"CSV file saved as {csv_file_path}")
