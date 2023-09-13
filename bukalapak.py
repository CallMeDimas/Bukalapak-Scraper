import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import csv
import os

banner = """
=======================================================
  ___ _   _ _  __   _   _      _   ___  _   _  __
 | _ ) | | | |/ /  /_\ | |    /_\ | _ \/_\ | |/ /
 | _ \ |_| | ' <  / _ \| |__ / _ \|  _/ _ \| ' < 
 |___/\___/|_|\_\/_/ \_\____/_/ \_\_|/_/ \_\_|\_\ 

=======================================================
  Versi: 1.1.0
  Judul: Bot Scraper Toko Bukalapak
  Tentang: Bot Scraping Data Dari Bukalapak.com
  Author : https://github.com/CallMeDimas/
  Website: https://CallMeDimas.github.io 
=======================================================
  Q: Apa Yang Bot Ini Bisa Dapatkan?...
  A: (Nama Toko, Rating Toko, Total Feedback, Tanggal Bergabung, Nama Barang, Harga Barang, Link Barang)
=======================================================
  Versi Custom/Lengkap nya Bisa Email ke CallMeDimas@proton.me
=======================================================
"""

class BukalapakScraper:
    def __init__(self, url):
        self.url = url
        self.user_agent = UserAgent(min_percentage=1.3)
        self.headers = {"User-Agent": self.user_agent.random}

    def get_response(self, url):
        return requests.get(url, headers=self.headers)

    def get_profile_data(self, response):
        soup = BeautifulSoup(response.content, 'html.parser')
        return {
            "Nama Toko": soup.find("h1", "u-txt--fair u-txt--bold merchant-page__store-name ut-store-name").text.strip(),
            "Pembeli Puas": soup.find_all('td', {'class': 'ut-feedback-percentage'})[1].text.strip(),
            "Total Feedback": soup.find("a", "c-link--quaternary").text.strip(),
            "Tanggal Bergabung": soup.find_all("td", {'class': 'ut-join'})[1].text.strip()
        }

    def get_items_data(self, response):
        soup = BeautifulSoup(response.content, 'html.parser')
        items = []
        self.parse_items(response, items)

        for link in soup.find_all("a", "c-ghostblock-pagination__link"):
            response_item = self.get_response(self.url + link.get('href'))
            if response_item.status_code == 200:
                self.parse_items(response_item, items)
        
        return items

    def parse_items(self, response_item, items):
        soup = BeautifulSoup(response_item.content, 'html.parser')
        for nama, link, harga in zip(
            soup.find_all('a', {'class': 'c-product-card__name js-tracker-product-link u-mrgn-top--2 u-mrgn-bottom--1 c-product-card__ellipsis c-product-card__ellipsis-2'}), 
            soup.find_all("div", "c-card__head revamp-c-card--head"),
            soup.find_all("span", {"class": "u-display-block u-fg--red-brand u-txt--bold"})):
            a_tag = link.find('a')
            if a_tag is not None:
                items.append({
                    "[INFO] - Nama Barang": nama.text.strip(), 
                    "[INFO] - Link Barang": a_tag.get('href'),
                    "[INFO] - Harga Barang": harga.text.strip()
                })


    def write_to_csv(self, profile_data, items_data):
        with open(f'{nama_file}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for key, value in profile_data.items():
                writer.writerow([key, value])
            print(f"  [INFO] - Profile data Ditulis Ke", {nama_file},".csv")

            writer.writerow(["Nama Barang", "Link Barang", "Harga Barang"])
            for item in items_data:
                writer.writerow(item.values())
        print("  [INFO] - List item Ditulis Ke",{nama_file},".csv")

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)

if __name__ == "__main__":
    print_banner()
    buka_url = input("  [USER] - Link Toko Bukalapak: ")
    nama_file = input("  [INFO] - Nama Output File: ")
    scraper = BukalapakScraper(buka_url)
    response = scraper.get_response(buka_url)

    if response.status_code == 200:
        profile_data = scraper.get_profile_data(response)
        print("  [INFO] - Profile Data:", profile_data)
        
        items_data = scraper.get_items_data(response)
        print("  [INFO] - Items Data:", "{'Nama Barang': 'Success', 'Link Barang': 'Success', 'Harga Barang': 'Success'}")

        scraper.write_to_csv(profile_data, items_data)

