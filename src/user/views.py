from typing import Dict

from basis.decorators import parse_request_body
from basis.exceptions import AppException
from basis.validators import validate_n_format_phone, validate_personal_id
from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from django.views.generic import View

from . import decorators, error_codes, messages
from .forms import RegistrationForm
from .models import InviteCode, User
from .param_models import FillProfile, Login, Signup


# @ensure_csrf_cookie
def register_page(request: HttpRequest):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('admin:index'))  # Redirect to admin page
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})
