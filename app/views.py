from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import EnterForm, ExitForm, SystemForm
from .models import Management
from datetime import datetime
from django.http import HttpResponse
import csv
from django.utils.timezone import localtime


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/index.html', {
            'user': request.user
        })


class EnterView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = EnterForm(request.POST or None)

        return render(request, 'app/enter.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = EnterForm(request.POST or None)

        if form.is_valid():
            management_data = Management()
            management_data.user = request.user
            management_data.name = form.cleaned_data['name']
            management_data.tel = form.cleaned_data['tel']
            management_data.entered = datetime.now()
            management_data.save()
            return redirect('index')

        return render(request, 'app/enter.html', {
            'form': form
        })


class ExitView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = ExitForm(request.POST or None)

        return render(request, 'app/exit.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = ExitForm(request.POST or None)

        if form.is_valid():
            tel = form.cleaned_data['tel']
            management_data = Management.objects.get(tel=tel)
            management_data.exited = datetime.now()
            management_data.save()
            return redirect('index')

        return render(request, 'app/exit.html', {
            'form': form
        })


class SystemView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = SystemForm(request.POST or None)

        return render(request, 'app/system.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = SystemForm(request.POST or None)

        if form.is_valid():
            entered = form.cleaned_data['entered']
            exited = form.cleaned_data['exited']
            management_data = Management.objects.filter(
                user=request.user,
                entered__gte=entered,
                exited__lte=exited
            )
            print(management_data)

            response = HttpResponse(content_type='text/csv; charset=Shift-JIS')
            header = ['お客様氏名', '電話番号', '入館時間', '退館時間']
            response['Content-Disposition'] = 'attachment; filename="enterexit.csv"'
            writer = csv.writer(response, quoting=csv.QUOTE_ALL)
            writer.writerow(header)

            for data in management_data:
                name = data.name
                tel = data.tel
                entered = localtime(data.entered).strftime("%Y/%m/%d %H:%M:%S")
                exited = localtime(data.exited).strftime("%Y/%m/%d %H:%M:%S")

                row = []
                row += [name, tel, entered, exited]
                writer.writerow(row)

        return response
