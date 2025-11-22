from django.urls import path, include

urlpatterns = [
    path('rules/', include('orders.urls')),
]

