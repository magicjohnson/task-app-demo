from django.views.generic import TemplateView
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.models import Task
from core.serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action not in ('list', 'complete'):
            queryset = queryset.filter(created_by=self.request.user)
        return queryset

    @detail_route(methods=['post'])
    def complete(self, *args, **kwargs):
        task = self.get_object()
        task.completed_by = self.request.user
        task.status = task.DONE
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)


class IndexView(TemplateView):
    template_name = 'core/index.html'
