import string
import random
from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import Child, School, Group, App, Admin
from .list_filters import GroupsListFilter, SchoolsListFilter

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


class ChildAdmin(admin.ModelAdmin):
    list_display = ('child_number', 'firstName', 'lastName', 'group', 'debt')
    list_filter = (GroupsListFilter, )
    list_display_links = ['child_number', 'firstName', 'lastName']
    exclude = ('id', 'child_number', 'school')
    search_fields = ('firstName', 'middleName', 'lastName', 'agreementNumber')
    ordering = ('monthlyFee', 'debt', 'id')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser and request.user.is_authenticated:
            return qs
        if request.user.is_staff and request.user.is_authenticated:
            return qs.filter(school=request.user.school)
        return None

    def save_model(self, request, obj, form, change):
        if not change:
            obj.school = request.user.school
            super().save_model(request, obj, form, change)


class SchoolAdmin(admin.ModelAdmin):
    exclude = ['id', ]

#
# class GroupAdminChangeForm(forms.ModelForm):
#     class Meta:
#         model = Group
#         fields = ('-all', )
#     # TODO django admin site async change form field according to other field's value
#


class GroupAdmin(admin.ModelAdmin):
    exclude = ['id', 'school']
    list_filter = [SchoolsListFilter, ]

    # def get_changeform_initial_data(self, request):
    #     return {'school': request.user.school}

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser and request.user.is_authenticated:
            return qs
        if request.user.is_staff and request.user.is_authenticated:
            return qs.filter(school=request.user.school)
        return None

    # def add_view(self, request, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['school'] = request.user.school.id
    #     return super(GroupAdmin, self).add_view(request, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.school = request.user.school
            super().save_model(request, obj, form, change)


class AppAdmin(admin.ModelAdmin):
    exclude = ['id', 'token']
    list_display = ['name', 'token']

    def save_model(self, request, obj, form, change):
        if not change:
            password_characters = string.ascii_letters + string.digits + string.punctuation
            obj.token = ''.join(random.choice(password_characters) for i in range(32))
            super().save_model(request, obj, form, change)


admin.site.register(Child, ChildAdmin)
admin.site.register(Admin, CustomUserAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(App, AppAdmin)
