from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from .models import Message, Mailing, Client, MailingAttempt
from .forms import MessageForm, MailingForm
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic import TemplateView
from django.db.models import Count, Q
import logging

logger = logging.getLogger(__name__)
CustomUser = get_user_model()

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

@user_passes_test(is_manager)
@login_required
def mailing_list(request):
    mailings = Mailing.objects.all()
    return render(request, 'mailing_list.html', {'mailings': mailings})


@login_required
@user_passes_test(is_manager)
def block_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    return redirect('mailings:view_users')

@login_required
@user_passes_test(is_manager)
@require_POST
def disable_mailing(request, mailing_id):
    mailing = get_object_or_404(Mailing, id=mailing_id)
    mailing.status = 'DISABLED'
    mailing.save()
    return redirect('mailings:manager_mailing_list')

# User views
@login_required
@user_passes_test(is_manager)
def view_users(request):
    users = User.objects.all()
    return render(request, 'mailings/users.html', {'users': users})

# Existing views for messages and mailings
@method_decorator(login_required, name='dispatch')
class MessageListView(ListView):
    model = Message
    template_name = 'mailings/messages.html'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)

@method_decorator(login_required, name='dispatch')
class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailings/message_detail.html'
    
    def get_object(self):
        return get_object_or_404(Message, pk=self.kwargs['pk'], owner=self.request.user)

@method_decorator(login_required, name='dispatch')
class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:message_list')

    def get_object(self):
        return get_object_or_404(Message, pk=self.kwargs['pk'], owner=self.request.user)

@method_decorator(login_required, name='dispatch')
class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailings/message_confirm_delete.html'
    success_url = reverse_lazy('mailings:message_list')

    def get_object(self):
        return get_object_or_404(Message, pk=self.kwargs['pk'], owner=self.request.user)

@method_decorator(login_required, name='dispatch')
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Mailing.objects.filter(owner=user.pk)
        return Mailing.objects.none()

@method_decorator(login_required, name='dispatch')
class MailingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'

    def get_object(self):
        mailing = get_object_or_404(Mailing, pk=self.kwargs['pk'])
        return mailing

    def test_func(self):
        mailing = self.get_object()
        return self.request.user == mailing.owner or self.request.user.groups.filter(name='Manager').exists()

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied()
        return redirect(reverse('login') + '?next=' + self.request.path)


@method_decorator(login_required, name='dispatch')
class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Установка владельца рассылки
        logger.info(f"Создание рассылки пользователем {self.request.user}: {form.cleaned_data}")
        response = super().form_valid(form)
        logger.info(f"Рассылка успешно создана: {self.object}")
        # Добавьте здесь любые действия, которые должны быть выполнены после сохранения формы
        return response

    def form_invalid(self, form):
        logger.error(f"Ошибка при создании рассылки: {form.errors}")
        return super().form_invalid(form)

@method_decorator(login_required, name='dispatch')
class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def get_object(self):
        mailing = get_object_or_404(Mailing, pk=self.kwargs['pk'])
        return mailing

    def test_func(self):
        mailing = self.get_object()
        return self.request.user == mailing.owner or self.request.user.groups.filter(name='Manager').exists()

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied()
        return redirect(reverse('login') + '?next=' + self.request.path)


@method_decorator(login_required, name='dispatch')
class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def get_object(self):
        mailing = get_object_or_404(Mailing, pk=self.kwargs['pk'])
        return mailing

    def test_func(self):
        mailing = self.get_object()
        return self.request.user == mailing.owner or self.request.user.groups.filter(name='Manager').exists()

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied()
        return redirect(reverse('login') + '?next=' + self.request.path)
    
@login_required
@require_POST
def block_user(request, pk):
    if not request.user.groups.filter(name='Менеджер').exists():
        return HttpResponseForbidden()

    user = get_object_or_404(CustomUser, pk=pk)
    user.is_active = False
    user.save()
    return redirect('mailings:mailing_list')

@method_decorator(login_required, name='dispatch')
class MailingDisableView(UpdateView):
    model = Mailing
    fields = []
    template_name = 'mailings/mailing_confirm_disable.html'
    success_url = reverse_lazy('mailings:manager_mailing_list')

    def post(self, request, *args, **kwargs):
        mailing = self.get_object()
        if not is_manager(request.user):
            return HttpResponseForbidden()

        mailing.status = 'DISABLED'
        mailing.save()
        return redirect(self.success_url)
    
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_manager), name='dispatch')
class ManagerMailingListView(ListView):
    model = Mailing
    template_name = 'mailings/manager_mailing_list.html'
    context_object_name = 'mailings'

    def test_func(self):
        return is_manager(self.request.user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied()
        return redirect(reverse('login') + '?next=' + self.request.path)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("Using template: ", self.template_name)  # Отладочный вывод
        print("Mailings: ", context['mailings'])  # Отладочный вывод
        return context


class MailingReportView(ListView):
    model = Mailing
    template_name = 'mailings/mailing_report.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        queryset = Mailing.objects.annotate(
            total_attempts=Count('mailingattempt'),
            successful_attempts=Count('mailingattempt', filter=Q(mailingattempt__status='COMPLETED')),
            failed_attempts=Count('mailingattempt', filter=Q(mailingattempt__status='ошибка'))
        )
        # Добавим вывод для отладки
        print(f"Queryset: {queryset}")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_attempts'] = MailingAttempt.objects.all()
        # Добавим вывод для отладки
        print(f"Mailing Attempts: {context['mailing_attempts']}")
        return context