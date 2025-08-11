import requests
from bs4 import BeautifulSoup
import csv

# function that takes a url as the argument and extracts data from a single product page
def getSingleBookData(url):
    page = requests.get(url)
    # Get the URL of the current page
    product_page_url = page.url
    # create soup object
    soup = BeautifulSoup(page.content, 'html.parser')
    # find elements (title, category, description) using selectors
    book_title = soup.select_one('#content_inner > article > div.row > div.col-sm-6.product_main > h1').text
    book_category = soup.select_one('#default > div > div > ul > li:nth-child(3) > a').text
    product_description = soup.select_one('#content_inner > article > p').text
    #loop through page table to find elements
    table_elements = soup.find_all('td')
    data = ""
    for td in table_elements:
        data = td.get_text(strip=True)
        if data == '4165285e1663650f':
            universal_product_code = data
        if data == '£54.23':
            price_excluding_tax = data
        if data == '£54.23':
            price_including_tax = data
        if data == 'In stock (20 available)':
            quantity_available = data
    # find star rating
    find_rating = soup.find(class_="star-rating Five")
    review_rating = find_rating.get('class')[1]
    # image url
    main_image = soup.find('img')
    if main_image:
        image_url = main_image["src"]
        
    #return all elements
    return product_page_url, universal_product_code, book_title, price_including_tax, price_excluding_tax, quantity_available, product_description, book_category, review_rating, image_url

#store elements in bookData tuple
bookData = getSingleBookData('https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html')

column_headings = ['product_page_url', 'universal_product_code', 'book_title', 'price_including_tax', 'price_excluding_tax', 'quantity_available', 'product_description', 'book_category', 'review_rating', 'image_url']

# #Open a new file to write to called ‘bookData.csv’
with open('bookData.csv', 'w', newline='') as csvfile:
    #Create a writer object with that file
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(column_headings) #write headers on first row
    writer.writerow(bookData) #write the scraped data on second row
   
  