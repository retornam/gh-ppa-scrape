#!/bin/bash

set -euo pipefail

fetch_tender_data() {
    page="${1}"
    output=$(curl --silent "https://tenders.ppa.gov.gh/contracts?page=$page" | \
        htmlq 'div.list-title > a[href]' --attribute href)
    echo "${output}"
}

export -f fetch_tender_data
LAST=$(curl https://tenders.ppa.gov.gh/contracts?page=1 | \
    htmlq --text '.page-item:nth-last-child(2)>a.page-link')
echo "LAST PAGE: ${LAST}"
TENDERS=($(seq 1 "${LAST}" | parallel -k -j+0 fetch_tender_data {}))
# version sort tenders
SORTED_TENDERS=($(echo "${TENDERS[@]}" | tr ' ' '\n' | sort --version-sort))

# Create a function to download a single file
download_file() {
    url="$1"
    curl --create-dirs --output-dir alltenders -LOJ "$url"
}
export -f download_file
# Use xargs to download the files in batches
echo "${SORTED_TENDERS[@]}" | xargs -I {} -P 50 -n 1 bash -c 'download_file "$@"' _ {}


