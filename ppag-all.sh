#!/bin/bash

LAST=$(curl https://tenders.ppa.gov.gh/contracts\?page\=1 | htmlq --text '.page-item:nth-last-child(2)>a.page-link')

TENDERS=()
for page in $(seq 1 ${LAST}); do
    # Make a curl request to the URL
    echo $page
    output=$(curl --silent "https://tenders.ppa.gov.gh/contracts?page=$page" |
        htmlq 'div.list-title > a[href]' --attribute href)
    TENDERS+=($output)
done

##echo "${TENDERS[@]}"

for item in "${TENDERS[@]}"; do
    curl --create-dirs  --output-dir alltenders -LOJ $item
done
