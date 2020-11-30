from django.urls import path
from .views import signupview, loginview, projectsview, projectdetailview, ProjectCreateClass, labelview, indexview
from .views import labellingview, LabelCreateClass, logoutview, AnnotationCreateClass
from .views import annsview, anndetailview, ProjectDeleteClass, LabelDeleteClass, LabelUpdateClass
from .views import AnnotationDeleteClass, ProjectUpdateClass
from .views import trainview, train_done_view
from .views import AnnotationExport
from .views import sentences_create_view
urlpatterns = [
    path('', indexview, name='index'),
    path('signup/', signupview, name='signup'),
    path('login/', loginview, name='login'),
    path('projects/', projectsview, name='projects'),
    path('projects/<int:pk>/', projectdetailview, name='project_detail'),
    path('projects/create/', ProjectCreateClass.as_view(), name='project_create'),
    path('projects/create/sentences_create',
         sentences_create_view, name='sentences_create'),
    path('projects/<int:pk>/update',
         ProjectUpdateClass.as_view(), name='project_update'),
    path('projects/<int:pk>/delete/',
         ProjectDeleteClass.as_view(), name='project_delete'),

    path('projects/<int:pk>/label', labelview, name='label'),
    path('projects/<int:pk>/create_label',
         LabelCreateClass.as_view(), name='label_create'),
    path('projects/<int:pk>/label/<int:label_pk>/update',
         LabelUpdateClass.as_view(), name='label_update'),
    path('projects/<int:pk>/label/<int:label_pk>/delete',
         LabelDeleteClass.as_view(), name='label_delete'),

    path('projects/<int:pk>/work/<int:sentence_pk>',
         AnnotationCreateClass.as_view(), name='submit'),
    path('projects/<int:pk>/work', labellingview, name='work'),
    path('anns/', annsview, name='anns'),
    path('anns/export', AnnotationExport, name="ann_export"),
    path('anns/<int:pk>', anndetailview, name='ann_detail'),
    path('anns/<int:pk>/delete', AnnotationDeleteClass.as_view(), name='ann_delete'),
    path('train/', trainview, name='train'),
    path('train/done/', train_done_view, name='train_done'),
    path('logout/', logoutview, name='logout'),

]
