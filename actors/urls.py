from django.urls import path

from actors.views import search_actor, actor_detail

urlpatterns = [
    path("<int:actor_id>", actor_detail, name="actor_detail"),
    path("search/", search_actor, name="search_actor"),
]