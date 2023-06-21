import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


def filename_from_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = os.path.basename(path)
    cleaned_filename = ''.join(c if c.isalnum() else '_' for c in filename)
    return cleaned_filename


def get_links(url, prefix):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith(prefix):
            links.append(get_base_url(url) + href)  # Add the base URL to the relative link
    return links


def fetch_page_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    return text

def save_text_to_file(text, filename):
    with open(Path.joinpath(Path('data'), filename), 'w', encoding='utf-8') as file:
        file.write(text)

def main():
    url = 'https://openai.com/policies'
    
    # Get all the links from the webpage
    links = get_links(url, prefix='/policies')

    # Fetch the text from each page and save it to a file
    for link in links:
        page_text = fetch_page_text(link)
        filename = f'{filename_from_url(link)}.txt'
        save_text_to_file(page_text, filename)
        print(f'Saved {filename}')

if __name__ == '__main__':
    main()
