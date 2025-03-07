from django.urls import path
from iam.views import Login, Signup, Getme


urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('getme/', Getme.as_view(), name='getme'),
]
