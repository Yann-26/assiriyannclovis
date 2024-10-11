from django.urls import path
from .views import *

urlpatterns = [
   path('', index, name='index'),
   path('contact/', send_contact, name="contact"),
   path('download-cv/<int:item_id>/', download_cv, name='download_cv'),
   path('blog/details/<int:blog_id>/', singleblog, name="single_blog"),
]
