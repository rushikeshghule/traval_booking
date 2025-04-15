from django.urls import path
from . import views

app_name = 'bus'

urlpatterns = [
    path('search/', views.BusSearchView.as_view(), name='search'),
    path('results/', views.BusResultsView.as_view(), name='results'),
    path('detail/<int:pk>/', views.BusDetailView.as_view(), name='detail'),
    path('booking/<int:pk>/', views.BusBookingView.as_view(), name='booking'),
    path('booking/confirm/<int:pk>/', views.BusBookingConfirmView.as_view(), name='booking_confirm'),
    path('booking/success/<str:reference>/', views.BusBookingSuccessView.as_view(), name='booking_success'),
]
