from django import forms


class EncryptForm(forms.Form):
    file = forms.FileField(allow_empty_file=False, required=True)
    mail = forms.EmailField(required=True, empty_value=False)


class DecryptForm(forms.Form):
    file = forms.FileField(allow_empty_file=False, required=True)
    mail = forms.EmailField(required=True, empty_value=False)
    key = forms.FileField(allow_empty_file=False, required=True)
    extension = forms.CharField(empty_value=False, required=True)
