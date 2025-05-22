
from rest_framework import serializers
from .models import Workers, News


class WorkersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workers
        fields = ('login','password', 'name', 'email', 'phone', 'role')

class WorkersLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workers
        fields = ('login', 'name', 'email', 'phone', 'role')


class NewsSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ('id','title', 'subTitle', 'content', 'dateTime', 'image', 'image_url')
        extra_kwargs = {
            'title': {'required': True, 'error_messages': {'required': 'Поле "Заголовок" обязательно'}},
            'subTitle': {'required': True, 'error_messages': {'required': 'Поле "Подзаголовок" обязательно'}},
            'content': {'required': True, 'error_messages': {'required': 'Поле "Контент" обязательно'}},
        }
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None
