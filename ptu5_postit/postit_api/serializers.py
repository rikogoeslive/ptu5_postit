from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import models

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = models.Comment
        fields = ('id', 'post', 'body', 'user', 'user_id', 'created_at')

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    #comments = serializers.StringRelatedField(many=True) (nenaudoti)  

    def get_likes_count(self, obj):
        return models.Postlike.objects.filter(post=obj).count()

    def get_comments_count(self, obj):
        return models.Comment.objects.filter(post=obj).count()


    class Meta:
        model = models.Post
        fields = ('id', 'title', 'body', 'image', 'user', 'user_id', 'created_at', 'likes_count', 'comments_count', 'comments')


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Postlike
        fields = ('id', )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  ('username', 'id', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user