from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import EnterForm, ExitForm, SystemForm
from .models import Management
from datetime import datetime, date
from django.http import HttpResponse
import csv
from django.utils.timezone import localtime
import qrcode
from io import BytesIO
import base64


DOMAIN = "http://127.0.0.1:8000/"


class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        img = qrcode.make(DOMAIN + "logs/" + request.user.slug + "/")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr = base64.b64encode(buffer.getvalue()).decode().replace("'", "")

        return render(request, 'app/index.html', {
            'user': request.user,
            'qr': qr
        })


class LogsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        return render(request, 'app/logs.html', {
            'user': request.user,
            'slug': self.kwargs['slug']
        })


class EnterView(View):
    def get(self, request, *args, **kwargs):
        form = EnterForm(request.POST or None)

        return render(request, 'app/enter.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = EnterForm(request.POST or None)
        slug = self.kwargs['slug']

        if form.is_valid():
            management_data = Management()
            management_data.name = form.cleaned_data['name']
            management_data.tel = form.cleaned_data['tel']
            management_data.entered = datetime.now()
            management_data.slug = slug
            management_data.save()
            return redirect('enter_done')

        return render(request, 'app/enter.html', {
            'form': form
        })


class EnterDoneView(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'app/enter_done.html', {
        })


class ExitView(View):
    def get(self, request, *args, **kwargs):
        form = ExitForm(request.POST or None)

        return render(request, 'app/exit.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = ExitForm(request.POST or None)
        slug = self.kwargs['slug']

        if form.is_valid():
            tel = form.cleaned_data['tel']
            today = date.today()
            today_start_str = str(today) + ' 00:00:00'
            today_start = datetime.strptime(
                today_start_str, '%Y-%m-%d %H:%M:%S')

            today_end_str = str(today) + ' 23:59:59'
            today_end = datetime.strptime(today_end_str, '%Y-%m-%d %H:%M:%S')

            management_data = Management.objects.get(
                slug=slug, tel=tel, entered__range=(today_start, today_end))
            management_data.exited = datetime.now()
            management_data.save()
            return redirect('exit_done')

        return render(request, 'app/exit.html', {
            'form': form
        })


class ExitDoneView(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'app/exit_done.html', {
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
                slug=request.user.slug,
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
