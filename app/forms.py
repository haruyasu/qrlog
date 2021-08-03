from django import forms


class EnterForm(forms.Form):
    name = forms.CharField(max_length=200, label='名前')
    tel = forms.CharField(max_length=200, label='電話番号')


class ExitForm(forms.Form):
    tel = forms.CharField(max_length=200, label='電話番号')


class SystemForm(forms.Form):
    entered = forms.DateField(label='入館', widget=forms.DateInput(attrs={"type":"date"}))
    exited = forms.DateField(label='退館', widget=forms.DateInput(attrs={"type":"date"}))
