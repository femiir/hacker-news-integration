from asgiref.sync import sync_to_async
from bleach import clean
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import HackerNewsComment, HackerNewsItem


class HackernewsListView(ListView):
    """
    A view for displaying a list of Hacker News items.

    Inherits from Django's generic ListView class.
    """
    model = HackerNewsItem
    template_name = 'news/hackernews_list.html'
    context_object_name = 'news_items'
    paginate_by = 10

    async def get_queryset(self):
        """
        Retrieve the queryset of Hacker News items.

        Applies optional filters based on item_type and search query parameters.

        Returns:
            queryset (QuerySet): The filtered and sorted queryset of Hacker News items.
        """
        queryset = await sync_to_async(HackerNewsItem.objects.all)()

        item_type = self.request.GET.get('item_type')
        search_query = self.request.GET.get('search')

        if item_type:
            queryset = queryset.filter(item_type=item_type)
        
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        

        return queryset.order_by('-id')

    async def get(self, request, *args, **kwargs):
        """
        A view for displaying the details of a Hacker News item.

        Inherits from Django's generic DetailView class.
        """
        queryset = await self.get_queryset()

        paginator = Paginator(queryset, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj= await sync_to_async(paginator.get_page)(page_number)

        context = {'news_items': page_obj}

        context['item_type'] = request.GET.get('item_type', 'All')
        return await sync_to_async(render)(request, self.template_name, context)

class HackernewsDetails(DetailView):
    """
    A view for displaying the details of a Hacker News item.

    Inherits from Django's generic DetailView class.
    """

    model = HackerNewsItem
    template_name = 'news/hackernews_detail.html'
    context_object_name = 'news_item'

    def get_object(self, queryset=None):
        """
        Retrieve the Hacker News item object.

        Returns:
            HackerNewsItem: The Hacker News item object.
        """
        news_id = self.kwargs.get('pk')
        news_item = HackerNewsItem.objects.get(id=news_id)
        return news_item

    def get_context_data(self, **kwargs):
        """
        Get the context data for rendering the template.

        Retrieves the comments associated with the Hacker News item and cleans them.

        Returns:
            dict: The context data for rendering the template.
        """

        context = super().get_context_data(**kwargs)
        comments = HackerNewsComment.objects.filter(news_item=context['news_item'], parent=None)
        context['comments'] = self.clean_comments(comments)
        return context

    def clean_comments(self, comments):
        """
        Clean and structure the comments recursively.

        Cleans the HTML content of the comments and structures them in a hierarchical format.

        Args:
            comments (QuerySet): The comments to be cleaned.

        Returns:
            list: The cleaned and structured comments.
        """
        cleaned_comments = []
        for comment in comments:
            cleaned_comment = {
                'comment': comment,
                'children': self.clean_comments(HackerNewsComment.objects.filter(parent=comment))
            }
            cleaned_comments.append(cleaned_comment)
        return cleaned_comments




"""

helper view to manually fetch the news

"""
    
import asyncio

from django.http import HttpResponse
from django.views import View

from .utils import HackerNewsFetcher


class FetchHackerNewsView(View):
    async def get(self, request):
        hacker_news_fetcher = HackerNewsFetcher()
        await hacker_news_fetcher.run()
        return HttpResponse("Hacker News fetch completed.")
