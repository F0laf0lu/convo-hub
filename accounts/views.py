from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, FormView
from django.shortcuts import render
from accounts.models import CustomUser
from .forms import CustomUserCreationForm

# Create your views here.
class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy('signin')


