from django.contrib import admin
from .models import User, OtpCode
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['phone_number', 'first_name', 'is_admin']
    list_filter = ['is_admin', 'phone_number']
    readonly_fields = ['last_login']

    fieldsets = (
        (
            None, {
                'fields': (
                    'phone_number',
                    'first_name',
                    'password',
                    'birth_date',
                    'picture',
                )
            }
        ),
        (
            'Permissions', {
                'fields': (
                    'is_active',
                    'is_admin',
                    'last_login',
                    # 'created',
                )
            }
        ),
    )

    add_fieldsets = (
        (
            None, {
                'fields': (
                    'phone_number',
                    'first_name',
                    'last_name',
                    'birth_date',
                    'picture',
                    'password1',
                    'password2',
                )
            }
        ),
    )

    search_fields = ['phone_number', 'first_name', 'last_name']
    ordering = ('phone_number',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(OtpCode)
admin.site.unregister(Group)
