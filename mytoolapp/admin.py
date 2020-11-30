from django.contrib import admin
from .models import ProjectModel, LabelModel, AnnotationModel, SentenceModel
from django.contrib.auth.admin import UserAdmin
from .models import CustomeUser
from guardian.admin import GuardedModelAdmin
# Register your models here.


class CustomeUserAdmin(UserAdmin):
    model = CustomeUser
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('expert',)}),)
    list_display = ['username', 'email', 'expert']


class ProjectAdmin(GuardedModelAdmin):
    pass


admin.site.register(CustomeUser, CustomeUserAdmin)

admin.site.register(ProjectModel, ProjectAdmin)
admin.site.register(LabelModel)
admin.site.register(AnnotationModel)
admin.site.register(SentenceModel)
