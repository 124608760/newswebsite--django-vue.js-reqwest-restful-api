from django.contrib.auth.decorators import login_required
from django.shortcuts import render,Http404, redirect, HttpResponse
from django.contrib.auth import authenticate,login as user_login,logout as user_logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from newswebsite.models import *
from newswebsite.forms import *
from rest_framework.authtoken.models import Token
# Create your views here.
def index(request):

    return render(request,'index.html')

def category(request,cate_id):

    return render(request,'category.html')

def detail(request,article_id):
    if not isinstance(request.user, User):
        return render(request, 'detail.html')
    token, created = Token.objects.get_or_create(user=request.user)    #创建登录用户的token并存到cookie中
    response = render(request, 'detail.html')
    response.set_cookie(key='token',value=token.key)
    return response

def login(request):
    if request.method == 'GET':
        form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username,password=password)
            if user:
                user_login(request,user)              #由于login方法和我自定义的login视图重名，这里将django.contrib.auth中的login方法重命名为user_login导入
                return redirect(to='index')
            else:
                return HttpResponse('用户名不存在或用户名密码错误')

    context={}
    context['form'] = form

    return render(request,'login.html',context=context)

def register(request):
    if request.method == 'GET':
        form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
           username = form.cleaned_data.get("username")
           email = form.cleaned_data.get("email")
           password = form.cleaned_data.get("password")
           user = User(username=username,email=email)
           user.set_password(password)
           user.save()                                                         #创建用户保存
           userprofile = UserProfile(belong_to=user,avatar='avatar/avatar.png')
           userprofile.save()                                                  #创建该用户的资料
           return redirect(to='login')

    context={}
    context['form']=form

    return render(request,'register.html',context=context)

@login_required(login_url='login')              #未登录则跳转到登录页面
def profile(request):
    if request.method == 'GET':
        form = EditForm(initial={'username':request.user.username,'email':request.user.email})
    if request.method == 'POST':
        form = EditForm(request.POST,request.FILES)

        if form.is_valid():
           user = request.user
           email = form.cleaned_data.get("email")
           password = form.cleaned_data.get("password")
           avatar = form.cleaned_data.get("avatar")
           user.email = email
           if avatar:
                user_profile = UserProfile.objects.get(belong_to=user)
                user_profile.avatar = avatar
                user_profile.save()             #如果有上传头像，替换用户的头像
           user.set_password(password)
           user.save()
           return redirect(to='login')

    context={}
    context['form']=form

    return render(request,'profile.html',context=context)

def logout(request):
    user_logout(request)

    return redirect(to='login')
