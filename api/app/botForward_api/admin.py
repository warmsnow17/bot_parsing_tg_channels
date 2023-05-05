from django.contrib import admin
from django.utils.html import format_html

from .models import Media, Post, Settings

from .models import Channel


class ChannelInline(admin.TabularInline):
    model = Channel
    fields = ('telegram_id', 'name')


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('forwarding',)
    inlines = [ChannelInline,]

    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        else:
            return True


admin.site.register(Settings, SettingsAdmin)





class MediaInline(admin.TabularInline):
    model = Media
    fields = ('file', )
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'is_verified',)
    search_fields = ('text',)
    list_filter = ('is_verified',)
    inlines = [MediaInline, ]


admin.site.register(Post, PostAdmin)


class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_media', 'post')
    search_fields = ('post',)
    list_filter = ('post',)

    def get_media_type(self, file_name):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            return 'image'
        elif file_name.lower().endswith(('.mp4', '.mkv')):
            return 'video'
        else:
            return None

    def display_media(self, obj):
        if self.get_media_type(obj.file.name) == 'image':
            return format_html('<img src="{}" width="50" height="50" />',
                               obj.file.url)
        elif self.get_media_type(obj.file.name) == 'video':
            return format_html('<video width="100" height="100" controls><source src="{}" type="video/mp4"></video>',
                               obj.file.url)
        return "No media"

    display_media.short_description = 'Media'

    readonly_fields = ('display_media',)


admin.site.register(Media, MediaAdmin)

