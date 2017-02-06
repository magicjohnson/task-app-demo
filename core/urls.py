from django.conf.urls import include, url
from rest_framework import routers

from core.views import TaskViewSet, IndexView

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url('^$', IndexView.as_view(), name='index'),
]
