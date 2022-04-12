from django.urls import path

from finalProject.checklist.views import CheckListCreateView, checklist_page, checklist_details, CheckListEditView, \
    CheckListDeleteView, delete_plan, complete_plan, active_plan

urlpatterns = [
    path('', checklist_page, name='checklist'),

    path('<int:pk>', checklist_details, name='details list'),
    path('create/', CheckListCreateView.as_view(), name='create list'),
    path('edit/<int:pk>', CheckListEditView.as_view(), name='edit list'),
    path('delete/<int:pk>', CheckListDeleteView.as_view(), name='delete list'),

    path('plan/delete/<int:pk>', delete_plan, name='delete plan'),
    path('plan/complete/<int:pk>', complete_plan, name='complete plan'),
    path('plan/activate/<int:pk>', active_plan, name='active plan'),

]