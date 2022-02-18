from unicodedata import name
from django.urls import path
from .views import memberLogin,memberRegi

urlpatterns = [
    path('' , memberLogin , name="memberLogin" ),
    path('memberRegi/' ,  memberRegi , name="memberRegi")
]
