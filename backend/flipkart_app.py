from fastapi import FastAPI
from bs4 import BeautifulSoup
import uvicorn
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

app = FastAPI()



custom_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "DNT": "1",
    "Host": "avaldsnes.spoortz.no",
    "Pragma": "no-cache",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--user-agent={Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36}')
driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(90)


def set_headers(url: str):
    driver.get(url)
    driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {'headers': custom_headers})

def scrape_products(search: str, page_num: str):
    title = []
    description = []
    imgUrl = []
    price = []
    review_in_stars = []
    total_ratings = []
    cut_price = []
    cut_price_off = []
    product_data = []
    set_headers(url = f"https://www.flipkart.com/search?q={search}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={page_num}")
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    box = soup.find("div", "DOjaWF gdgoEp")

    if box:
        # Each page products title
        # Electronics
        titles_1 = box.find_all("div", "KzDlHZ")
        if titles_1:
            for title_tag in titles_1:
                title.append(title_tag.text.strip())
        # Clothes
        titles_2 = box.find_all("a", "WKTcLC")
        if titles_2:
            for title_tag in titles_2:
                title.append(title_tag["title"].strip())
        # Furniture
        titles_3 = box.find_all("a", "wjcEIp")
        if titles_3:
            for title_tag in titles_3:
                title.append(title_tag["title"].strip())
        
        # Each product description
        # Electronics
        descriptions_1 = box.find_all("div", "_6NESgJ")
        # Furniture
        descriptions_2 = box.find_all("div", "NqpwHC")
        # Clothes
        descriptions_3 = box.find_all("div", "yiggsN O5Fpg8")
        if descriptions_1:
            for i in range(len(title)):
                if i < len(descriptions_1):
                    div_tag = descriptions_1[i]
                    ul_tag = div_tag.find("ul", "G4BRas")
                    if ul_tag:
                        lis = ul_tag.find_all("li", "J+igdf")
                        description_text = ' '.join(li.text.strip() for li in lis)
                        description.append(description_text)
                    else:
                        description.append("")
                else:
                    description.append("")
        if descriptions_2:
            for i in range(len(title)):
                if i < len(descriptions_2):
                    description.append(descriptions_2[i].text.strip())
                else:
                    description.append("")
        if descriptions_3:
            for i in range(len(title)):
                if i < len(descriptions_3):
                    description.append(descriptions_3[i].text.strip())
                else:
                    description.append("")
        
        # Each product price
        # electronics
        prices_1 = box.find_all("div", "Nx9bqj _4b5DiR")
        if prices_1:
            for i in range(len(title)):
                if i < len(prices_1):
                    price.append(prices_1[i].text.strip())
                else:
                    price.append("")
        # Clothes and Furniture
        prices_2 = box.find_all("div", "Nx9bqj")
        if prices_2:
            for i in range(len(title)):
                if i < len(prices_2):
                    price.append(prices_2[i].text.strip())
                else:
                    price.append("")

        # Each product review in stars
        # Electronics
        stars = box.find_all("div", "XQDdHH")
        for i in range(len(title)):
            if i < len(stars):
                review_in_stars.append(stars[i].text.strip())
            else:
                review_in_stars.append("")
        # Furniture

        # Each product cut price
        # Electronics
        cut_prices_1 = box.find_all("div", "yRaY8j ZYYwLA")
        if cut_prices_1:
            for i in range(len(title)):
                if i < len(cut_prices_1):
                    cut_price.append(cut_prices_1[i].text.strip())
                else:
                    cut_price.append("")
        # Furniture and Clothes
        cut_prices_2 = box.find_all("div", "yRaY8j")
        if cut_prices_2:
            for i in range(len(title)):
                if i < len(cut_prices_2):
                    cut_price.append(cut_prices_2[i].text.strip())
                else:
                    cut_price.append("")
        
        # Each product cut price off
        cut_price_offs_1 = box.find_all("div", "UkUFwK")
        if cut_price_offs_1:
            for i in range(len(title)):
                if i < len(cut_price_offs_1):
                    cut_price_off.append(cut_price_offs_1[i].text.strip())
                else:
                    cut_price_off.append("")

        # Each product total ratings
        ratings = box.find_all("span", "Wphh3N")
        for i in range(len(title)):
            if i < len(ratings):
                s = ratings[i].text.strip().replace("\xa0", "").replace("&", " & ").replace("(", "").replace(")", "")
                total_ratings.append(s)
            else:
                total_ratings.append("")

        # Each product image url
        imgUrls_1 = box.find_all("img", "DByuf4")
        if imgUrls_1:
            for i in imgUrls_1:
                s = i['src']
                imgUrl.append(s)
        imgUrls_2 = box.find_all("img", "_53J4C-")
        if imgUrls_2:
            for i in imgUrls_2:
                s = i['src']
                imgUrl.append(s)

        for i in range(len(title)):
            product = {
                "title": title[i],
                "description": description[i],
                "img_url": imgUrl[i] if i < len(imgUrl) else "",
                "price": price[i],
                "review_in_stars": review_in_stars[i],
                "total_ratings": total_ratings[i],
                "cut_price": cut_price[i],
                "cut_price_off": cut_price_off[i]
            }
            product_data.append(product)
        
        if(len(product_data) != 0):
            return product_data
        else:
            error = {
                "error": "Internal Error Occured! Try Again"
            }
            return error
    else:
        error = {
            "error": "Internal Error Occured! Try Again"
        }
        return error
    driver.quit()

def search_functionality(search: str):
    return scrape_products(search, 1)

@app.get("/products/{search}/{page_num}")
async def get_products(search: str, page_num: str):
    result = scrape_products(search, page_num)
    return result

@app.post("/products/{search}")
async def search_products(search: str):
    return search_functionality(search)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)