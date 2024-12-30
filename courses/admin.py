from django.contrib import admin
from .models import Course, Module, Lesson

class LessonInline(admin.TabularInline):
    model = Lesson

class ModuleInline(admin.TabularInline):
    model = Module

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor')
    search_fields = ('title', 'instructor__username')
    inlines = [ModuleInline]

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ('title', 'course__title')
    inlines = [LessonInline]

admin.site.register(Course, CourseAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lesson)