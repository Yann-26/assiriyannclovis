from django.urls import path
from .views import *

urlpatterns = [
   path('', index, name='index'),
   path('contact/', send_contact, name="contact"),
   path('blog/details/<int:blog_id>/', singleblog, name="single_blog"),
]
