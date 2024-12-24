from django.contrib import admin
from .models import Category,News,Comment
from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject')



admin.site.register(Category)

class AdminNews(admin.ModelAdmin):
    list_display=('title','category','add_time')

admin.site.register(News,AdminNews)

class AdminComment(admin.ModelAdmin):
    list_display=('news','email','comment','status')
admin.site.register(Comment,AdminComment)
