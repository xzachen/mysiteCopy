from django.shortcuts import render,redirect,reverse,HttpResponse
from rest_framework.renderers import JSONRenderer
from myapp.froms import *
from django.core import serializers
from django.db.models import Q
import json, ast
from django.contrib.auth.models import User
from myapp.models import CollectionNote,Note,APPUser,Course
from myapp.Serializer import UserSerializer
# 网页端登录
# Create your views here.
from rest_framework.decorators import api_view

def login(request):
    # POST方法的话进行数据的校验
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        # 如果用户数据有效
        if login_form.is_valid():
            user=login_form.cleaned_data['user']
            auth.login(request,user)
            # 登录成功返回主页
            return redirect(reverse('home'))
    # 是GET方法的话跳转到渲染的模板上
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)


def index(request):
    return render(request, 'home.html', {})

def addnote(request):
    if request.method=='GET':
        form = NoteFrom()
        return render(request, 'addnote.html', {'form': form})
    # 如果为Post的话则对文章进行处理
    elif request.method=='POST':
        form = NoteFrom(request.POST)
        if form.is_valid():
            title=form.cleaned_data['title']
            category=form.cleaned_data['category']
            content=form.cleaned_data['content']
            meta_description=form.cleaned_data['meta_description']
            is_published=form.cleaned_data['is_published']
            note=Note()
            note.title=title
            note.auther=request.user
            note.category=category
            note.content=content
            note.meta_description=meta_description
            note.is_published=is_published
            note.save()
            # 保存成功之后预览文章。
            return redirect(reverse('notedetailed',args=[note.nid]))
def notedetailed(request,nid):
    note=Note.objects.get(pk=nid)
    context={}
    context['note']=note
    iscollect=CollectionNote.objects.filter(noteid=nid,cuser=request.user)
    if iscollect:
        context['iscollect']=False
    else:
        context['iscollect'] = True
    return render(request, 'sharedetailed.html',context)
def mynote(request):
    user=request.user
    notes=Note.objects.filter(auther=user)
    return render(request, 'mynote.html', {'notes': notes})

def seachnote(request):
    if request.method == "POST":
        seachkeyword = request.POST.get('seachkeyword')
        notes = Note.objects.filter(
            Q(category__icontains=seachkeyword) | Q(title__icontains=seachkeyword) | Q(content__icontains=seachkeyword))
        return render(request, 'seachnote.html', {'notes': notes})
    elif request.method == 'GET':
        return render(request, 'seachnote.html', {'notes': None})

def sharenote(request):
    notes=Note.objects.filter(is_published=True)
    return render(request, 'sharenote.html', {'notes': notes})

def collection(request):
    if request.method=="POST":
        # 把该文章加入收藏的笔记之后。
        user=request.user
        noteid=request.POST.get("noteid")
        cnote=CollectionNote()
        cnote.cuser=user
        cnote.noteid=noteid
        cnote.save()
        return redirect(reverse('collection'))
    elif request.method=="GET":
        # 取出用户所收藏的所有文章
        user=request.user
        notes = []
        cnotes=CollectionNote.objects.filter(cuser=user)
        for cnote in cnotes:
            note=Note.objects.get(pk=cnote.noteid)
            notes.append(note)
        print()
        return render(request, 'sharenote.html', {'notes': notes})

# APPuser的处理方法
@api_view(['POST'])
def loginbyapp(request):
    # 考虑到出错的可能性，一开始就设置为
    context = {'status': 400, 'content': 'null'}
    if request.method == "POST":
        # 得到用户上传的数据并进行校验
        username = request.data.get('username', )
        password = request.data.get('password')
        try:
            user = APPUser.maneger.get(username=username, password=password)
            # 用户用户存在的话 则进行登录
            if user:
                context['status'] = 200
        except:
            context['status'] == 400
        if context['status'] == 200:
            serializer = UserSerializer(user)
            context['content'] = serializer.data
        else:
            context['content'] = "null"
        content = JSONRenderer().render(context)
        return HttpResponse(content)
    return HttpResponse(JSONRenderer().render(context))
# 用户注册事件处理/测试成功
@api_view(['POST'])
def register(request):
    context = {'status': 400}
    if request.method == "POST":
        # 获取到对象，之后序列化
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            testuser = APPUser.maneger.filter(username=username)
            if testuser:
                context['status'] = 500
            else:
                user = APPUser.maneger.create(username, password)
                user1=User()
                user1.username=username
                user1.set_password(password)
                user1.save()
                user.save()
                context['status'] = 200
        except Exception:
            context['status'] = 400
        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))


# 以下是课程的增删改查
# 查询用户的所有课程信息
@api_view(['GET'])
def querycourseinfo(request,uid):
    context = {'status': 400, 'content': "null"}
    if request.method == "GET":
        try:
            course = Course.manager.filter(uid=uid)
            # 查询集为空时候
            if course.count() != 0:
                context['status'] = 200
                serialize = serializers.serialize("json", course)
                # 这里先将json对象转化为列表进行存储缺少这一步的话将无法解析。
                context['content'] = json.loads(serialize)
        except Exception:
            context['status'] = 400
        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))


# 更新通过id得到课程信息并进行更新。状态码200表示成功/测试成功
@api_view(['POST'])
def updatecourseInfo(request):
    context = {'status': 400}
    if request.method == "POST":
        # 获取到对象，之后序列化
        cid = request.data.get('cid')
        cname = request.data.get('cname')
        schoolYear = request.data.get('schoolYear')
        term = request.data.get('term')
        credit = request.data.get('credit')
        intstartSection = request.data.get('credit')
        endSection = request.data.get('endSection')
        startWeek = request.data.get('startWeek')
        endWeek = request.data.get('endWeek')
        dayOfWeek = request.data.get('dayOfWeek')
        classroom = request.data.get('classroom')
        teacher = request.data.get('teacher')
        try:
            course = Course.manager.get(cid=cid)
            # 确实存在这个课程
            if course:
                course.cname = cname
                course.schoolYear = schoolYear
                course.term = term
                # 注意类型的转化
                data = ast.literal_eval(credit)
                course.credit = data
                course.intstartSection = intstartSection
                course.endSection = endSection
                course.startWeek = startWeek
                course.endWeek = endWeek
                course.dayOfWeek = dayOfWeek
                course.classroom = classroom
                course.teacher = teacher
                course.save()
                context['status'] = 200
        except Exception as e:
            context['status'] == 400
        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))


# 创建课程的信息/测试成功
@api_view(['POST'])
def createCourse(request):
    context = {'status': 400}
    if request.method == "POST":
        # 获取到对象，之后序列化
        uid = request.data.get('uid')
        cname = request.data.get('cname')
        schoolYear = request.data.get('schoolYear')
        term = request.data.get('term')
        credit = request.data.get('credit')
        intstartSection = request.data.get('credit')
        endSection = request.data.get('endSection')
        startWeek = request.data.get('startWeek')
        endWeek = request.data.get('endWeek')
        dayOfWeek = request.data.get('dayOfWeek')
        classroom = request.data.get('classroom')
        teacher = request.data.get('teacher')
        try:
            user = APPUser.maneger.get(userid=uid)
            if user:
                course = Course.manager.create(cname, schoolYear, term, credit, intstartSection, endSection, startWeek,
                                               endWeek, dayOfWeek, classroom, teacher)
                course.uid_id = user.userid
                course.save()
                context['status'] = 200
            else:
                context['status'] = 400
        except Exception as e:
            context['status'] == 400
        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))

# 删除课程信息/测试成功
@api_view(['GET'])
def deleteCourse(request, cid):
    context = {'status': 400}
    if request.method == "GET":
        try:
            course = Course.manager.get(cid=cid)
            # 查询集不为空时候
            if course:
                course.delete()
                context['status'] = 200
            else:
                context['status'] = 400
        except Exception:
            context['status'] = 400
        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))

