from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from data_pull.forms import RegistrationForm
from data_pull.helpers import fetch_new_records
from common.logging_helper import api_logging

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_endpoint = 'show-records'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Welcome, {self.request.user.username}!')
        return redirect(self.redirect_endpoint)

class CustomLogoutView(LogoutView):
    next_page = 'login'

class RegisterView(View):
    template_name = 'register.html'
    form_class = RegistrationForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('show-records')
        return render(request, self.template_name, {'form': form})

class ShowRecordsView(View):
    template_name = 'show_records.html'

    def get(self, request):
        try:
            if not request.user.is_authenticated:
                return redirect("login")
            
            api_logging.logger.info("API hit for show records %s", str(request))
            template_data = fetch_new_records(request)

            return render(request, self.template_name, template_data)
        except Exception as e:
            api_logging.logger.exception(e)
            return render(request, "internal_error.html")
