from django.urls import path
from . import views

app_name = 'hotel'

urlpatterns = [
    path('search/', views.HotelSearchView.as_view(), name='search'),
    path('results/', views.HotelResultsView.as_view(), name='results'),
    path('detail/<int:pk>/', views.HotelDetailView.as_view(), name='detail'),
    path('booking/<int:pk>/', views.HotelBookingView.as_view(), name='booking'),
    path('booking/confirm/<int:pk>/', views.HotelBookingConfirmView.as_view(), name='booking_confirm'),
    path('booking/success/<str:reference>/', views.HotelBookingSuccessView.as_view(), name='booking_success'),
]
