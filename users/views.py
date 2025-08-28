from ninja import Router, Schema
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from typing import Optional

router = Router(tags=["users"])

class RegisterIn(Schema):
    username: str
    email: Optional[str] = None
    password: str

class UserOut(Schema):
    id: int
    username: str
    email: Optional[str] = None

@router.post("register", response=UserOut)
def register(request: HttpRequest, data: RegisterIn):
    if User.objects.filter(username=data.username).exists():
        raise ValueError("Username already taken")
    user = User.objects.create_user(
        username=data.username, email=data.email or "", password=data.password
    )
    return UserOut(id=user.id, username=user.username, email=user.email)

class LoginIn(Schema):
    username: str
    password: str

@router.post("login")
def login_view(request: HttpRequest, data: LoginIn):
    user = authenticate(request, username=data.username, password=data.password)
    if not user:
        return {"success": False, "message": "Invalid credentials"}
    login(request, user)
    return {"success": True, "message": "Logged in"}

@router.post("logout")
def logout_view(request: HttpRequest):
    logout(request)
    return {"success": True}

@router.get("me", response=UserOut)
def me(request: HttpRequest):
    if not request.user.is_authenticated:
        raise PermissionError("Not authenticated")
    u = request.user
    return UserOut(id=u.id, username=u.username, email=u.email)