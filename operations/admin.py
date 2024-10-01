from django.contrib import admin
from .models import Project, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_deleted')
    search_fields = ('name',)
    list_filter = ('is_deleted',)
    filter_horizontal = ('users',)  #'users' is a ManyToManyField


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'due_date', 'is_deleted')
    search_fields = ('title', 'project__name')  # To allow searching by project name
    list_filter = ('status', 'due_date', 'is_deleted')
