from mangas_origines.utils import Utils
from bs4 import BeautifulSoup
import aiofiles
import asyncio
import aiohttp
import json
import re
import os


class Main:
    def __init__(
            self,
            url: str,
            path: str,
            client_session: aiohttp.ClientSession
    ):
        self.url = url
        self.path = path if path[-1] == os.sep else path + os.sep
        self.temp_path = self.path + 'temp' + os.sep
        self.client_session = client_session
        self.utils = Utils

        self.scan_id = 0
        self.has_season = False
        self.chapters_url = []
        self.chapters_url_len = 0
        self.chapters_got = 0
        self.images_url = []
        self.images_url_len = 0
        self.images_got = 0

    async def __get_images_links(self, chapter_url: str):
        async with self.client_session.get(chapter_url) as r:
            all_links = BeautifulSoup(
                await r.text(),
                'html.parser'
            ).find_all('script')

        chapter_split = chapter_url.split('/')
        chapter = chapter_split[len(chapter_split) - 2].replace('chapitre-', '').replace('_1', '')

        if re.findall(r'-[a-zA-Z%]+', chapter):
            chapter = chapter.split(re.findall(r'-[a-zA-Z%]+', chapter)[0])[0]

        season = ''

        if self.has_season:
            season = chapter_split[5].replace('saison-', '')

        for x in all_links:
            if x.contents and 'chapter_preloaded_images' in x.contents[0]:
                for x2 in json.loads(
                        str(
                            x.contents[0]
                        ).replace(' ', '').replace('varchapter_preloaded_images=', '')
                                .replace(',chapter_images_per_page=1;', '')
                ):
                    if [chapter, x2] not in self.images_url:
                        self.images_url.append([chapter, x2, season])

        self.chapters_got += 1
        self.utils.progress_bar(self.chapters_got, self.chapters_url_len, 'Get the links to all images in all chapters')

    async def __download(self, element: list):
        file_name = os.path.basename(element[1])

        if self.has_season:
            folder = self.path + element[2] + os.sep + element[0] + os.sep
            temp_folder = self.temp_path + element[2] + os.sep + element[0] + os.sep
        else:
            folder = self.path + element[0] + os.sep
            temp_folder = self.temp_path + element[0] + os.sep

        if os.path.isfile(folder + file_name) is False:
            self.utils.create_folder(folder)
            self.utils.create_folder(temp_folder)

            async with self.client_session.get(element[1]) as r:
                async with aiofiles.open(temp_folder + file_name, 'wb') as f:
                    async for data in r.content.iter_chunked(1024):
                        await f.write(data)
            os.rename(temp_folder + file_name, folder + file_name)

        self.images_got += 1
        self.utils.progress_bar(self.images_got, self.images_url_len, 'Download all images')

    async def start(self):
        self.utils.clear_line()
        self.utils.clear_line()

        self.utils.create_folder(self.path)
        self.utils.create_folder(self.temp_path)

        print('Get scan id...', end='\r')

        async with self.client_session.get(self.url) as r:
            content = await r.text()

            for x in content.split('\n'):
                if 'postid' in x:
                    self.scan_id = int(x.split('postid')[1].split(' ')[0].replace('-', ''))

        print('Get all chapters links...', end='\r')

        async with self.client_session.post(
                'https://mangas-origines.fr/wp-admin/admin-ajax.php',
                data={'action': 'manga_get_chapters', 'manga': self.scan_id}
        ) as r:
            all_links = BeautifulSoup(
                await r.text(),
                'html.parser'
            ).find_all('a', href=True)

        for link in all_links:
            href = str(link.get('href')) + '?style=paged'

            if 'http' in href and href not in self.chapters_url:
                self.chapters_url.append(href)

                if 'saison' in href and self.has_season is False:
                    self.has_season = True

        self.chapters_url_len = len(self.chapters_url)
        self.utils.progress_bar(0, self.chapters_url_len, 'Get the links to all images in all chapters')
        await self.utils.limit_task(15, *[self.__get_images_links(url) for url in self.chapters_url])

        self.utils.clear_line()

        self.images_url_len = len(self.images_url)
        self.utils.progress_bar(0, self.images_url_len, 'Download all images')
        await self.utils.limit_task(5, *[self.__download(url) for url in self.images_url])

        self.utils.delete_folder(self.temp_path)

        print('Completed!', end='\r')


async def main():
    url = ''
    is_first = True

    while 'https://mangas-origines.fr/' not in url:
        if is_first:
            is_first = False
        else:
            Utils.clear_line()

        url = input(
            'Please enter the download url (e.g. '
            'https://mangas-origines.fr/manga/martial-peak/). > '
        ).replace(' ', '')

    path = input('Please enter the folder where the images are saved (e.g. /home/asthowen/download/scans/). > ')

    async with aiohttp.ClientSession(
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
    ) as client_session:
        await Main(url, path, client_session).start()


def start():
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        Utils().send_except('Stop the script...')
    except aiohttp.InvalidURL:
        Utils().send_except('Invalid URL!')
    except PermissionError:
        Utils().send_except('Permission denied for folder!')
