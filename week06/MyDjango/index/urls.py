from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),

    path('<int:year>',views.year),
    path('<int:year>/<str:name>', views.name),
    path('books',views.books),
]