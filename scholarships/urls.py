from django.urls import path
from . import views

urlpatterns = [
    path('',                                views.home,               name='home'),
    path('scholarships/dashboard/',         views.dashboard,          name='dashboard'),
    path('scholarships/search/',            views.search_view,        name='search'),
    path('scholarships/<int:pk>/',          views.scholarship_detail, name='scholarship_detail'),
    path('scholarships/<int:pk>/eligibility/', views.eligibility_check, name='eligibility_check'),
]
