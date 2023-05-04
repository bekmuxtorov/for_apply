from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('tickets', views.tickets_page, name='tickets'),
    path('tickets/<int:pk>', views.tables_detail, name='tickets_detail'),
    path('send_message/ticket/<int:pk>',
         views.send_message_page, name='send_message'),
    path('filter_status/<str:status>/',
         views.status_tables_page, name='filter_status'),
    path('filter_type/<int:pk>/',
         views.type_tables_page, name='filter_type'),
]
