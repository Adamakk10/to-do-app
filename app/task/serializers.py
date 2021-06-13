from rest_framework import serializers
from core.models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'task', 'is_done', 'time_created')
        read_only_fields = ('id', 'time_created')

    