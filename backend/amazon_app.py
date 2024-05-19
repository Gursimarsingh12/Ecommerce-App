from fastapi import FastAPI, HTTPException
from autoscraper import AutoScraper

app = FastAPI()

scraper = AutoScraper()
scraper.load('amazon-search')

async def scrape_amazon(url):
    try:
        result = scraper.get_result_similar(url, group_by_alias=True)
        if not result:
            return []
        return _aggregate_result(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping error: {str(e)}")

@app.get("/products/{search_term}")
async def get_products(search_term: str):
    url = f"https://www.amazon.in/s?k={search_term}"
    results = await scrape_amazon(url)
    if not results:
        return {"message": "No products found for the search term."}
    return {"products": results}

def _aggregate_result(result):
    final_result = []
    print(list(result.values())[0])
    for i in range(len(list(result.values())[0])):
        try:
            final_result.append({alias: result[alias][i] for alias in result})
        except:
            pass
    return final_result