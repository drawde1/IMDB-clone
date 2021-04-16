from django.urls import path

from actors.views import search_actor, actor_detail, actor_link

urlpatterns = [
    path("<int:actor_id>/", actor_detail, name="actor_detail"),
    path("search/", search_actor, name="search_actor"),
    path('link/<str:actor_name>/', actor_link, name="actor_link")
]