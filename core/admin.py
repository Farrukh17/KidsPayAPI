from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import Child, School, Group, App, Admin

admin.site.site_header = 'KidsPay'


class CustomAdminChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Admin


class CustomUserAdmin(UserAdmin):
    form = CustomAdminChangeForm

    fieldsets = UserAdmin.fieldsets + (
            ('Management', {'fields': ('type', 'school')}),
    )

    list_filter = UserAdmin.list_filter + ('type', )


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('firstName', 'lastName', 'debt')
    list_filter = ('id', 'debt')
    search_fields = ('firstName', 'middleName', 'lastName', 'agreementNumber')
    ordering = ('monthlyFee', 'debt', 'id')


class SchoolAdmin(admin.ModelAdmin):
    exclude = ['id', ]


admin.site.register(Admin, CustomUserAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Group)
admin.site.register(App)
