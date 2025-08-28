from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from ninja.security import django_auth
from users.views import router as users_router
from habits.views import router as habits_router

api = NinjaAPI(auth=django_auth)

api.add_router("/users/", users_router)
api.add_router("/habits/", habits_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]