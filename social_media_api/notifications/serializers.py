from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    recipient_username = serializers.CharField(source='recipient.username', read_only=True)
    target_ct = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('id','recipient','recipient_username','actor','actor_username','verb','target_content_type','target_object_id','is_read','timestamp','target_ct')
        read_only_fields = ('actor','recipient','timestamp')

    def get_target_ct(self, obj):
        if obj.target_content_type:
            return f'{obj.target_content_type.app_label}.{obj.target_content_type.model}'
        return None
