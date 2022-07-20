from django.urls import path
from . import views

app_name = 'parking_lot_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('entry/', views.entry, name='entry'),
    path('exit/', views.exit, name='exit'),
    # path('entry_details/', views.entry_details, name='entry_details'),
    path('print_ticket/<str:ref>', views.print_ticket, name='print_ticket'),
    path('ticket_lost/', views.ticket_lost, name='ticket_lost'),
    path('manual_exit/', views.manual_exit, name='manual_exit'),
]
