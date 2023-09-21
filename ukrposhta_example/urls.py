from django.urls import path

from .views import *

urlpatterns = [
    path('', archive, name='archive'),
    path('letter/search', search_results, name='search_results'),
    path('letter/add/', letter_add, name='letter_add'),
    path('letter/<slug:slug>/details/', letter_details, name='letter_details'),
    path('letter/<slug:slug>/update/', UpdateLetterInfo.as_view(), name='letter_update'),
    path('recipient/add/', recipient_add, name='recipient_add'),
    path('recipients/list/', recipient_list, name='recipient_list'),
    path('sender/add/', sender_add, name='sender_add'),
    path('senders/list/', sender_list, name='sender_list'),
]
