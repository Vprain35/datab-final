import requests
from bs4 import BeautifulSoup
import re
import csv
import time

#FYI: THIS USES ACTUAL DATA FROM THE WEBSITE. I HAVE NOT CENSORED ANY RESULTS.

headers = {
    "User-Agent": "Mozilla/5.0"
}

books = []

# how many pages to scrape
MAX_PAGES = 5

for page in range(1, MAX_PAGES + 1):

    url = f"https://annas-archive.pk/search?index=&page={page}&sort=&lang=en&display=&q="

    print(f"Scraping page {page}...")

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    entries = soup.find_all(
        "div",
        class_="flex pt-3 pb-3 border-b last:border-b-0 border-gray-100"
    )

    for entry in entries:

        # TITLE
        title_tag = entry.find(
            "a",
            class_=lambda c: c and "text-[#2563eb]" in c
        )

        title = title_tag.get_text(strip=True) if title_tag else ""

        # AUTHOR + PUBLISHER
        info_links = entry.find_all(
            "a",
            href=re.compile(r"/search\?q=")
        )

        author = ""
        publisher = ""
        year = ""

        if len(info_links) > 0:
            author = info_links[0].get_text(strip=True)

        if len(info_links) > 1:
            publisher_text = info_links[1].get_text(strip=True)

            year_match = re.search(r"\b(19|20)\d{2}\b", publisher_text)

            if year_match:
                year = year_match.group()

            publisher = re.sub(r",?\s*(19|20)\d{2}\b", "", publisher_text)

        # DESCRIPTION
        description = ""

        desc_tag = entry.find(
            "div",
            class_=lambda c: c and "text-sm text-gray-600" in c
        )

        if desc_tag:
            description = desc_tag.get_text(" ", strip=True)

        books.append({
            "title": title.strip(),
            "author": author.strip(),
            "publisher": publisher.strip(),
            "releaseYear": year,
            "description": description.strip()
        })

    time.sleep(1)

# SAVE CSV
with open("library_catalogue.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "title",
            "author",
            "publisher",
            "releaseYear",
            "description"
        ]
    )

    writer.writeheader()
    writer.writerows(books)

print(f"Saved {len(books)} books to library_catalogue.csv")