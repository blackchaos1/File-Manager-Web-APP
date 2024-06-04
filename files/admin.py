from django.utils.timezone import localtime
from django.contrib import admin
from .models import UserFile, Company, UserProfile
import os
admin.site.register(Company)
admin.site.register(UserProfile)

class UserFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'formatted_uploaded_at')
    readonly_fields = ('uploaded_at',)
    search_fields = ('user__username', 'file', 'uploaded_at')

    actions = ['delete_files']

    def formatted_uploaded_at(self, obj):
        return localtime(obj.uploaded_at).strftime('%Y-%m-%d %H:%M:%S')
    formatted_uploaded_at.short_description = 'Uploaded At'

    def delete_files(self, request, queryset):
        for obj in queryset:
            if os.path.isfile(obj.file.path):
                os.remove(obj.file.path)
            obj.delete()
        self.message_user(request, "Selected files have been deleted.")
    delete_files.short_description = "Delete selected files and remove from directory"

admin.site.register(UserFile, UserFileAdmin)
