
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Report, PreparationFile, Outcome
from .forms import ReportForm, PreparationFileForm

import re


@login_required
def index(request):

    if request.method == 'GET':
        user = User.objects.get(username=request.user.username)
        r_form = ReportForm()
        p_form = PreparationFileForm()

        item = request.session.get('type_of_report', None)

        if item:
            preparing_files = PreparationFile.objects.filter(user=user, item=item)
            for file in preparing_files:
                short_name = re.split(r'/', file.ready_file.name)[-1]
                file.ready_file.short_name = short_name

            outcome = Outcome.objects.filter(user=user, report=item)
            for file in outcome:
                short_name = re.split(r'/', file.file.name)[-1]
                file.file.short_name = short_name
                file.time_str = str(file.time)[:19]
        else:
            preparing_files = None
            outcome = None
        context_dict = {
            'r_form': r_form,
            'p_form': p_form,
            'preparing_files': preparing_files,
            'outcome': outcome,
        }
    else:
        context_dict = {
            'r_form': None,
            'p_form': None,
            'preparing_files': None,
            'outcome': None,
        }

    response = render(request, 'sloth/index.html', context_dict)
    return response


def adjust(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        item = Report.objects.get(user=user, item=request.POST['item'])

        form = ReportForm(request.POST, request.FILES)
        last_year = request.FILES.get('last_year', Report.objects.get(user=user, item=request.POST['item']).last_year)


        if form.is_valid():
            Report.objects.update_or_create(
                user=user,
                item=request.POST['item'],
                defaults={'last': request.FILES['last'],
                          'last_year': last_year,
                          'month': request.POST['month'],
                          'year': request.POST['year'],
                          'open_last_report': (request.POST['open_last_report']), })

        raw_data_form = PreparationFileForm(request.FILES)
        files = request.FILES.getlist('primarily_file')


        if raw_data_form.is_valid():
            rubbish = PreparationFile.objects.filter(user=user, item=item)
            rubbish.delete()
            for f in files:
                PreparationFile.objects.create(user=user, item=item, primarily_file=f, ready_file=f, )

    request.session['type_of_report'] = item.id

    return redirect('index')


