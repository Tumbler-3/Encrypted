from django import forms
import os


class EncryptForm(forms.Form):
    file = forms.FileField(required=True, widget=forms.FileInput(
        attrs={"class": "form-control form-control-lg", "placeholder": "File", "id": "floatingInputValue"}), label='File')
    mail = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={"class": "form-control-lg", "placeholder": "Email", "id": "floatingInputValue"}), label='')


class AsymEncryptForm(forms.Form):
    file = forms.FileField(required=True, widget=forms.FileInput(
        attrs={"class": "form-control form-control-lg", "placeholder": "File", "id": "floatingInputValue"}), label='File')
    key = forms.FileField(required=False, widget=forms.FileInput(
        attrs={"class": "form-control form-control-lg", "placeholder": "Key", "id": "floatingInputValue"}), label='Key')
    mail = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={"class": "form-control-lg", "placeholder": "Email", "id": "floatingInputValue"}), label='')

    def clean_file(self):
        file = self.cleaned_data.get('file')
        self.fields['file'].widget.attrs['class'] = "error"
        if file.size > 245:
            raise forms.ValidationError("File is too big, 245 bytes maximum")
        return file
    


class DecryptForm(forms.Form):
    file = forms.FileField(allow_empty_file=False, required=True, widget=forms.FileInput(
        attrs={"class": "form-control form-control-lg", "placeholder": "File", "id": "floatingInputValue"}), label='File')
    extension = forms.CharField(empty_value=False, required=True, widget=forms.TextInput(
        attrs={"class": "form-control-lg", "placeholder": "Extension", "id": "floatingInputValue"}), label='')
    key = forms.FileField(allow_empty_file=False, required=True, widget=forms.FileInput(
        attrs={"class": "form-control form-control-lg", "placeholder": "Key", "id": "floatingInputValue"}), label='Key')
    mail = forms.EmailField(required=True, empty_value=False, widget=forms.EmailInput(
        attrs={"class": "form-control-lg", "placeholder": "Email", "id": "floatingInputValue"}), label='')
