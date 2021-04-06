import datetime

from django import forms

from .models import (
    Report,
    PreparationFile,
)
from .xls_script.report_scripts.script import TEMPLATE


class ReportForm (forms.Form):
    TYPE_REPORT = [(key, key.capitalize().replace('_', ' ')) for key in TEMPLATE.keys()]
    CURRENT_YEAR = datetime.datetime.now().year
    CURRENT_MONTH = datetime.datetime.now().month
    CHECKBOX_MAP = [('on', True), ('off', False)]

    MONTH_CHOICES = [(i, j) for i, j in zip(range(1, 13), range(1, 13))]
    YEAR_CHOICES = [(i, j) for i, j in zip(range(CURRENT_YEAR - 1, CURRENT_YEAR + 10),
                                           range(CURRENT_YEAR - 1, CURRENT_YEAR + 10))]

    item = forms.CharField(
        max_length=Report._meta.get_field('user').max_length,
        widget=forms.Select(choices=TYPE_REPORT, attrs={'class': 'form-select'}))

    last = forms.FileField(required=False,
                           widget=forms.FileInput(attrs={'class': 'form-control'}))

    last_year = forms.FileField(required=False,
                                widget=forms.FileInput(attrs={'class': 'form-control'}))

    tag = forms.CharField(required=False,
                          max_length=Report._meta.get_field('tag').max_length)

    month = forms.IntegerField(widget=forms.Select(choices=MONTH_CHOICES,
                                                   attrs={'class': 'form-select'}),
                               initial=MONTH_CHOICES[CURRENT_MONTH - 2])

    year = forms.IntegerField(widget=forms.Select(choices=YEAR_CHOICES,
                                                  attrs={'class': 'form-select'}),
                              initial=YEAR_CHOICES[1])
    open_last_report = forms.BooleanField(required=False,
                                          initial=True,
                                          widget=forms.CheckboxInput(
                                              attrs={'class': 'form-check-input', 'value': 'True'}))

    class Meta:
        model = Report
        fields = ['item', 'last', 'last_year', 'tag', 'month', 'year', 'open_last_report', ]


class RawDataForm(forms.Form):
    primarily_file = forms.FileField(required=False,
                                     widget=forms.ClearableFileInput(attrs={'multiple': True,
                                                                            'class': 'form-control'}))

    class Meta:
        model = PreparationFile
        fields = ['primarily_file']


class PreparationFileForm(forms.Form):

    ready_file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = PreparationFile
        fields = ['ready_file']

