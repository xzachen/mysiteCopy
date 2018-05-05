from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    # 设置级联关系。
    # 笔记的主键
    nid=models.AutoField(primary_key=True)
    category =models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    content =RichTextUploadingField()
    # 文章的拥有者
    auther=models.ForeignKey(User,on_delete=models.CASCADE,)
    # 可以创建笔记的时候添加描述
    meta_description = models.TextField()
    is_published=models.BooleanField(default=False)
    class Meta:
        # 设置表名字
        db_table = 'note'
        ordering=['-date']

class CollectionNote(models.Model):
    cnid = models.AutoField(primary_key=True)
    cuser = models.ForeignKey(User, on_delete=models.CASCADE,)
    noteid= models.IntegerField()
    class Meta:
        ordering=['-cnid']

class APPUserManager(models.Manager):
    def create(self, username, password, ):
        user = APPUser()
        user.username = username
        user.password = password
        return user

class APPUser(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=40)
    # 创建元数据
    class Meta:
        ordering = ['userid']
        db_table = 'appuser'
    maneger = APPUserManager()

# 课程的管理类主要用于创建课程。
class CourseManager(models.Manager):
    def create(self, cname, schoolYear,term, credit,intstartSection,endSection,startWeek,endWeek,dayOfWeek,classroom,teacher):
        course = Course()
        course.cname = cname
        course.schoolYear = schoolYear
        course.term = term
        course.credit = credit
        course.intstartSection = intstartSection
        course.endSection = endSection
        course.startWeek = startWeek
        course.endWeek = endWeek
        course.dayOfWeek = dayOfWeek
        course.classroom = classroom
        course.teacher = teacher
        return course

# 创建课程类的数据表
class Course(models.Model):
    uid = models.ForeignKey('APPUser',on_delete=models.CASCADE,)
    cid = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=20)
    schoolYear = models.CharField(max_length=20)
    term = models.CharField(max_length=20)
    credit = models.FloatField()
    intstartSection = models.IntegerField()
    endSection = models.IntegerField()
    startWeek = models.IntegerField()
    endWeek = models.IntegerField()
    dayOfWeek = models.IntegerField()
    classroom = models.CharField(max_length=20)
    teacher = models.CharField(max_length=20)

    class Meta:
        ordering = ['cid']
        # 设置表名字
        db_table = 'appcourse'
    # 创建管理类。
    manager=CourseManager()
