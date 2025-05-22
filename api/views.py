import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Workers
from .serializer import *

class WorkersAPIView(APIView):
    def get(self, request):
        workers = Workers.objects.all()
        serializer = WorkersSerializer(workers, many=True).data
        return Response({'workers':serializer})

    def post(self, request):
        login = request.data.get('login')
        password = request.data.get('password')

        if not login or not password:
            return Response({'error':'login and password are required'},status=400)
        try:
            worker = Workers.objects.get(login=login, password=password)
            serializers = WorkersLoginSerializer(worker)
            return Response({'success':True,'message':'Worker found','data':serializers.data})

        except Workers.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class NewsAPIView(APIView):
    def get(self, request):
        data = News.objects.all()
        serializer = NewsSerializer(data,many=True, context={'request': request})
        return Response({'data':serializer.data})

    def post(self, request):
        serializer = NewsSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'Успешно добавлена','data':serializer.data})
        return Response(serializer.errors, status=400)

class NewsDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            news_item = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response({'error': 'Новость не найдена'}, status=status.HTTP_404_NOT_FOUND)

        serializer = NewsSerializer(news_item, context={'request': request})
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            news_item = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response({'error': 'Новость не найдена'}, status=status.HTTP_404_NOT_FOUND)

        old_image = news_item.image.path if news_item.image else None
        print(old_image)
        new_image = request.FILES.get('image')
        print(new_image)
        serializer = NewsSerializer(news_item, data=request.data, context={'request': request})
        if serializer.is_valid():
            if new_image and old_image and os.path.isfile(old_image):
                try:
                    os.remove(old_image)
                except Exception as e:
                    # Можно залогировать ошибку или вернуть ошибку, если нужно
                    print(f"Ошибка при удалении файла: {e}")

            serializer.save()
            return Response({'message': 'Новость обновлена', 'data': serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            news_item = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response({'error': 'Новость не найдена'}, status=status.HTTP_404_NOT_FOUND)

        # Удаляем изображение, если оно есть
        if news_item.image and news_item.image.path:
            import os
            if os.path.isfile(news_item.image.path):
                os.remove(news_item.image.path)

        news_item.delete()
        return Response({'message': 'Новость удалена'}, status=status.HTTP_204_NO_CONTENT)


# Create your views here.
