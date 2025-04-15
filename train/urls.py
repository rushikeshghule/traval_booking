from django.urls import path
from . import views

app_name = 'train'

urlpatterns = [
    path('search/', views.TrainSearchView.as_view(), name='search'),
    path('results/', views.TrainResultsView.as_view(), name='results'),
    path('detail/<int:pk>/', views.TrainDetailView.as_view(), name='detail'),
    path('booking/<int:pk>/', views.TrainBookingView.as_view(), name='booking'),
    path('booking/confirm/<int:pk>/', views.TrainBookingConfirmView.as_view(), name='booking_confirm'),
    path('booking/success/<str:reference>/', views.TrainBookingSuccessView.as_view(), name='booking_success'),
]
