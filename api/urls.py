from django.urls import include, path

from .views import UserList, UserDetail, UserDesk, AdminList, AdminDetail

app_name = 'api'

urlpatterns = [
    path('', UserList.as_view()),
    path('<int:id>/', UserDetail.as_view()),
    path('<int:userid>/desk', UserDesk.as_view()),
    path('admin/', AdminList.as_view()),
    path('admin/<int:id>', AdminDetail.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
