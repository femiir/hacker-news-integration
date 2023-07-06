from typing import List

from django.core import serializers
from django.shortcuts import get_object_or_404
from ninja import Router

from hackernews.apps.news.models import HackerNewsComment, HackerNewsItem

from .schema import (CustomResponse, DevNewsSchema, HackerNewsCommentSchema,
                     HackerNewsItemSchema)

router = Router()


@router.get("/items", response=List[HackerNewsItemSchema])
def list_items(request, limit: int = 100):
    """
    Retrieve a list of Hacker News items.

    Args:
        request (HttpRequest): The HTTP request object.
        limit (int, optional): The maximum number of items to retrieve. Defaults to 100.

    Returns:
        List[HackerNewsItemSchema]: The list of Hacker News items.
    """
    items_qs = HackerNewsItem.objects.order_by('-id')[:limit]
    return items_qs

@router.post("/items")
def add_item(request, payload: DevNewsSchema):
    """
    Add a new Hacker News item.

    Args:
        request (HttpRequest): The HTTP request object.
        payload (DevNewsSchema): The payload containing the details of the new item.

    Returns:
        dict: The response containing the added item details.
    """
    descendants = 0
    score = 0
    item_type=f'in-house'

    item = HackerNewsItem.objects.create(
        title=payload.title,
        by=payload.by,
        url=payload.url,
        descendants=descendants,
        score=score,
        item_type=item_type,
        in_house=True
    )
    item.item_id = item.id 
    item.save()
    

    return {'by': item.by,
        'title': item.title,
        'message': 'Item added successfully'}



@router.put("/items/{item_id}", response={200:CustomResponse, 401: CustomResponse})
def update_item(request, item_id: int, payload: DevNewsSchema):
    """
    Update an existing Hacker News item.

    Args:
        request (HttpRequest): The HTTP request object.
        item_id (int): The ID of the item to update.
        payload (DevNewsSchema): The payload containing the updated item details.

    Returns:
        Union[int, dict]: The response indicating the status and message of the update operation.
    """
    item = HackerNewsItem.objects.get(item_id=item_id)
    if not item.in_house:
        return 401, CustomResponse(message='Unauthorized')
    else:
        for attr, value in payload.dict().items():
            setattr(item, attr, value)
        item.save()
    
        return 200, CustomResponse(message='Update Succesul!', body=payload)
    
@router.delete("/items/{item_id}", response={200:CustomResponse, 401: CustomResponse})
def delete_item(request, item_id: int):
    """
    Delete an existing Hacker News item.

    Args:
        request (HttpRequest): The HTTP request object.
        item_id (int): The ID of the item to delete.

    Returns:
        Union[int, dict]: The response indicating the status and message of the deletion operation.
    """
    item = get_object_or_404(HackerNewsItem, item_id=item_id)
    if not item.in_house:
        return 401, CustomResponse(message='Unauthorized', body=None)
    else:
        # Perform item deletion logic
        item.delete()

        return 200, CustomResponse(message='Delete Successful!')
    


@router.get("/items/{item_id}", response=HackerNewsItemSchema)
def get_item(request, item_id: int):
    item = HackerNewsItem.objects.get(item_id=item_id)
    return item



@router.get("/items/{item_id}/comments", response=List[HackerNewsCommentSchema])
def get_item_comments(request, item_id: int):
    """
    Retrieve a specific Hacker News item.

    Args:
        request (HttpRequest): The HTTP request object.
        item_id (int): The ID of the itemto retrieve.

    Returns:
        HackerNewsItemSchema: The details of the retrieved Hacker News item.
    """
    comments = HackerNewsComment.objects.filter(news_item__item_id=item_id)
    cleaned_comments = []

    for comment in comments:
        if comment.parent:
            parent_id = comment.parent.id if isinstance(comment.parent.id, int) else None
        else:
            parent_id = None

        cleaned_comment = HackerNewsCommentSchema(
            id=comment.id,
            by=comment.by,
            item_id=comment.item_id,
            text=comment.text,
            parent=parent_id,
            children=[]
        )

        cleaned_comments.append(cleaned_comment)

    return cleaned_comments
