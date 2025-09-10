from django.urls import path
from .views import index,send_contact,download_cv

urlpatterns = [
   path('', index.as_view(), name='index'),
   path('contact/', send_contact, name="contact"),
   path('download-cv/<int:item_id>/', download_cv, name='download_cv'),
]
