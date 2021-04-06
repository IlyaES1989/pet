
from pathlib import Path

from ..classes.prepare import Prepare
from .weekly import weekly
from .count_bills import count_bills


SCRIPT_DIR = Path(__file__).resolve().parent

TEMPLATE = {
    'weekly_report': {
        'Дисп': ['Отчет по диспетчерам'],
        'QR': ['Склад.Город', 'МТЗ'],
        'Продажи': ['Продажи с'],
        'Планы': ['План на конец'],
    },
    'count_bills': {'count': [' ']},
}


def preparation(file, template):
    prepare = Prepare()

    prepare.file = file
    prepare.template_dict = template

    prepare.fix_error()
    prepare.reader()
    prepare.find_head()
    prepare.find_group()
    prepare.determ_file()
    prepare.del_empty()
    prepare.change_head()

    outcome = prepare.writer()
    return outcome, prepare.file_tag


def generate_variable(**kwargs):

    month = kwargs.get('month')
    template = kwargs.get('template')
    file_tags = kwargs.get('file_tags')
    year = kwargs.get('year')
    last_report = kwargs.get('last_report')
    last_year_report = kwargs.get('last_year_report')

    report_variables = {
        'weekly_report': (
            {weekly.DataSh1: {'month': month,
                              'template': template,
                              'file_tags': file_tags}},
            {weekly.DataSh2: {'month': month,
                              'template': template,
                              'file_tags': file_tags}},
            {weekly.DataSh3: {'month': month,
                              'template': template,
                              'file_tags': file_tags,
                              'year': year,
                              'last_report': last_report,
                              'last_year_report': last_year_report}},
            {weekly.DataSh4: {'month': month,
                              'template': template,
                              'file_tags': file_tags,
                              'year': year,
                              'last_report': last_report,
                              'last_year_report': last_year_report}}
        ),
        'count_bills': (
            {count_bills.Data: {'month': month,
                                'template': template,
                                'file_tags': file_tags}},
        ),
    }
    return report_variables


def report_generation(key, report_variables):
    sheet_list = []
    for report in report_variables.get(key):
        for sheet_class in report:
            kwargs = report[sheet_class]
            sheet = sheet_class(**kwargs)
            sheet_list.append(sheet)

    return sheet_list


