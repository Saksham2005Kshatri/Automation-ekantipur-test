import asyncio
import json
from playwright.async_api import async_playwright


output_json = {"entertainment_news": []}

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        # navigate to the link and waiting for the page to fully load

        # for entertainment page
        await page.goto('https://ekantipur.com/entertainment', wait_until='load', timeout=60000)
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        await asyncio.sleep(2)
        await extracting_articles_list(page)

        # for cartoon page
        await page.goto('https://ekantipur.com/cartoon', timeout=120000)
        # await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        # await asyncio.sleep(2)
        await extracting_cartoon(page)
        await browser.close()
    
    # Write output to JSON file
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(output_json, f, ensure_ascii=False, indent=2)
    print("File has been created")

async def extracting_articles_list(page):
    article_list = await page.query_selector_all('article.normal') 
    category = await page.query_selector('div.catName')
    if category:
        category = await category.inner_text()
    # for extracting the top 5 articles

    # if there are fewer than 5 articles
    count = min(len(article_list), 5)

    for article in range(count):
        print(f"Article no {article}")
        title = await article_list[article].query_selector('h2')
        if title:
            title = await title.inner_text()
        image_element = await article_list[article].query_selector('div.image  img')
        
        # Extract the image URL string
        image_url = None
        if image_element:
            image_url = await image_element.get_attribute('src') or await image_element.get_attribute('data-src')
        
        author = await article_list[article].query_selector('div.author > a')
        if author:
            author = await author.inner_text()
        
        print(f"Title: {title}, Image URL: {image_url}, Author: {author}, Category: {category}")

        article_dict = {
            "title": title, 
            "image_url": image_url, 
            "category": category,
            "author": author  
        }

        output_json['entertainment_news'].append(article_dict)

async def extracting_cartoon(page):
    cartoons = await page.query_selector_all('div.catroon-wrap')
    for cartoon in range(1):
        image_element = await cartoons[cartoon].query_selector('img')
        if image_element:
            image_url = await image_element.get_attribute('src') or await image_element.get_attribute('data-src')
        title_author = await cartoons[cartoon].query_selector('div.cartoon-author p')
        title = (await title_author.inner_text()).split('-')[0].strip()
        author = (await title_author.inner_text()).split('-')[1].strip()
    print(f"TITLE: {title}, AUTHOR: {author}, IMAGEURL: {image_url}")
    output_json['cartoon_of_the_day'] = {
        "title": title, 
        "image_url": image_url,
        "author": author
    }

    



if __name__ == "__main__":
    asyncio.run(main())