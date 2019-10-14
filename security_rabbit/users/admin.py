from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# https://kuanyui.github.io/2015/02/06/django-customize-user-model/
class CustomUserAdmin(UserAdmin):
    list_display = ('id','companyName','username','email','is_staff','is_active','is_superuser','last_login','companyURL')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('email', 'companyName', 'companyURL')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )

    USERNAME_FIELD = 'companyName'

admin.site.register(User, CustomUserAdmin)