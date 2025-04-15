from django.urls import path
from . import views

app_name = 'flight'

urlpatterns = [
    path('search/', views.FlightSearchView.as_view(), name='search'),
    path('results/', views.FlightResultsView.as_view(), name='results'),
    path('detail/<int:pk>/', views.FlightDetailView.as_view(), name='detail'),
    path('booking/<int:pk>/', views.FlightBookingView.as_view(), name='booking'),
    path('booking/confirm/<int:pk>/', views.FlightBookingConfirmView.as_view(), name='booking_confirm'),
    path('booking/success/<str:reference>/', views.FlightBookingSuccessView.as_view(), name='booking_success'),
]
