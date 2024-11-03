#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 23:17:06 2024

@author: luoshanni
"""

import requests
from bs4 import BeautifulSoup
import os

def main():
    print("Welcome to SUBS LIKE SCRIPTS")
    title_url = input("Enter the URL of the script: ").strip()

    # Validate the URL
    if not title_url.startswith('https://subslikescript.com/'):
        print("Invalid URL. Please enter a valid subslikescript.com URL.")
        return None

    # Fetch the title page
    response = requests.get(title_url)
    if response.status_code != 200:
        print("Error fetching title page")
        return None  # Return None if error

    soup = BeautifulSoup(response.content, 'html.parser')
    h1 = soup.find('h1')
    full_title = h1.get_text() if h1 else "No title found"

    # Find and format the transcript, replacing <br> tags with newline characters
    transcript_div = soup.find('div', class_='full-script')
    if transcript_div:
        # Replace <br> tags with newline characters
        for br in transcript_div.find_all('br'):
            br.replace_with('\n')
        transcript = transcript_div.get_text()
    else:
        transcript = "No transcript found"

    # Ensure the csv folder exists
    if not os.path.exists('csv'):
        os.makedirs('csv')

    # Clean the filename to remove illegal characters
    safe_title = "".join(c for c in full_title if c.isalnum() or c in " ._-")
    filename = f"{safe_title}.txt"

    # Save the file inside the 'csv' folder
    file_path = os.path.join('csv', filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_title + "\n\n")
        f.write(transcript)

    print(f"Transcript saved to {file_path}")

    return file_path, full_title

if __name__ == "__main__":
    main()