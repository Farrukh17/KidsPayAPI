from __future__ import absolute_import, unicode_literals
from django.contrib import admin
from .models import Group,School


class GroupsListFilter(admin.SimpleListFilter):
    """
    This filter will always return a subset of the instances in a Model, either filtering by the
    user choice or by a default value.
    """

    # Human-readable title which will be displayed in the right admin sidebar just above the filter options.
    title = 'Группы'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'group'

    default_value = None

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list_of_group = []
        if request.user.is_superuser and request.user.is_authenticated:
            queryset = Group.objects.all()
        elif request.user.is_staff and request.user.is_authenticated:
            queryset = Group.objects.filter(school=request.user.school)
        else:
            queryset = None

        for group in queryset:
            list_of_group.append(
                (str(group.id), group.name)
            )
        return sorted(list_of_group, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(group=self.value())
        else:
            return queryset
'''
    def value(self):
        """
        Overriding this method will allow us to always have a default value.
        """
        value = super(GroupsListFilter, self).value()
        if value is None:
            if self.default_value is None:
                # If there is at least one Group, return the first by name. Otherwise, None.
                first_group = Group.objects.order_by('name').first()
                value = None if first_group is None else first_group.id
                self.default_value = value
            else:
                value = self.default_value
        return str(value)
'''


class SchoolsListFilter(admin.SimpleListFilter):
    """
    This filter will always return a subset of the instances in a Model, either filtering by the
    user choice or by a default value.
    """

    # Human-readable title which will be displayed in the right admin sidebar just above the filter options.
    title = 'Детские садики'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'school'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list_of_schools = []
        if request.user.is_superuser and request.user.is_authenticated:
            queryset = School.objects.all()
        elif request.user.is_staff and request.user.is_authenticated:
            queryset = School.objects.filter(id=request.user.school.id)
        else:
            queryset = None

        for school in queryset:
            list_of_schools.append(
                (str(school.id), school.name)
            )
        return sorted(list_of_schools, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(school=self.value())
        else:
            return queryset
