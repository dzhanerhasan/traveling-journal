from django.urls import path

from finalProject.checklist.views import CheckListCreateView, checklist_page, checklist_details, CheckListEditView, \
    CheckListDeleteView

urlpatterns = [
    path('', checklist_page, name='checklist'),

    path('<int:pk>', checklist_details, name='details list'),
    path('create/', CheckListCreateView.as_view(), name='create list'),
    path('edit/<int:pk>', CheckListEditView.as_view(), name='edit list'),
    path('delete/<int:pk>', CheckListDeleteView.as_view(), name='delete list'),
]