from rest_framework import serializers
from.models import Post

# serializer.py


class PostSerializers(serializers.ModelSerializer):
    
    class Meta:
        model=Post
        fields = "__all__"