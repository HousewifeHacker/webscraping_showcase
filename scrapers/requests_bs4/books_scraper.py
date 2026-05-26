# This script scrapes the travel books category from "Books to Scrape" website 
# and saves the HTML content to a file, then extracts book titles, prices, and 
# star ratings, and saves the data to a CSV file.

# standard library imports
import csv

# third-party imports
import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# save the response content to a file
with open('books.html', 'w', encoding='utf-8') as file:
    file.write(response.text)

print("HTML downloaded successfully.")

soup = BeautifulSoup(response.text, 'html.parser')

# Extract book titles and prices
books_data = []
books = soup.select('.product_pod')

for book in books:
    # example Book Title: 
    # <a href="../../../full-moon-over-noahs-ark-an-odyssey-to-mount-ararat-and-beyond_811/index.html" title="Full Moon over Noah’s Ark: An Odyssey to Mount Ararat and Beyond">
    #   Full Moon over Noah’s ...
    # </a>
    # book's full title is in 'title' attribute, shortened in displayed text
    title = book.select_one('h3 a')['title']
    price_text = book.select_one('.price_color').text
    price = float(price_text.replace("Â£", "").strip())
    star_class_name = book.select_one('.star-rating')['class'][1]
    # star_class_name is a list like ['star-rating', 'Three'], we want the second element which indicates the rating
    star_int = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }.get(star_class_name, 0)  # default to 0 if not found
    books_data.append({
        'title': title,
        'price': price,
        'star_rating': star_int
    })

# Save the extracted data to a CSV file
with open('books.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(
        csvfile,
        fieldnames=['title', 'price', 'star_rating']
    )
    writer.writeheader()
    writer.writerows(books_data)
