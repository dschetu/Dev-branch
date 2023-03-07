from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

# Create your views here.
class ArticleView(APIView):
    def get(self,request):
        model = Article.objects.all()
        serializer = ArticleSerializer(model,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleUpdateView(APIView):

    def get_article(self,article_id):
        try:
            articleobj = Article.objects.get(id=article_id)
            return articleobj
        except Article.DoesNotExist:
            return Response(f'Article with ID {article_id} is Not Found in the Database',status=status.HTTP_404_NOT_FOUND)
        
    def get(self,request,article_id):
        serializerobj = ArticleSerializer(self.get_article(article_id))
        return Response(serializerobj.data)
    
    def put(self,request,article_id):
        try:
            articleobj = Article.objects.get(id=article_id)
        except:
            return Response(f'Article with ID {article_id} is Not Found in the Database',status=status.HTTP_404_NOT_FOUND)
        serializerobj = ArticleSerializer(articleobj,data=request.data)
        if serializerobj.is_valid():
            serializerobj.save()
            return Response(serializerobj.data,status=status.HTTP_200_OK)
        return Response(serializerobj.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,article_id):
        articleobj = self.get_article(article_id)
        articleobj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)