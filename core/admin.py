import string
import random
from import_export import resources
from import_export.fields import Field
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin, ExportMixin
from import_export.formats.base_formats import DEFAULT_FORMATS, XLS, XLSX
from django.contrib import admin
from django.contrib.auth.models import Group as DjangoAuthGroup
from django import forms
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django.utils.formats import number_format
from django.utils.translation import ugettext_lazy as _

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
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Management'), {'fields': ('type', 'school')}),
    )

    list_filter = UserAdmin.list_filter + ('type', )

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'user_permissions':
            qs = kwargs.get('queryset', db_field.remote_field.model.objects)
            qs = qs.exclude(codename__in=(
                'add_permission',
                'change_permission',
                'delete_permission',
                'view_permission',

                'add_contenttype',
                'change_contenttype',
                'delete_contenttype',
                'view_contenttype',

                'add_session',
                'delete_session',
                'change_session',
                'view_session',

                'add_logentry',
                'change_logentry',
                'delete_logentry',
                'view_logentry',

                # 'add_group',
                # 'change_group',
                # 'delete_group',
                # 'view_group',
            ))
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
            kwargs['queryset'] = qs.select_related('content_type')
        return super(CustomUserAdmin, self).formfield_for_manytomany(db_field, request=request, **kwargs)


class ExportModelAdmin(ExportMixin, admin.ModelAdmin):
    """
    Subclass of ModelAdmin with import/export functionality.
    """
    formats = (
        XLS,
        XLSX,
    )


class ChildResource(resources.ModelResource):
    def dehydrate_full_name(self, child):
        return child.__str__()

    def dehydrate_group(self, child):
        return child.group

    def dehydrate_school(self, child):
        return child.school

    def dehydrate_balance(self, child):
        return number_format(child.balance, 0) + ' UZS'

    def dehydrate_child_number(self, child):
        return child.child_number

    full_name = Field(column_name='Полное имя')
    group = Field(column_name='Группа')
    school = Field(column_name='Детский садик')
    child_number = Field(column_name='Воспитанник ID')
    balance = Field(column_name='Баланс')

    class Meta:
        model = Child
        import_id_fields = ['id']
        export_order = ['child_number', 'full_name', 'balance', 'group', 'school']
        fields = ['child_number', 'full_name', 'group', 'school', 'balance']


class ChildAdmin(ExportModelAdmin):
    list_display = ('firstName', 'lastName', 'group', 'balance', 'child_number')
    list_filter = [SchoolsListFilter, CoreGroupsListFilter]
    list_display_links = ['firstName', 'lastName']
    search_fields = ('firstName', 'middleName', 'lastName', 'agreementNumber')
    ordering = ('monthlyFee', 'balance', 'id')
    exclude = ['id', 'child_number', 'school']
    resource_class = ChildResource

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.user.is_superuser:
            if 'status' in self.exclude:
                self.exclude.remove('status')
        else:
            if 'status' not in self.exclude:
                self.exclude.append('status')
        return super().change_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        if request.user.is_superuser:
            if 'status' in self.exclude:
                self.exclude.remove('status')
        else:
            if 'status' not in self.exclude:
                self.exclude.append('status')
        return super().add_view(request, form_url, extra_context)

    def get_list_filter(self, request):
        if request.user.is_superuser:
            if 'status' not in self.list_filter:
                self.list_filter.insert(0, 'status')
        else:
            if 'status' in self.list_filter:
                self.list_filter.remove('status')

        return self.list_filter

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser and request.user.is_authenticated:
            return qs
        if request.user.is_staff and request.user.is_authenticated:
            return qs.filter(school=request.user.school, status=Child.CHILD_STATUSES[0][0])
        return None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "group":
            if request.user.is_superuser:
                kwargs["queryset"] = Group.objects.all()
            elif request.user.is_staff and request.user.is_authenticated:
                kwargs["queryset"] = Group.objects.filter(school=request.user.school, status=Group.GROUP_STATUSES[0][0])
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

    def delete_model(self, request, obj):
        obj.status = Child.CHILD_STATUSES[1][0]
        obj.save()

    def delete_queryset(self, request, queryset):
        for child in queryset:
            child.status = Child.CHILD_STATUSES[1][0]
            child.save()


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

    def delete_queryset(self, request, queryset):
        for school in queryset:
            if school.logo != School.DEFAULT_LOGO:
                school.logo.delete()
        super().delete_queryset(request, queryset)

    def delete_model(self, request, obj):
        if obj.logo != School.DEFAULT_LOGO:
            obj.logo.delete()
        super().delete_model(request, obj)


class GroupAdmin(admin.ModelAdmin):
    exclude = ['id', 'school']
    list_display = ['name', 'fee', 'school']
    list_filter = [SchoolsListFilter, ]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.user.is_superuser:
            if 'status' in self.exclude:
                self.exclude.remove('status')
        else:
            if 'status' not in self.exclude:
                self.exclude.append('status')
        return super().change_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        if request.user.is_superuser:
            if 'status' in self.exclude:
                self.exclude.remove('status')
        else:
            if 'status' not in self.exclude:
                self.exclude.append('status')
        return super().add_view(request, form_url, extra_context)

    def get_list_filter(self, request):
        if request.user.is_superuser:
            if 'status' not in self.list_filter:
                self.list_filter.append('status')
        else:
            if 'status' in self.list_filter:
                self.list_filter.remove('status')

        return self.list_filter

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser and request.user.is_authenticated:
            return qs
        if request.user.is_staff and request.user.is_authenticated:
            return qs.filter(school=request.user.school, status=Group.GROUP_STATUSES[0][0])
        return None

    def save_model(self, request, obj, form, change):
        if not change:
            obj.school = request.user.school
        else:
            for child in obj.children.filter(status=Child.CHILD_STATUSES[0][0]):
                child.monthlyFee = obj.fee
                child.save()
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        for child in obj.children.filter(status=Child.CHILD_STATUSES[0][0]):
            child.status = Child.CHILD_STATUSES[1][0]
            child.save()
        obj.status = Group.GROUP_STATUSES[1][0]
        obj.save()

    def delete_queryset(self, request, queryset):
        for group in queryset:
            for child in group.children.filter(status=Child.CHILD_STATUSES[0][0]):
                child.status = Child.CHILD_STATUSES[1][0]
                child.save()
            group.status = Group.GROUP_STATUSES[1][0]
            group.save()


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
