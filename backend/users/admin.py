from django.contrib import admin
from users.models import Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('id', 'user')
    empty_value_display = '-NONE-'
