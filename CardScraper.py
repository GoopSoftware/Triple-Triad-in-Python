import requests as rq
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin


# Function to download the image from the scraped url
def download_image(url, directory):
    # Extract the filename
    filename = os.path.join(directory, url.split('/')[-1])
    response = rq.get(url)
    # Download the file
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        # Ensures no files are missed
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {filename}")


urls = [
    "https://strategywiki.org/wiki/Final_Fantasy_VIII/Monster_Cards",
    "https://strategywiki.org/wiki/Final_Fantasy_VIII/Boss_Cards",
    "https://strategywiki.org/wiki/Final_Fantasy_VIII/GF_Cards",
    "https://strategywiki.org/wiki/Final_Fantasy_VIII/Character_Cards"
    ]



for url in urls:

    response = rq.get(url)

    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <img> tags in the html
        img_tags = soup.find_all('img', src=True)

        # Extracts .png links from the url
        png_links = []
        for img in img_tags:
            src = img['src']
            if src.endswith('.png'):
                if src.startswith('//'):
                    src = 'https:' + src
                png_links.append(src)

        # Creates a directory
        directory_name = os.path.basename(url)
        os.makedirs("downloaded_images", exist_ok=True)

        # Downloads the images
        for link in png_links:
            download_image(link, 'downloaded_images')

    else:
        print("failed to fetch the webpage")

if __name__ == '__main__':
    print('Cards have been scraped')