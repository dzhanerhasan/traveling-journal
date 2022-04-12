from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import CreateView, UpdateView, DeleteView

from finalProject.checklist.models import CheckList, ListItems


@login_required
def checklist_page(request):
    checklists = CheckList.objects.filter(author=request.user)

    paginator = Paginator(checklists, 9)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'checklists': checklists,
        'posts': posts,
    }

    return render(request, 'checklist/checklists.html', context)


@login_required
def checklist_details(request, pk):

    # Filter items by user and checklist
    checklist = CheckList.objects.get(pk=pk)
    plans = ListItems.objects.filter(checklist__pk=pk)
    current_user = None

    if plans:
        current_user = plans[0].checklist.author

        if request.user != current_user:
            return redirect('home page')

    # Add new item to the list
    if request.method == "POST":
        content = request.POST

        ListItems.objects.create(
            user=request.user,
            checklist=checklist,
            content=content['content'],
        )

        return redirect('details list', checklist.pk)

    # Filter active and completed plans
    status = request.GET.get('status')

    if status == 'Completed':
        plans = plans.filter(completed=True)
    elif status == 'Active':
        plans = plans.filter(completed=False)

    paginator = Paginator(plans, 9)
    page = request.GET.get('page')

    # paginate
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'checklist_name': checklist.title,
        'checklist_pk': pk,
        'plans': plans,
        'posts': posts,
    }

    return render(request, 'checklist/checklist_page.html', context)


class CheckListCreateView(LoginRequiredMixin, CreateView):
    model = CheckList
    fields = ['title']
    template_name = 'checklist/create_checklist.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CheckListEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CheckList
    fields = ['title']
    template_name = 'checklist/edit_checklist.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        album = self.get_object()
        if self.request.user == album.author:
            return True
        return False


class CheckListDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CheckList
    template_name = 'checklist/delete_list.html'
    success_url = reverse_lazy('checklist')

    def test_func(self):
        album = self.get_object()
        if self.request.user == album.author:
            return True
        return False


@login_required
def delete_plan(request, pk):
    plan = ListItems.objects.get(pk=pk)
    list_page = plan.checklist.pk
    plan.delete()
    return redirect('details list', list_page)


@login_required
def complete_plan(request, pk):
    plan = ListItems.objects.get(pk=pk)
    list_page = plan.checklist.pk
    plan.completed = True
    plan.save()
    return redirect('details list', list_page)


@login_required
def active_plan(request, pk):
    plan = ListItems.objects.get(pk=pk)
    list_page = plan.checklist.pk
    plan.completed = False
    plan.save()
    return redirect('details list', list_page)
