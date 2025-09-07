from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserSerializer
from posts.serializers import PostSerializer

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    target_object = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'target_object', 'timestamp', 'is_read']

    def get_target_object(self, obj):
        if isinstance(obj.target, type(obj.target)):
            return {
                'id': obj.target.id,
                'content_type': obj.content_type.model,
                'content': str(obj.target)
            }
        
        # You would need to create a serializer for each target type
        # For example, if the target is a Post, you could use PostSerializer
        if obj.target:
            if obj.content_type.model == 'post':
                return PostSerializer(obj.target).data
        return None
