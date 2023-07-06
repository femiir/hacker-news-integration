from ninja import NinjaAPI

from api.api import router as hackernews_router

api = NinjaAPI()

api.add_router('v1/hackernews', hackernews_router)