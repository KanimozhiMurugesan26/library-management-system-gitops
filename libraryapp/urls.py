# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('', views.login_view, name='login'),
#     path('register/', views.register, name='register'),
#     path('dashboard/', views.dashboard, name='dashboard'),
#     path('books/', views.books, name='books'),
#     path('borrow/', views.borrow, name='borrow'),
#     path('return/', views.return_book, name='return'),
#     path('reserve/', views.reserve, name='reserve'),
#     path('admin_books/', views.admin_books, name='admin_books'),
#     path('reservations/', views.reservations, name='reservations'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('books/', views.books, name='books'),
    path('borrow/', views.borrow, name='borrow'),
    path('return/', views.return_book, name='return_book'),
    path('reserve/', views.reserve, name='reserve'),
    path('admin_books/', views.admin_books, name='admin_books'),
    path('reservations/', views.reservations, name='reservations'),
]
