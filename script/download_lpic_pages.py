import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# URL of the archives page
url = "https://linux1st.com/archives.html"

# Directory to save downloaded pages
download_dir = os.path.join(os.getcwd(), 'downloads')
os.makedirs(download_dir, exist_ok=True)

# Fetch the page
response = requests.get(url)
response.raise_for_status()

# Parse the HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Find all links
links = soup.find_all('a', href=True)

# Filter links that are internal and not the archives page itself
internal_links = [urljoin(url, link['href']) for link in links if urljoin(url, link['href']).startswith('https://linux1st.com/') and urljoin(url, link['href']) != url]

# Remove duplicates and exclude home, support, tags
exclude = ['https://linux1st.com/', 'https://linux1st.com/support', 'https://linux1st.com/tags.html']
lpic_links = [link for link in set(internal_links) if link not in exclude]

# Download each page
for link in lpic_links:
    try:
        page_response = requests.get(link)
        page_response.raise_for_status()
        # Get filename from URL
        filename = link.split('/')[-1]
        filepath = os.path.join(download_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(page_response.text)
        print(f"Downloaded {link} to {filepath}")
    except Exception as e:
        print(f"Failed to download {link}: {e}")