import string
import random
from import_export import resources
from import_export.fields import Field
from import_export.admin import ExportActionModelAdmin
from django.contrib import admin
from django.contrib.auth.models import Group as DjangoAuthGroup
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe

from .models import Child, School, Group, App, Admin
from .list_filters import CoreGroupsListFilter, SchoolsListFilter

admin.site.site_header = 'KidsPay'
admin.site.site_title = 'KidsPay'
admin.site.unregister(DjangoAuthGroup)


class CustomAdminChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Admin


class CustomUserAdmin(UserAdmin):
    form = CustomAdminChangeForm
    list_display = ('username', 'first_name', 'last_name', 'type', 'school')
    fieldsets = UserAdmin.fieldsets + (
            ('Management', {'fields': ('type', 'school')}),
    )

    list_filter = UserAdmin.list_filter + ('type', )


class ChildForm(forms.ModelForm):
    # monthlyFee = forms.CharField()

    class Meta:
        model = Child
        exclude = ('id', 'child_number', 'school')
        # widgets = {'monthlyFee': forms.TextInput(attrs={'data-mask': "000 000 000.00"})}


class ChildResource(resources.ModelResource):
    def dehydrate_full_name(self, child):
        return child.__str__()

    full_name = Field(column_name='Полное имя')

    class Meta:
        model = Child
        import_id_fields = ['child_number']
        export_order = ['child_number', 'full_name', 'group__name', 'school__name']
        fields = ['child_number', 'full_name', 'group__name', 'school__name']


class ChildAdmin(ExportActionModelAdmin):
    list_display = ('firstName', 'lastName', 'group', 'balance', 'child_number')
    list_filter = (CoreGroupsListFilter, SchoolsListFilter)
    list_display_links = ['firstName', 'lastName']
    search_fields = ('firstName', 'middleName', 'lastName', 'agreementNumber')
    ordering = ('monthlyFee', 'balance', 'id')
    form = ChildForm
    resource_class = ChildResource

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser and request.user.is_authenticated:
            return qs
        if request.user.is_staff and request.user.is_authenticated:
            return qs.filter(school=request.user.school)
        return None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "group":
            if request.user.is_superuser:
                kwargs["queryset"] = Group.objects.all()
            elif request.user.is_staff and request.user.is_authenticated:
                kwargs["queryset"] = Group.objects.filter(school=request.user.school)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.school = request.user.school
            try:
                n = str(int(Child.objects.filter(id__startswith=obj.school.id+':').latest('id').id.split(':')[1]) + 1)
                obj.id = obj.school.id + ':' + n.zfill(4)
                obj.child_number = n
            except ObjectDoesNotExist:
                obj.id = obj.school.id + ':0001'
                obj.child_number = '1'
        super().save_model(request, obj, form, change)


class SchoolAdmin(admin.ModelAdmin):
    exclude = ['id', ]
    readonly_fields = ['logo_preview']
    list_display = ['name', 'address']

    def logo_preview(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.logo.url,
            width=obj.logo.width,
            height=obj.logo.height,
        )
        )

#
# class GroupAdminChangeForm(forms.ModelForm):
#     class Meta:
#         model = Group
#         fields = ('-all', )
#


class GroupAdmin(admin.ModelAdmin):
    exclude = ['id', 'school']
    list_display = ['name', 'fee', 'school']
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
        else:
            for child in obj.children.all():
                child.monthlyFee = obj.fee
                child.save()
        super().save_model(request, obj, form, change)


class AppAdmin(admin.ModelAdmin):
    exclude = ['id', 'token']
    list_display = ['name', 'token']

    def save_model(self, request, obj, form, change):
        if not change:
            token_characters = string.ascii_letters + string.digits + '!#$%()*?@[]_{|}'
            obj.token = ''.join(random.choice(token_characters) for i in range(32))
        super().save_model(request, obj, form, change)


admin.site.register(Child, ChildAdmin)
admin.site.register(Admin, CustomUserAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(App, AppAdmin)
