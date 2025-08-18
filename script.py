import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# Phase 1/ Milstone 2
#---
# Pick any single product page (i.e., a single book) on Books to Scrape, and write a
# Python script that visits this page and extracts the following information:
# ● product_page_url
# ● universal_ product_code (upc)
# ● book_title
# ● price_including_tax
# ● price_excluding_tax
# ● quantity_available
# ● product_description
# ● category
# ● review_rating
# ● image_url
# Write the data to a CSV file using the above fields as column headings
#---
# function that takes a url as the argument and extracts specified data from a single product page
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

# Phase 2 / Milestone 3
#---
# Now that you have obtained the information for one book, you should get all of
# the necessary information for one category.
# Pick any book category on Books to Scrape, and write a Python script that visits
# this category page and extracts the product page URL for each book in the
# category.
# Then combine this script with the work you have completed in Phase 1 to extract
# the product data for each book in your category and write the data to a single
# CSV file.
# Note: some category pages have more than 20 books listed, spread across
# different pages. This is referred to as pagination. Your application should be able
# to handle this scenario automatically
#---
# modify function so it is not specific to one book
# def getSingleBookData(url):
#     page = requests.get(url)
#     # Get the URL of the current page
#     product_page_url = page.url
#     # create soup object
#     soup = BeautifulSoup(page.content, 'html.parser')
#     # find elements (title, category, description) using selectors
#     book_title = soup.select_one('#content_inner > article > div.row > div.col-sm-6.product_main > h1').text
#     book_category = soup.select_one('#default > div > div > ul > li:nth-child(3) > a').text
#     if soup.select_one('#content_inner > article > p') == None:
#         product_description = 'None'
#     else:
#         product_description = soup.select_one('#content_inner > article > p').text
#     #locate table using the <table> tag
#     table = soup.find('table', class_='table table-striped') 
#     #loop through table to find and store headers
#     table_headers = [th.text.strip() for th in table.find_all('th')]
#     #test print(table_headers)
#     #loop through table to find and store table data
#     table_data = [td.text.strip() for td in table.find_all('td')]
#     #test print(table_data)
#     #declare empty dictionary
#     element_dict = {}
#     #fill dictionary with keys (headers) and values (table data) using loop
#     for item in range(len(table_headers)):
#         element_dict[table_headers[item]] = table_data[item]
#     #test print(element_dict)
#     #assign elements the corresponding dictionary value
#     universal_product_code = element_dict['UPC']
#     price_excluding_tax = element_dict['Price (excl. tax)']
#     price_including_tax = element_dict['Price (incl. tax)']
#     quantity_available = element_dict['Availability']
#     find_rating = soup.select_one('[class^="star-rating "]')
#     review_rating = find_rating.get('class')[1]
#     # image url
#     main_image = soup.find('img')
#     if main_image:
#         image_url = main_image["src"].replace("../..", "")
#     base_url = 'http://books.toscrape.com/'
#     # use urljoin to combine base url with relative url to get absolute URL
#     image_url = urljoin(base_url, image_url)
#     #return all elements
#     return product_page_url, universal_product_code, book_title, price_including_tax, price_excluding_tax, quantity_available, product_description, book_category, review_rating, image_url

# #visit category page and extract URLs
# def singleCategoryData(url):
#     page = requests.get(url)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     urls = []
#     page_num = 2
#     while True:
#         #scan for and store the book URL data represented by their image
#         find_urls = soup.find_all('div', attrs={'class':'image_container'})
        
#         for element in find_urls:
#         #loop through each <a> tag
#             for link in element.find_all('a'):
#                 # retrieve URL (specified as local link/relative URL)
#                 href = link.get('href').replace("../../..", "catalogue")
#                 if href:
#                     # add relative URL to urls list
#                     urls.append(href)
#         # evaluate if a next page exists, if not then stop while loop
#         #next_button = soup.find("li", class_="next")
#         page_button = soup.find('ul', class_='pager') 
#         #loop through table to find and store headers
#         page_list_items = [li.text.strip() for li in page_button.find_all('li')]
#         if 'next' not in page_list_items:
#             break  # No more pages
#         base_url = url.replace("index.html","")
#         next_page = f"{base_url}page-{page_num}.html"
#         page = requests.get(next_page)
#         soup = BeautifulSoup(page.content, 'html.parser')
#         page_num += 1

#     base_url = 'http://books.toscrape.com/'
#     # use urljoin to combine base url with relative url to get absolute URL
#     full_links = []
#     for url in urls:
#         absolute_url = urljoin(base_url, url)
#         #store absolute URL in full_links list
#         full_links.append(absolute_url)
    
#     # creat list of csv column headers
#     element_headings = ['product_page_url', 'universal_product_code', 'book_title', 'price_including_tax', 'price_excluding_tax', 'quantity_available', 'product_description', 'book_category', 'review_rating', 'image_url']
    
#     #Open a new file to write to called ‘bookCategoryData.csv’
#     # test 1 - ‘bookCategoryData.csv’
#     # test 2 - ‘bookCategoryData2.csv’
#     # test 3 - ‘bookCategoryData3.csv’
#     # test 4 - ‘bookCategoryData4.csv’
#     with open('bookCategoryData4.csv', 'w', encoding="utf-8", newline='') as csvfile:
#         #Create a writer object with that file
#         writer = csv.writer(csvfile, delimiter=',')
#         #write headers on first row
#         writer.writerow(element_headings) 
    
#         #use a loop to go through each link and write its data found on onto each subsequent row
#         for i in range(len(full_links)):
#             # call function for each book page and store elements in bookData tuple
#             bookData = (getSingleBookData(full_links[i]))
#             #write the scraped data for each book on each row
#             writer.writerow(bookData) 


# call this function for a book category: History (test 1, 1 page)
#singleCategoryData('https://books.toscrape.com/catalogue/category/books/history_32/index.html') 

# call this function for a book category: Historical (test 2, 2 pages)
#singleCategoryData('https://books.toscrape.com/catalogue/category/books/mystery_3/index.html') 

# call this function for a book category: Historical (test 3, multiple pages)
#singleCategoryData('https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html')

# call this function for a book category: Historical (test 4, most pages)
#singleCategoryData('https://books.toscrape.com/catalogue/category/books/default_15/index.html')

#-----------------------------------------------------------------------------------------

# Phase 3
#---
# Write a script that visits Books to Scrape, extracts all the book categories available,
# and then extracts product information for all books across all categories. You
# should write the data for each book category in a separate CSV file.
#---
def getCategories(url):
    home_page = requests.get(url)
    # create soup object
    soup = BeautifulSoup(home_page.content, 'html.parser')
    #locate navigation section with categories
    navigation_section = soup.find_all('ul', class_='nav nav-list') 
    category_urls = []    
    for element in navigation_section:
    #loop through each <a> tag
        for link in element.find_all('a'):
            # retrieve URL (specified as local link/relative URL)
            href = link.get('href')
            if href:
                # add relative URL to urls list
                category_urls.append(href)
    base_url = 'http://books.toscrape.com/'
    # use urljoin to combine base url with relative url to get absolute URL
    full_links = []
    for url in category_urls:
        absolute_url = urljoin(base_url, url)
        #store absolute URL in full_links list
        full_links.append(absolute_url)
    #test print
    print(full_links)

getCategories('http://books.toscrape.com/')