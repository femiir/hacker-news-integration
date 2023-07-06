import asyncio

import aiohttp
import ujson
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from .models import HackerNewsComment, HackerNewsItem


class HackerNewsFetcher:
    """
    Class for fetching and saving Hacker News items and comments.

    """

    def __init__(self):
        self.session = None

    async def initialize(self):
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=None))

    async def close(self):
        """
        Close the aiohttp ClientSession.

        """
        await self.session.close()

    async def get_latest_news_id(self):
        """
        Retrieve the latest Hacker News item IDs.

        Returns:
            list: The list of latest Hacker News item IDs.
        """
        new_hackernews_url = 'https://hacker-news.firebaseio.com/v0/newstories.json'
        async with self.session.get(new_hackernews_url) as response:
            response.raise_for_status()
            news_ids = await response.json(loads=ujson.loads)
            latest_news_ids = news_ids[:100]
        return latest_news_ids

    async def fetch_news_item(self, url):
        """
        Fetch and save a Hacker News item.

        Args:
            url (str): The URL to fetch the Hacker News item.

        """
        async with self.session.get(url) as response:
            response.raise_for_status()
            news_item = await response.json(loads=ujson.loads)

            hacker_news_item = HackerNewsItem(
                item_id=news_item.get('id', ''),
                title=news_item.get('title'),
                by=news_item.get('by'),
                url=news_item.get('url', ''),
                descendants=int(news_item.get('descendants', 0) or 0),
                score=news_item.get('score', ''),
                item_type=news_item.get('type', '')
            )

            try:
                await sync_to_async(HackerNewsItem.objects.get)(item_id=hacker_news_item.item_id)
            except ObjectDoesNotExist:
                await self.save_model(hacker_news_item)


            if 'kids' in news_item:
                kid_ids = news_item.get('kids', [])
                await self.fetch_and_save_kids_items(kid_ids=kid_ids, item_id=hacker_news_item, parent_comment_id=None)

    async def fetch_news_items(self):
        """
        Fetch and save multiple Hacker News items.

        """
        latest_news_ids = await self.get_latest_news_id()
        tasks = [
            asyncio.ensure_future(
                self.fetch_news_item(f'https://hacker-news.firebaseio.com/v0/item/{item_id}.json')
            )
            for item_id in latest_news_ids
        ]
        await asyncio.gather(*tasks)

    async def fetch_kids_item(self, url):
        """
        Fetch a Hacker News comment.

        Args:
            url (str): The URL to fetch the Hacker News comment.

        Returns:
            dict: The fetched Hacker News comment.

        """

        async with self.session.get(url) as response:
            response.raise_for_status()
            kids_item = await response.json(loads=ujson.loads)
            return kids_item
        
    async def fetch_and_save_kids_items(self, kid_ids: list, item_id: HackerNewsItem = None, parent_comment_id:HackerNewsComment  = None):
        """
        Fetch and save the Hacker News comments (kid items).

        Args:
            kid_ids (list): The list of Hacker News comment IDs.
            item_id (HackerNewsItem): The parent Hacker News item.
            parent_comment_id (HackerNewsComment): The parent comment ID.

        """

        tasks = [
            asyncio.ensure_future(
                self.fetch_kids_item(f'https://hacker-news.firebaseio.com/v0/item/{kid_id}.json')
            )
            for kid_id in kid_ids
        ]
        kids_items = await asyncio.gather(*tasks)
        
        for kid_item in kids_items:
            kid_news_item = HackerNewsComment(
                by=kid_item.get('by'),
                item_id=kid_item.get('id'),
                text=kid_item.get('text'),
                parent=parent_comment_id if  parent_comment_id else None,
                news_item=item_id
            )

         
            
            await self.save_model(kid_news_item)
           

            if 'kids' in kid_item:         
                await self.fetch_and_save_kids_items(kid_ids=kid_item.get('kids'), item_id=kid_news_item.news_item, parent_comment_id=kid_news_item)
    
    async def save_model(self, model):
        """
        Save the model instance asynchronously.

        Args:
            model: The model instance to be saved.

        """
        try:
            await sync_to_async(model.save)()
        except IntegrityError:
            pass  # Skip saving if the unique constraint is violated
        except Exception as e:
            # Handle other exceptions if needed
            pass
    
    async def run(self):
        """
        Run the Hacker News fetching process asynchronously.

        """
        await self.initialize()
        await self.fetch_news_items()
        await self.close()


if __name__ == '__main__':
    """
    Entry point for running the Hacker News fetching process.

    """
    hacker_news_fetcher = HackerNewsFetcher()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(hacker_news_fetcher.run())
