from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import User
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        depth = 1

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        depth = 1

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','profile','username')
        depth = 1

class CommentSerializer(serializers.ModelSerializer):
    belong_user = UserSerializer()
    class Meta:
        model = Comment
        fields = '__all__'
        depth = 1

@api_view(['GET'])
def api_index(request):                                                #首页api
    cates = Category.objects.all().order_by("-id") #分类列表
    cates = CategorySerializer(cates,many=True)

    todaynew_big = Best.objects.filter(select_reason="今日新闻")[0].select_article #取出一篇今日新闻作为大标题
    todaynew_big = ArticleSerializer(todaynew_big)
    todaynew = Best.objects.filter(select_reason="今日新闻")[:3]
    todaynew_top3 = [i.select_article for i in todaynew]                          #取出三篇今日新闻
    todaynew_top3 = ArticleSerializer(todaynew_top3,many=True)

    index_recommend = Best.objects.filter(select_reason="首页推荐")[:4]
    index_recommendlist = [i.select_article for i in index_recommend]   #取出四篇首页推荐
    index_recommendlist = ArticleSerializer(index_recommendlist,many=True)

    editor_recommendtop3 = Best.objects.filter(select_reason="编辑推荐")[:3]
    editor_recommendtop3list = [i.select_article for i in editor_recommendtop3] #取出三篇编辑推荐作为大标题
    editor_recommendtop3list = ArticleSerializer(editor_recommendtop3list,many=True)

    editor_recommend = Best.objects.filter(select_reason="编辑推荐")[3:10]
    editor_recommendlist = [i.select_article for i in editor_recommend]     #再取出七篇编辑推荐
    editor_recommendlist = ArticleSerializer(editor_recommendlist,many=True)

    article_list = Article.objects.all().order_by("-publish_time") #取出所有文章
    pagerobot = Paginator(article_list,5)                         #创建分页器，每页限定五篇文章
    page_num = request.GET.get("page")                            #取到当前页数
    try:
        article_list = pagerobot.page(page_num)                   #一般情况下返回当前页码下的文章
    except EmptyPage:
        article_list = pagerobot.page(pagerobot.num_pages)        #如果不存在该业，返回最后一页
    except PageNotAnInteger:
        article_list = pagerobot.page(1)                          #如果页码不是一个整数，返回第一页
    pages = len(article_list.paginator.page_range)                #取总页数

    article_list = ArticleSerializer(article_list,many=True)

    context={}
    context={
      "cates":cates.data,
      "todaynew_big":todaynew_big.data,
      "todaynew_top3":todaynew_top3.data,
      "index_recommendlist":index_recommendlist.data,
      "editor_recommendtop3list":editor_recommendtop3list.data,
      "editor_recommendlist":editor_recommendlist.data,
      "pages":pages,
      "article_list":article_list.data
    }


    return Response(context)

@api_view(['GET'])
def api_category(request,cate_id):
    cates = Category.objects.all().order_by("-id") #分类列表
    cates = CategorySerializer(cates,many=True)

    editor_recommendtop3 = Best.objects.filter(select_reason="编辑推荐")[:3]
    editor_recommendtop3list = [i.select_article for i in editor_recommendtop3] #取出三篇编辑推荐作为大标题
    editor_recommendtop3list = ArticleSerializer(editor_recommendtop3list,many=True)

    editor_recommend = Best.objects.filter(select_reason="编辑推荐")[3:10]
    editor_recommendlist = [i.select_article for i in editor_recommend]     #再取出七篇编辑推荐
    editor_recommendlist = ArticleSerializer(editor_recommendlist,many=True)

    article_list = Article.objects.filter(category=int(cate_id)).order_by("-publish_time") #取出当前目录下的所有文章
    print(article_list[0].category)
    pagerobot = Paginator(article_list,5)                         #创建分页器，每页限定五篇文章
    page_num = request.GET.get("page")                            #取到当前页数
    try:
        article_list = pagerobot.page(page_num)                   #一般情况下返回当前页码下的文章
    except EmptyPage:
        article_list = pagerobot.page(pagerobot.num_pages)        #如果不存在该业，返回最后一页
    except PageNotAnInteger:
        article_list = pagerobot.page(1)                          #如果页码不是一个整数，返回第一页
    pages = len(article_list.paginator.page_range)                #取总页数

    article_list = ArticleSerializer(article_list,many=True)

    context={}
    context={
      "cates":cates.data,
      "editor_recommendtop3list":editor_recommendtop3list.data,
      "editor_recommendlist":editor_recommendlist.data,
      "pages":pages,
      "article_list":article_list.data
    }


    return Response(context)

@api_view(['GET','POST'])
@authentication_classes((TokenAuthentication,))
def api_detail(request,article_id):
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        current_article = Article.objects.get(id=article_id)
        current_user = User.objects.get(id=request.user.id)
        created = request.POST.get('created')
        words = request.POST.get('words')
        newcomment = Comment(belong_article=current_article,belong_user=current_user,created=created,words=words)
        newcomment.save()
        return Response(status=status.HTTP_201_CREATED)
    cates = Category.objects.all().order_by("-id") #分类列表
    cates = CategorySerializer(cates,many=True)

    editor_recommendtop3 = Best.objects.filter(select_reason="编辑推荐")[:3]
    editor_recommendtop3list = [i.select_article for i in editor_recommendtop3] #取出三篇编辑推荐作为大标题
    editor_recommendtop3list = ArticleSerializer(editor_recommendtop3list,many=True)

    editor_recommend = Best.objects.filter(select_reason="编辑推荐")[3:10]
    editor_recommendlist = [i.select_article for i in editor_recommend]     #再取出七篇编辑推荐
    editor_recommendlist = ArticleSerializer(editor_recommendlist,many=True)

    article = Article.objects.get(id=article_id)
    comments = Comment.objects.filter(belong_article_id=article_id)
    comments = CommentSerializer(comments,many=True)
    article = ArticleSerializer(article)

    context ={}
    context ={
       "cates":cates.data,
       "editor_recommendtop3list":editor_recommendtop3list.data,
       "editor_recommendlist":editor_recommendlist.data,
       "article":article.data,
       "comments":comments.data,

    }

    return Response(context)
