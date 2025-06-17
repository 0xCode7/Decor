from django.contrib import admin
from django.contrib.auth.models import User

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile_number', 'date_of_birth')


class ProfileInline(admin.StackedInline):  # or TabularInline
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


# Unregister the original User admin
admin.site.unregister(User)

# Re-register with the custom admin
admin.site.register(User, UserAdmin)
