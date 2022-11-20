import asyncio
import random
from typing import Dict, List, Tuple

import aiohttp
import cssutils
from bs4 import BeautifulSoup


class VKRandomPhoto:
    def __init__(self, url: str):
        self.url = url
        self.header = (
            "Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"
        )
        self.loop = asyncio.get_event_loop()
        self.photo_list = []

    async def get_page(self) -> Tuple[str, str]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.url, headers={"User-Agent": self.header}
            ) as response:
                response.raise_for_status()
                content = await response.read()
                content = str(content)
                return content, response.headers["CONTENT-TYPE"]

    async def get_photo_list(self):
        result = []
        res, _ = await self.get_page()

        soup: BeautifulSoup = BeautifulSoup(res, "lxml")
        photos_link: List = soup.body.select(".photos_row")

        for link in photos_link:
            parse_link: BeautifulSoup = BeautifulSoup(str(link), "lxml")
            div_style = parse_link.find("div")["style"]
            style = cssutils.parseStyle(div_style)
            url = style["background-image"]
            url_thumbs = url[4:-1]
            url_photo = "https://vk.com" + parse_link.find("a", href=True)["href"]

            dict_photo: Dict = {url_photo: url_thumbs}
            result.append(dict_photo)

        return result

    def get_random_photo(self, count: int) -> List[Dict]:
        result: List = []
        try:
            photo_list_url: List = self.loop.run_until_complete(self.get_photo_list())
            result = random.sample(photo_list_url, count)
        finally:
            self.loop.close()
            return result
