import asyncio

from django_q.tasks import async_task

from hackernews.apps.news.utils import HackerNewsFetcher


async def news_scrapper():
    """
    Asynchronous function for running the Hacker News scrapper.

    Instantiates a HackerNewsFetcher object and runs the scrapper.

    """
    propagate = HackerNewsFetcher()
    await propagate.run()



def schedule_sync_news():
    """
    Schedule the synchronization of Hacker News items.

    Creates an async task for running the news_scrapper function.

    Returns:
        async_task: The created async task.
    """
    scrapper  = asyncio.run(news_scrapper())

    item=async_task(scrapper)

    print('Task created')
    return(item)

