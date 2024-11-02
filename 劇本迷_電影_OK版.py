#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 20:00:50 2024

@author: luoshanni
"""

import requests
from bs4 import BeautifulSoup
import os

def main():
    print("Welcome to SUBTITLES LIKE SCRIPTS")
    base_url = "https://subslikescript.com"

    # Default to movies category
    category = 'movies'

    # Let users enter a title name, strip whitespace
    title_input = input("Enter the movie title: ").strip()
    first_letter = title_input[0].lower()

    # Construct the URL for the first letter
    search_url = f"{base_url}/{category}_letter-{first_letter.upper()}"

    # Initialize variables for searching
    found_titles = []
    page = 1

    while True:
        print(f"Searching page {page} of letter '{first_letter.upper()}'...")
        response = requests.get(f"{search_url}?page={page}")
        if response.status_code != 200:
            print("Error fetching page")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find('article', class_='main-article')
        if not articles:
            print("No articles found")
            break

        title_links = articles.find_all('a', href=True, title=True)

        # Loop through the titles and look for partial matches
        for idx, link in enumerate(title_links):
            title_text = link.get_text(strip=True).lower()
            if title_input.lower() in title_text:
                # Found a partial match
                # Collect this and the next up to 10 titles
                for i in range(idx, min(idx + 10, len(title_links))):
                    matching_link = title_links[i]
                    matching_title = matching_link.get_text(strip=True)
                    found_titles.append((matching_title, matching_link['href']))
                break  # Break after collecting titles
        if found_titles:
            break

        # Check if there is a next page
        pagination = soup.find('ul', class_='pagination')
        if pagination:
            next_page = pagination.find('a', string=str(page + 1))
            if next_page:
                page += 1
            else:
                break
        else:
            break

    if not found_titles:
        print("Title not found.")
        return None  # Return None if not found

    # Present the found titles to the user for selection
    print("Found the following titles:")
    for idx, (title, _) in enumerate(found_titles):
        print(f"{idx + 1}. {title}")

    # Let the user select the desired title
    while True:
        choice = input("Enter the number of the desired title: ")
        if choice.isdigit() and 1 <= int(choice) <= len(found_titles):
            choice = int(choice) - 1
            break
        else:
            print("Invalid choice. Please enter a valid number.")

    selected_title, title_href = found_titles[choice]
    title_url = base_url + title_href

    # Enter the title page, find title and transcript
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

    # Export title and transcript as txt file in csv folder
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

    # Return the filename for use outside the function
    return file_path, full_title

if __name__ == "__main__":
    result = main()