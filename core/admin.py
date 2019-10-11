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
    list_display = ('child_number', 'firstName', 'lastName', 'group', 'debt')
    list_filter = ('group', 'debt')
    list_display_links = ['child_number', 'firstName', 'lastName']
    exclude = ('id', 'child_number')
    search_fields = ('firstName', 'middleName', 'lastName', 'agreementNumber')
    ordering = ('monthlyFee', 'debt', 'id')


class SchoolAdmin(admin.ModelAdmin):
    exclude = ['id', ]

#
# class GroupAdminChangeForm(forms.ModelForm):
#     class Meta:
#         model = Group
#         fields = ('-all', )
#     # TODO filter groups by Director's school id
#     # TODO when creating a group implicitly assign school from director/accountant's obj.school
#     # TODO django admin site async change form field according to other field's value
#


class GroupAdmin(admin.ModelAdmin):
    exclude = ['id', ]


admin.site.register(Admin, CustomUserAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(App)
