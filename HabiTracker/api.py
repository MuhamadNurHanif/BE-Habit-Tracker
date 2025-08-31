from ninja import NinjaAPI
from todos.api import todo_router

api = NinjaAPI()
api.add_router("/todos/", todo_router)