import requests
from bs4 import BeautifulSoup as bs
import csv
class Scrapper:
    BASE_URL = None
    def __init__(self) -> None:
        pass

    def get_page_url(self, page_no):
        PAGE_URL = f"https://www.amazon.in/s?k=bags&page={page_no}&qid=1692620898&sprefix=%2Caps%2C415&ref=sr_pg_1"
        return PAGE_URL
    
    def run_scrapper(self):
        headers = self.get_amazon_headers()
        products = list()
        for count in range(1,21):
            page_url = self.get_page_url(count)
            response = requests.get(page_url, headers=headers)

            if response.status_code == 200:
                print(f"Starting scrapping data for page: {count}")
                web_page = bs(response.content, "html.parser")
                product_divs = web_page.find_all("div", attrs={"class":"sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 sg-col-12-of-24 s-list-col-right"})
                for product_div in product_divs:
                    product_url = ""
                    product_title = ""
                    price = ""
                    rating = ""
                    reviews = ""
                    try:
                        product_url = "https://www.amazon.in/"+product_div.find("a", attrs={"class":"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"}).get("href")
                    except:
                        pass
                    try:
                        product_title = product_div.find("span", attrs={"class":"a-size-medium a-color-base a-text-normal"}).text
                    except:
                        pass
                    try:
                        price = product_div.find("span", attrs={"class":"a-price"}).find("span", attrs={"class":"a-offscreen"}).text
                    except:
                        pass
                    try:
                        rating = product_div.find("span", attrs={"class":"a-icon-alt"}).text
                    except:
                        pass
                    try:
                        reviews = product_div.find("span", attrs={"class":"a-size-base s-underline-text"}).text
                    except:
                        pass
                    
                    response = requests.get(product_url, headers=headers)
                    web_page = bs(response.content,"html.parser")
                    
                    description_list = list()
                    try:
                        description_list = [i.text for i in web_page.find("div", attrs = {"id":"feature-bullets"}).find_all("span")]
                    except:
                        pass

                    product_description = ""
                    try:
                        product_description = web_page.find("div", attrs = {"id":"productDescription"}).find("p").find("span").text
                    except:
                        pass
                    
                    detailBullets = ""
                    try:
                        detailBullets = web_page.find("div", attrs = {"id":"detailBullets_feature_div"}).find("ul").find_all("li")
                    except:
                        pass
                    
                    description = ""
                    for j in description_list:
                        description += j + "\n"

                    myDict = dict()
                    for items in detailBullets:
                        values = items.find("span").find_all("span", string=True)
                        myDict.update({self.remove_unicodes(values[0].text):self.remove_unicodes(values[1].text)})

                
                    product_info = [product_title, product_url, price, rating, reviews, description, product_description, myDict.get("Manufacturer"), myDict.get("ASIN")]
                    products.append(product_info)
            else:
                print(f"Got status_code {response.status_code} for page: {count}")
        print("Scrapping completed writing data into csv file........")
        self.write_data_into_csv(product_details=products)    

    def get_amazon_headers(self):
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding":"gzip, deflate, br"
        }
    
    def remove_unicodes(self, string):
        strencode = string.encode("ascii", "ignore")
        
        strdecode = strencode.decode()
        strdecode = strdecode.replace("\n","")
        strdecode = strdecode.replace(":","")
        strdecode = strdecode.strip()

        return strdecode

    def write_data_into_csv(self, product_details):
        headers = ['name', 'url', 'price', 'rating', 'reviews', 'description', 'product_description', 'Manufacturer', 'ASIN']

        with open('amazon_scrapped_data.csv', 'w', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(product_details)

        print(f"Created {len(product_details)} entries...")

if __name__ == "__main__":
    scrapper = Scrapper()
    scrapper.run_scrapper()
    print("Scrapper stopped!!!")

