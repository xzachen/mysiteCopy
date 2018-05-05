from django.contrib import admin
from myapp.models import Note,CollectionNote,APPUser,Course

class CourseAdmin(admin.ModelAdmin):
    list_filter = ['cname','cid','uid']
    search_fields = ['cname','cid','uid']  # 添加快速查询栏

admin.site.register(Note)
admin.site.register(CollectionNote)
admin.site.register(APPUser)
admin.site.register(Course, CourseAdmin)