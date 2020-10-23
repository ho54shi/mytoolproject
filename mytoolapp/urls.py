from django.urls import path
from .views import signupview, loginview, projectsview, projectdetailview, ProjectCreateClass, labelview, indexview
from .views import labellingview, LabelCreateClass, logoutview, AnnotationCreateClass
from .views import annsview, anndetailview, ProjectDeleteClass, LabelDeleteClass, LabelUpdateClass
from .views import AnnotationDeleteClass
urlpatterns = [
    path('', indexview, name='index'),
    path('signup/', signupview, name='signup'),
    path('login/', loginview, name='login'),
    path('projects/', projectsview, name='projects'),
    path('projects/<int:pk>/', projectdetailview, name='project_detail'),
    path('projects/create/', ProjectCreateClass.as_view(), name='project_create'),
    path('projects/<int:pk>/delete/',
         ProjectDeleteClass.as_view(), name='project_delete'),

    path('projects/<int:pk>/label', labelview, name='label'),
    path('projects/<int:pk>/create_label',
         LabelCreateClass.as_view(), name='label_create'),
    path('projects/<int:pk>/label/<int:label_pk>/update',
         LabelUpdateClass.as_view(), name='label_update'),
    path('projects/<int:pk>/label/<int:label_pk>/delete',
         LabelDeleteClass.as_view(), name='label_delete'),

    path('projects/<int:pk>/work',
         AnnotationCreateClass.as_view(), name='submit'),
    path('projects/<int:pk>/work', labellingview, name='work'),
    path('anns/', annsview, name='anns'),
    path('anns/<int:pk>', anndetailview, name='ann_detail'),
    path('anns/<int:pk>/delete', AnnotationDeleteClass.as_view(), name='ann_delete'),
    path('logout/', logoutview, name='logout'),

]
