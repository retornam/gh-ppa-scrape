#!/usr/bin/env python3
import csv
import glob
import os
from multiprocessing import Pool

from bs4 import BeautifulSoup


def parse_html_file(file_path):
    with open(file_path, "r") as html_file:
        html_content = html_file.read()
    soup = BeautifulSoup(html_content, "html.parser")
    dt_elements = soup.find_all("dt")
    dd_elements = soup.find_all("dd")
    ttemp = [s.get_text().strip() for s in dt_elements]
    vtemp = [
        s.get_text().replace("\n", " ").replace("\t", " ").replace("\r", " ").strip()
        for s in dd_elements
    ]
    return ttemp, vtemp


def write_csv_file(filename, titles, values):
    with open(filename, "w") as csv_file:
        csv_writer = csv.writer(csv_file, dialect="unix")
        csv_writer.writerow(titles)
        for value in values:
            csv_writer.writerow(value)
    print(f"CSV file saved as {filename}")


def process_folder(folder_path):
    allfiles = glob.glob(f"{folder_path}/*")
    allfiles.sort()
    titles = None
    tender_types = {"Open Tender": [], "Restricted Tender": [], "Single Sourced": []}
    for file_path in allfiles:
        ttemp, vtemp = parse_html_file(file_path)
        for key in tender_types.keys():
            if key in vtemp:
                tender_types[key].append(vtemp)
                if key == "Open Tender":
                    open_tender_titles = ttemp
                else:
                    titles = ttemp
    return titles, open_tender_titles, tender_types


if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    folder_path = f"{script_directory}/alltenders"
    with Pool(processes=os.cpu_count()) as pool:
        results = pool.map(process_folder, [folder_path])
    titles, open_tender_titles, tender_types = results[0]

    restricted_file_path = f"{script_directory}/csv/tenders-ppa-restricted.csv"
    single_sourced_file_path = f"{script_directory}/csv/tenders-ppa-single-sourced.csv"
    open_file_path = f"{script_directory}/csv/tenders-ppa-open.csv"

    write_csv_file(restricted_file_path, titles, tender_types["Restricted Tender"])
    write_csv_file(single_sourced_file_path, titles, tender_types["Single Sourced"])
    write_csv_file(open_file_path, open_tender_titles, tender_types["Open Tender"])
