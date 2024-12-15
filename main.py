import requests
from bs4 import BeautifulSoup
import pandas as pd

current_page = 1

proceed = True

data = []

target_card_elem = "li"
target_card_elem_class = "col-xs-6 col-sm-4 col-md-3 col-lg-3"


while(proceed):
    print("-----------------------------")
    print("---Currently scraping page: " + str(current_page))
    print("-----------------------------")

    url = "https://books.toscrape.com/catalogue/page-"+str(current_page)+".html"

    page = requests.get(url)

    soup = BeautifulSoup(page.text,"html.parser")

    if soup.title.text == "404 Not Found":
        proceed = False
    else:
        all_books = soup.find_all(target_card_elem,class_=target_card_elem_class)

        for book in all_books:
            item = {}

            item['Title'] = book.find("img").attrs['alt']

            item['Link'] = "https://books.toscrape.com/catalogue/"+book.find("a").attrs["href"]

            item['Price'] = book.find("p", class_="price_color").text.replace("Â£","")

            item['Stock'] = book.find("p",class_="instock availability").text.strip()

            # print(item['Price']) // inner loop control point
            # print(item['Stock']) // inner loop control point

            data.append(item)


    current_page +=1
    # proceed = False // inner loop control point

# print(soup.title.text) //first control point

df = pd.DataFrame(data)
df.to_excel("books.xlsx")
df.to_csv("books.csv")

