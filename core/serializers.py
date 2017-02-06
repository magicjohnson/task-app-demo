from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import Task


class TaskSerializer(serializers.ModelSerializer):
    is_own = serializers.SerializerMethodField()
    created_by = serializers.ReadOnlyField(source='created_by.username')
    completed_by = serializers.ReadOnlyField(source='completed_by.username')

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'status', 'is_own', 'created_by', 'completed_by')
        extra_kwargs = {
            'name': {'required': False},
        }

    def get_is_own(self, obj):
        return obj.created_by == self.context['request'].user

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data['status'] == instance.DONE:
            validated_data['completed_by'] = self.context['request'].user

        return super().update(instance, validated_data)

    def validate(self, attrs):
        if not self.instance and not attrs.get('name'):
            raise ValidationError({'name': 'This field is required.'})
        return super().validate(attrs)



