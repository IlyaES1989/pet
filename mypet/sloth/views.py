from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Report

from datetime import datetime

@login_required
def index(request):

    response = render(request, 'sloth/index.html',)

    return response


