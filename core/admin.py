from django.contrib import admin
from .models import Child, School, Group, App


admin.site.register(School)
admin.site.register(Group)
admin.site.register(App)


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('firstName', 'lastName', 'debt')
    # exclude = ('id', 'school')
    list_filter = ('id', 'debt')
    search_fields = ('firstName', 'middleName', 'lastName', 'agreementNumber')
    ordering = ('monthlyFee', 'debt', 'id')

