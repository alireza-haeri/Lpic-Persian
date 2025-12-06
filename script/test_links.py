import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://linux1st.com/archives.html"
response = requests.get(url)
print("Response status:", response.status_code)
soup = BeautifulSoup(response.content, 'html.parser')
print("Title:", soup.title)
links = soup.find_all('a', href=True)
print("Total links:", len(links))
for link in links[:10]:  # Print first 10
    full_href = urljoin(url, link['href'])
    print(full_href)
lpic_links = [urljoin(url, link['href']) for link in links if urljoin(url, link['href']).startswith('https://linux1st.com/') and urljoin(url, link['href']) != url]
print("Filtered links:", len(lpic_links))
print("Sample:", lpic_links[:5])