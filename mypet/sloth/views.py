from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.core.files import File
from django.views import View
from django.db.models import Max

from .models import Report, PreparationFile, Outcome
from .forms import ReportForm, PreparationFileForm, RawDataForm

import re

from .xls_script.report_scripts.script import preparation, generate_variable, report_generation, TEMPLATE

from .xls_script.classes.report import GenerateReport


#   Help function
def get_user(request):
    user = User.objects.get(username=request.user.username)
    return user


def name_cutter(long_name):
    short_name = re.split(r'/', long_name)[-1]
    return short_name


#   Common function and classes
@method_decorator(login_required, name='dispatch')
class Setting(View):
    r_form_class = ReportForm
    p_form_class = RawDataForm
    template_name = 'index.html'

    def get(self, request):
        user = get_user(request)
        r_form = self.r_form_class()
        p_form = self.p_form_class(request.POST, request.FILES)
        response = render(request, 'sloth/index.html', {'r_form': r_form, 'p_form': p_form, 'user': user})
        return response

    def post(self, request):
        user = get_user(request)
        item_obj = Report.objects.get(user=user, item=request.POST.get('item'))
        form = self.r_form_class(request.POST, request.FILES)
        request.session['type_of_report'] = item_obj.id

        # If last_year file download - update, else use previous.
        last_year = request.FILES.get(
            'last_year',
            Report.objects.get(user=user, item=request.POST.get('item')).last_year)

        if form.is_valid():
            Report.objects.update_or_create(
                user=user,
                item=request.POST.get('item'),
                defaults={'last': request.FILES.get('last'),
                          'last_year': last_year,
                          'month': request.POST.get('month'),
                          'year': request.POST.get('year'),
                          'open_last_report': (request.POST.get('open_last_report', False)), })

        raw_data_form = RawDataForm(request.FILES)
        files = request.FILES.getlist('primarily_file')

        if raw_data_form.is_valid():

            rubbish = PreparationFile.objects.filter(user=user, item=item_obj)
            rubbish.delete()
            template = TEMPLATE[item_obj.item]

            for f in files:
                (p, tag) = preparation(f, template)
                ready_file = File(p, name=f.name)

                PreparationFile.objects.create(user=user,
                                               item=item_obj,
                                               ready_file=ready_file,
                                               file_tag=tag)
        return redirect('create')


@method_decorator(login_required, name='dispatch')
class CreateReport(View):
    r_form_class = ReportForm
    p_form_class = PreparationFileForm
    template_name = 'create.html'

    def get(self, request):
        user = get_user(request)
        r_form = self.r_form_class()

        p_form = self.p_form_class()

        item = request.session.get('type_of_report', None)

        if item:
            preparing_files = PreparationFile.objects.filter(user=user, item=item)
            for file in preparing_files:
                short_name = name_cutter(file.ready_file.name)
                file.ready_file.short_name = short_name

            outcome = Outcome.objects.filter(user=user, report=item)
            for file in outcome:
                short_name = name_cutter(file.file.name)
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

        response = render(request, 'sloth/create.html', context_dict)
        return response

    def post(self, request):
        now = timezone.now()

        user = get_user(request)

        item_id = request.session.get('type_of_report')
        report_obj = Report.objects.get(id=item_id)
        template = TEMPLATE[report_obj.item]
        month = report_obj.month
        year = report_obj.year
        last_year_report = report_obj.last_year
        open_last_report = report_obj.open_last_report
        last_report = report_obj.last

        ready_files = PreparationFile.objects.filter(user=user, item=item_id)
        file_tags = {file.file_tag: file.ready_file for file in ready_files}

        sheets = generate_variable(month=month,
                                   year=year,
                                   template=template,
                                   last_report=last_report,
                                   last_year_report=last_year_report,
                                   file_tags=file_tags)

        sheets_list = report_generation(report_obj.item, sheets)

        w_r = GenerateReport(sheets=sheets_list)
        if open_last_report:
            (p, new_report_name) = w_r.generate_mutable_part(last_report)
            new_report = File(p, name=new_report_name)
        else:
            (p, new_report_name) = w_r.generate_template(year=year)
            template_file = File(p, name=new_report_name)
            report_obj.last = template_file
            report_obj.save()
            last_report = report_obj.last

            (p, new_report_name) = w_r.generate_mutable_part(last_report)
            new_report = File(p, name=new_report_name)

        Outcome.objects.create(user=user, report=report_obj, file=new_report, time=now)

        return redirect('result')


def get_result(request):
    if request.method == 'GET':
        user = get_user(request)
        item_id = request.session.get('type_of_report')
        max_time = Outcome.objects.filter(user=user, report=item_id).aggregate(Max('time'))
        print('max_time' * 10, max_time)
        result = Outcome.objects.get(user=user, report=item_id, time=max_time['time__max'])
        short_name = name_cutter(result.file.name)
        result.short_name = short_name

        response = render(request, 'sloth/result.html', {'result': result})
        return response


def update_file(request):
    if request.method == 'POST':
        user = get_user(request)
        item_id = request.session.get('type_of_report')
        item = Report.objects.get(id=item_id)
        up_tag = request.POST.get('up_file')
        new_file = request.FILES.get('ready_file')
        print('NEW ' * 10, request.FILES)

        form = PreparationFileForm(request.POST, request.FILES)

        if form.is_valid():
            PreparationFile.objects.update_or_create(user=user, item=item, file_tag=up_tag,
                                                     defaults={'ready_file': new_file})
    return redirect('create')


