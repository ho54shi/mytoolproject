from django.contrib import admin
from .models import ProjectModel, LabelModel, AnnotationModel
from django.contrib.auth.admin import UserAdmin
from .models import CustomeUser
# Register your models here.


class CustomeUserAdmin(UserAdmin):
    model = CustomeUser
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('expert',)}),)
    list_display = ['username', 'email', 'expert']


admin.site.register(CustomeUser, CustomeUserAdmin)

admin.site.register(ProjectModel)
admin.site.register(LabelModel)
admin.site.register(AnnotationModel)
