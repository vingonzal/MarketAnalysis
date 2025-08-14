import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# # Phase 1/ Milstone 2
#
# #function that takes a url as the argument and extracts specified data from a single product page
# def getSingleBookData(url):
#     page = requests.get(url)
#     # Get the URL of the current page
#     product_page_url = page.url
#     # create soup object
#     soup = BeautifulSoup(page.content, 'html.parser')
#     # find elements (title, category, description) using selectors
#     book_title = soup.select_one('#content_inner > article > div.row > div.col-sm-6.product_main > h1').text
#     book_category = soup.select_one('#default > div > div > ul > li:nth-child(3) > a').text
#     product_description = soup.select_one('#content_inner > article > p').text
#     #loop through page table to find elements
#     table_elements = soup.find_all('td')
#     data = ""
#     for td in table_elements:
#         data = td.get_text(strip=True)
#         if data == '4165285e1663650f':
#             universal_product_code = data
#         if data == '£54.23':
#             price_excluding_tax = data
#         if data == '£54.23':
#             price_including_tax = data
#         if data == 'In stock (20 available)':
#             quantity_available = data
#     # find star rating
#     find_rating = soup.find(class_="star-rating Five")
#     review_rating = find_rating.get('class')[1]
#     # image url
#     main_image = soup.find('img')
#     if main_image:
#         image_url = main_image["src"]
        
#     #return all elements
#     return product_page_url, universal_product_code, book_title, price_including_tax, price_excluding_tax, quantity_available, product_description, book_category, review_rating, image_url

# #store elements in bookData tuple
# bookData = getSingleBookData('https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html')

# column_headings = ['product_page_url', 'universal_product_code', 'book_title', 'price_including_tax', 'price_excluding_tax', 'quantity_available', 'product_description', 'book_category', 'review_rating', 'image_url']

# #Open a new file to write to called ‘bookData.csv’
# with open('bookData.csv', 'w', newline='') as csvfile:
#     #Create a writer object with that file
#     writer = csv.writer(csvfile, delimiter=',')
#     writer.writerow(column_headings) #write headers on first row
#     writer.writerow(bookData) #write the scraped data on second row

#-----------------------------------------------------------------------------------------

# Phase 2 / Milestone 3 (work in progress)
# modify function so it is not specific to one book
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
    #locate table using the <table> tag
    table = soup.find('table', class_='table table-striped') 
    #loop through table to find and store headers
    table_headers = [th.text.strip() for th in table.find_all('th')]
    #test print(table_headers)
    #loop through table to find and store table data
    table_data = [td.text.strip() for td in table.find_all('td')]
    #test print(table_data)
    #declare empty dictionary
    element_dict = {}
    #fill dictionary with keys (headers) and values (table data) using loop
    for item in range(len(table_headers)):
        element_dict[table_headers[item]] = table_data[item]
    #test print(element_dict)
    #assign elements the corresponding dictionary value
    universal_product_code = element_dict['UPC']
    price_excluding_tax = element_dict['Price (excl. tax)']
    price_including_tax = element_dict['Price (incl. tax)']
    quantity_available = element_dict['Availability']
    find_rating = soup.select_one('[class^="star-rating "]')
    review_rating = find_rating.get('class')[1]
    # image url
    main_image = soup.find('img')
    if main_image:
        image_url = main_image["src"].replace("../..", "")
    base_url = 'http://books.toscrape.com/'
    # use urljoin to combine base url with relative url to get absolute URL
    image_url = urljoin(base_url, image_url)
    #return all elements
    return product_page_url, universal_product_code, book_title, price_including_tax, price_excluding_tax, quantity_available, product_description, book_category, review_rating, image_url

#test function with specified link
#getSingleBookData('https://books.toscrape.com/catalogue/unbound-how-eight-technologies-made-us-human-transformed-society-and-brought-our-world-to-the-brink_950/index.html')

# #Open a new file to write to called ‘bookData.csv’
# with open('bookData.csv', 'w', newline='') as csvfile:
#     #Create a writer object with that file
#     writer = csv.writer(csvfile, delimiter=',')
#     writer.writerow(column_headings) #write headers on first row
#     writer.writerow(bookData) #write the scraped data on second row

#visit category page and extract URLs
def singleCategoryData(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    find_urls = soup.find_all('div', attrs={'class':'image_container'})
    urls = []
    for element in find_urls:
       for link in element.find_all('a'):
            # retrieve URL (specified as local link/relative URL)
            href = link.get('href').replace("../../..", "catalogue")
            if href:
                # add relative URL to urls list
                urls.append(href)
    base_url = 'http://books.toscrape.com/'
    # use urljoin to combine base url with relative url to get absolute URL
    full_links = []
    for url in urls:
        absolute_url = urljoin(base_url, url)
        #test print
        #print(absolute_url)
        full_links.append(absolute_url)
    
    book_dict = {}
    element_headings = ['product_page_url', 'universal_product_code', 'book_title', 'price_including_tax', 'price_excluding_tax', 'quantity_available', 'product_description', 'book_category', 'review_rating', 'image_url']
    #fill dictionary with keys (headers) and values (table data) using loop
    for i in range(len(element_headings)):
        bookData = (getSingleBookData(full_links[i]))
        book_dict[element_headings[i]] = bookData[i]
    #test print
    print(book_dict)
    #use loop to call the singleCategoryData function with each link in full_links
    #....
    
    
# book category: History
singleCategoryData('https://books.toscrape.com/catalogue/category/books/history_32/index.html') 