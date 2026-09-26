from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView

from .forms import AssignmentForm, SignUpForm
from .models import Assignment


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created. You can log in now.')
        return response


@login_required
def assignment_list(request):
    assignments = Assignment.objects.filter(user=request.user)

    status = request.GET.get('status')
    if status == 'completed':
        assignments = assignments.filter(completed=True)
    elif status == 'pending':
        assignments = assignments.filter(completed=False)

    return render(request, 'assignments/assignment_list.html', {
        'assignments': assignments,
        'status': status or 'all',
        'today': timezone.localdate(),
    })


@login_required
def assignment_create(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.user = request.user
            assignment.save()
            messages.success(request, 'Assignment added.')
            return redirect('assignment_list')
    else:
        form = AssignmentForm()
    return render(request, 'assignments/assignment_form.html', {'form': form, 'title': 'Add Assignment'})


@login_required
def assignment_edit(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment updated.')
            return redirect('assignment_list')
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'assignments/assignment_form.html', {'form': form, 'title': 'Edit Assignment'})


@login_required
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Assignment deleted.')
        return redirect('assignment_list')
    return render(request, 'assignments/assignment_confirm_delete.html', {'assignment': assignment})


@login_required
def assignment_toggle(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    assignment.completed = not assignment.completed
    assignment.save()
    return redirect('assignment_list')
