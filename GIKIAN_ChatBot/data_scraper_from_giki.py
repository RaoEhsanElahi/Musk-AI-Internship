# -*- coding: utf-8 -*-
"""Data_Scraper_from_giki.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZvMagCD_Qkbrbr-RukMhNO7H3f1QL527

#https://python.langchain.com/docs/integrations/document_loaders/web_base
"""

!pip -q install langchain bitsandbytes

"""#Loading Single webpage"""

from langchain.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://giki.edu.pk/admissions/sitemap.xlm")

data = loader.load()

data

"""#ANOTHER method"""

!pip install beautifulsoup4 requests

import requests
from bs4 import BeautifulSoup

def get_sitemap_urls(sitemap_url):
    response = requests.get(sitemap_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        urls = [loc.text.strip() for loc in soup.find_all('loc')]
        return urls
    else:
        print(f"Failed to fetch the sitemap. Status code: {response.status_code}")
        return []

def scrape_text_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text().strip()
        return text
    else:
        print(f"Failed to scrape URL: {url}. Status code: {response.status_code}")
        return None

def main():
    sitemap_url = 'https://giki.edu.pk/sitemap.xml'  # Replace with the actual sitemap URL
    urls = get_sitemap_urls(sitemap_url)
    scraped_texts = []

    for url in urls:
      text = scrape_text_from_url(url)
      if text:
        scraped_texts.append(text)
        print(text)
    # Do something with the scraped_texts, like saving to a file or processing further.
    # For example, you can save it to a text file:


    with open('scr.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(scraped_texts))



if __name__ == "__main__":
    main()

"""##Removing Timestamps and empty spaces between lines.

###Removing spaces/blanks
"""

def clean_urls(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    cleaned_lines = [line.strip() for line in lines if line.strip() and not line.strip().isdigit()]

    with open(output_file, 'w') as file:
        file.write('\n'.join(cleaned_lines))

if __name__ == "__main__":
    input_file_name = "scr.txt"  # Replace with the name of your input file
    output_file_name = "clean.txt"  # Replace with the name of the output file

    clean_urls(input_file_name, output_file_name)

"""##Removing .png etc"""

#NEW FUN()
import re

def remove_timestamps(text):
    # Define the pattern for matching timestamps (in the format "YYYY-MM-DDTHH:MM:SS+00:00")
    pattern = r'\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}\b'
    return re.sub(pattern, '', text)

def get_cleaned_urls(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    cleaned_lines = [remove_timestamps(line.strip()) for line in lines if line.strip() and not line.strip().isdigit()]
    return cleaned_lines

def remove_image_links(url_list):
    # Define the pattern for matching image links based on common image extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']
    image_pattern = r'\b(?:https?://\S+)(?:{})\b'.format('|'.join(image_extensions))
    return [url for url in url_list if not re.search(image_pattern, url, re.IGNORECASE)]

def clean_urls(output_file):
    with open(output_file, 'w') as file:
        file.write('\n'.join(cleaned_urls))

if __name__ == "__main__":
    input_file_name = "urls.txt"  # Replace with the name of your input file

    cleaned_urls_list = get_cleaned_urls(input_file_name)

    # Remove image links from the list
    cleaned_urls = remove_image_links(cleaned_urls_list)
    output_file_name = "url.txt"  # Replace with the name of the output file
    # Print the cleaned URLs
    for url in cleaned_urls:
        print(url)

# Define an empty list to store the data from each iteration
all_docs = []

for url in cleaned_urls:
    loader = WebBaseLoader(url)
    doc = loader.load()

    # Append the new data to the list
    all_docs.append(doc)

import requests

# Define an empty list to store the downloaded data from each URL
all_data = []

for url in cleaned_urls:
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Append the content to the list
        all_data.append(response.text)
    else:
        print(f"Failed to download data from {url}. Status code: {response.status_code}")

# Now all_data will contain the downloaded content from each URL

for i in all_data:
  with open('data.txt', 'w', encoding='utf-8') as file:
    file.write("".join())

# Assuming you have a list named 'data_list' containing the data you want to transfer

# Specify the file name
file_name = "data.txt"

# Open the file in write mode
with open(file_name, "w") as file:
    # Iterate through the list and write each item to the file
    for item in all_data:
        file.write(str(item) + "\n")

"""###Removing time-stamps"""

import re

def remove_timestamps(text):
    # Define the pattern for matching timestamps (in the format "YYYY-MM-DDTHH:MM:SS+00:00")
    pattern = r'\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}\b'
    return re.sub(pattern, '', text)

def clean_urls(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    cleaned_lines = [remove_timestamps(line.strip()) for line in lines if line.strip() and not line.strip().isdigit()]

    with open(output_file, 'w') as file:
        file.write('\n'.join(cleaned_lines))

if __name__ == "__main__":
    input_file_name = "clean.txt"  # Replace with the name of your input file
    output_file_name = "urls.txt"  # Replace with the name of the output file

    clean_urls(input_file_name, output_file_name)

"""#Loading multiple webpages"""

loader = WebBaseLoader(list(url))
docs = loader.load()
docs

"""#Load multiple urls concurrently"""

!pip install nest_asyncio

# fixes a bug with asyncio and jupyter
import nest_asyncio

nest_asyncio.apply()

loader = WebBaseLoader(["https://giki.edu.pk"])
loader.requests_per_second = 1
docs = loader.aload()
docs



"""#load txt to variable to use"""

def read_urls_from_file(file_path):
    urls_list = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Assuming each line contains a single URL
                url = line.strip()  # Remove any leading/trailing whitespace or newline characters
                urls_list.append(url)
    except FileNotFoundError:
        print("Error: The file was not found.")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")

    return urls_list

# Replace 'file_path.txt' with the actual path of your file containing URLs.
file_path = 'clean.txt'
urls_list = read_urls_from_file(file_path)

# Print the list of URLs
print(urls_list)

import requests
from bs4 import BeautifulSoup

def scrape_urls_to_file(urls_list, output_file):
    try:
        with open(output_file, "w") as f:
            for url in urls_list:
                res = requests.get(url)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, "html.parser")
                    # Here you need to identify the specific HTML elements that contain the data you want
                    # and extract their content accordingly.
                    data_elements = soup.find_all("div", class_="your-specific-class-name")
                    f.write(f"URL: {url}\n")
                    for element in data_elements:
                        f.write(f"{element.get_text()}\n")
                    f.write("\n")
                else:
                    print(f"Error: Unable to access URL {url}. Status Code: {res.status_code}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")

# Assuming you already have the urls_list from the previous code snippet
# Replace 'urls_list' with the actual list of URLs you want to scrape.
# Replace 'output_file.txt' with the name of the file where you want to save the data.
scrape_urls_to_file(urls_list, "output_file.txt")

import requests

def download_urls_to_file(urls_list, output_file):
    try:
        with open(output_file, "w") as f:
            for url in urls_list:
                res = requests.get(url)
                if res.status_code == 200:
                    f.write(f"URL: {url}\n")
                    f.write(f"{res.text}\n\n")
                else:
                    print(f"Error: Unable to access URL {url}. Status Code: {res.status_code}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")

# Assuming you already have the urls_list from the previous code snippet
# Replace 'urls_list' with the actual list of URLs you want to download.
# Replace 'output_file.txt' with the name of the file where you want to save the data.
download_urls_to_file(urls_list, "output_file.txt")