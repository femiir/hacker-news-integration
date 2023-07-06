from typing import List, Optional

from ninja import FilterSchema, Schema
from pydantic import BaseModel, Field

from hackernews.apps.news.models import HackerNewsComment, HackerNewsItem


class HackerNewsItemSchema(Schema):
    """
    Schema for representing a Hacker News item.
    """
    by: str
    descendants: int
    item_id: Optional[int]
    score: int
    title: str
    url: str
    item_type: str


class DevNewsSchema(Schema):
    """
    Schema for representing a new Hacker News item.
    """
    by: str
    title: str
    url: str

class CustomResponse(Schema):
    """
    Schema for representing a custom response.
    """
    body: Optional[dict]  = Field(None, exclude_none=True)
    message: str

class HackerNewsCommentSchema(Schema):
    """
    Schema for representing a Hacker News comment.
    """
    id: int
    by: Optional[str]
    item_id: Optional[int]
    text: Optional[str]
    parent: Optional[int]
    children: Optional[List['HackerNewsCommentSchema']]
  
   