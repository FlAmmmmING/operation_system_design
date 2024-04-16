# 异步爬虫

import asyncio
import time

import aiohttp

# 要爬取的网页集合
urls = [
    f"https://www.cnblogs.com/sitehome/p/{page}"
    for page in range(1, 101)
]


# 爬虫
def craw(url):
    r = requests.get(url)
    return r.text


# 解析
# 获取网页的每一个文章标题
def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_="post-item-title")
    return [(link['href'], link.get_text()) for link in links]


# 异步IO
async def async_craw(url):
    print("craw url:", url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            result = await resp.text()
            print(f"craw url {url}, result: {len(result)}")

loop = asyncio.get_event_loop()

tasks = [
    loop.create_task(async_craw(url))
    for url in urls]

start = time.time()
loop.run_until_complete(asyncio.wait(tasks))
end = time.time()

print("consume time:", end - start)