from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List
from collections import deque
import aiohttp
import asyncio
import os
from course_table import CourseTable

# BFS crawler to find all degree programs offered by GT

class BFSCrawler:

    def __init__(self, starting_url: str):
        self.starting_url = starting_url
        self.raw_course_tables = {}

        # ensure async operations run without warning on Windows
        if os.name == "nt":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    def get_course_tables(self) -> List[CourseTable]:

        results = []
        asyncio.run(self.load_raw_course_tables())
        for program in self.raw_course_tables.keys():
            for course_table in self.raw_course_tables[program]:
                ct = CourseTable(program, course_table)
                if ct.is_valid():
                    results.append(CourseTable(program, course_table))
                
        return results

    async def load_raw_course_tables(self, timeout: int = 10) -> None:
        """
        Populate the raw course table map with a list of all of the html course tables on a program page

        Args:
            timeout (int, optional): the timeout for requests (seconds)

        """

        # initialize BFS variables
        queue = deque()
        queue.append(self.starting_url)
        visited = set()

        async with aiohttp.ClientSession() as session:
            while len(queue) != 0:
                urls = []
                while len(queue) != 0:
                    url = queue.popleft()
                    if url not in visited:
                        urls.append(url)
                        visited.add(url)

                if len(urls) == 0:
                    return

                pages = await self._get_pages(urls, session, timeout)
                for page, url in zip(pages, urls):

                    if isinstance(page, Exception):
                        print("failed on", url)

                    source = BeautifulSoup(page, 'lxml')
                    page_content = source.find(id="contentarea")
                    program_name = page_content.find(class_="page-title").text

                    for page_url in page_content.find_all('a'):
                        url_path = page_url.get('href')
                        if BFSCrawler.is_degree_program_url(url_path):
                            queue.append(urljoin(url, url_path))

                    for course_table in page_content.find_all(class_="sc_courselist"):
                        if program_name not in self.raw_course_tables.keys():
                            self.raw_course_tables[program_name] = []

                        self.raw_course_tables[program_name].append(course_table)

    async def _get_pages(self, urls: List[str], session: aiohttp.ClientSession, timeout: int):

        async def get_page(url: str) -> str:
            async with session.get(url, timeout=timeout) as resp:
                    return await resp.text()

        page_coros = []
        for url in urls:
            page_coros.append(get_page(url))

        return await asyncio.gather(*page_coros, return_exceptions=True)

    @staticmethod
    def is_degree_program_url(url: str) -> bool:
        return url and url.startswith('/') and '-bs' in url and url[:6] != "mailto" and 'search' not in url
