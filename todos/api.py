from ninja import Router, Schema
from typing import List
from .models import Todo
from datetime import datetime
import uuid

todo_router = Router()

class TodoSchema(Schema):
    id: uuid.UUID            
    title: str
    description: str | None = None
    completed: bool
    created_at: datetime    
    updated_at: datetime

    class Config:
        from_attributes = True  

class TodoCreateSchema(Schema):
    title: str
    description: str | None = None


class TodoUpdateSchema(Schema):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

# ==== Routes ====
@todo_router.get("/", response=List[TodoSchema])
def list_todos(request):
    return Todo.objects.all().order_by("-created_at")

@todo_router.get("/{todo_id}", response=TodoSchema)
def get_todo(request, todo_id: str):
    return Todo.objects.get(id=todo_id)

@todo_router.post("/", response=TodoSchema)
def create_todo(request, data: TodoCreateSchema):
    todo = Todo.objects.create(**data.dict())
    return todo

@todo_router.put("/{todo_id}", response=TodoSchema)
def update_todo(request, todo_id: str, data: TodoUpdateSchema):
    todo = Todo.objects.get(id=todo_id)
    for attr, value in data.dict(exclude_none=True).items():
        setattr(todo, attr, value)
    todo.save()
    return todo

@todo_router.delete("/{todo_id}")
def delete_todo(request, todo_id: str):
    todo = Todo.objects.get(id=todo_id)
    todo.delete()
    return {"success": True}