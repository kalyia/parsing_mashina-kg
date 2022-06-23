import requests
from bs4 import BeautifulSoup
from urllib import response
import csv

url = "https://www.mashina.kg/specsearch/all/"

def get_html(url):
    response = requests.get(url)
    return response.text

def get_soup(html):
    soup = BeautifulSoup(html, "lxml")
    return soup

def get_last_page(soup):
    pagination = soup.find("ul", class_ = "pagination").find_all("a", class_="page-link")
    item = pagination[-4].text
    return int(item)

def get_product_cards(soup):
    product_list = soup.find("div", class_="table-view-list")
    products = product_list.find_all("div", class_="list-item")
    return products

def get_data_from_cards(products):
    for product in products:
        try:
            title = product.find("h2", class_="name").text.strip()
        except:
            title = "-"
        try:
            year = product.find("p", class_="year-miles").text.strip()
            body = product.find("p", class_="body-type").text.strip()
            vol = product.find("p", class_="volume").text.strip()
            desc = year + "," + body + "," +vol
        except:
            year = "-"
            body = "-"
            vol = "-"
            desc = "-"
        try:
            price = product.find("strong").text.strip()
        except:
            price = "-"
        try:
            image = product.find('div', class_="thumb-item-carousel").find("img").get("data-src")
        except:
            image = "-"
        data = {"title": title, "desc": desc, "price": price, "image": image}

        write_to_csv(data)

def write_to_csv(data):
    with open("mashina_specsearch.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow((data["title"], data["desc"], data["price"], data["image"]))

def main():
    html = get_html(url)
    soup = get_soup(html)
    get_last_page_num = get_last_page(soup)
    for page in range(1, get_last_page_num+1):
        page_url = url + "?type=11&page=" + str (page)
        html = get_html(page_url)
        soup = get_soup(html)
        cards = get_product_cards(soup)
        get_data_from_cards(cards)

main()