from django.shortcuts import render, redirect
from django.views.generic import ListView
from apps.Files.models import FileModel
from apps.Files.forms import EncryptForm, DecryptForm
from apps.crypt import symm, asym


class CryptModelView(ListView):
    template_name = 'main.html'
    model = FileModel

    def get_context_data(self, **kwargs):
        context = {
            'encrypt_form': kwargs['encrypt_form'],
            'decrypt_form': kwargs['decrypt_form'],
        }
        return context

    def get(self, request, **kwargs):
        enform = EncryptForm()
        deform = DecryptForm()
        return render(request, self.template_name, context=self.get_context_data(
            decrypt_form=deform,
            encrypt_form=enform,
        ))

    def post(self, request, **kwargs):
        enform = EncryptForm(request.POST, request.FILES)
        deform = DecryptForm(request.POST, request.FILES)

        if enform.is_valid() and ('sym_encrypt' in request.POST):

            newfile = FileModel.objects.create(
                file=enform.cleaned_data["file"])

            symm.symmetric_encryption(
                filename=f'media/{enform.cleaned_data["file"]}',
                receiver=enform.cleaned_data['mail'])

            return redirect('/')

        elif deform.is_valid() and ('sym_decrypt' in request.POST):

            symm.symmetric_decryption(
                filename=f'media/{deform.cleaned_data["file"]}',
                keyfile=f'media/{deform.cleaned_data["key"]}',
                file_type=f'{deform.cleaned_data["extension"]}',
                receiver=deform.cleaned_data['mail'])

            return redirect('/')

        elif enform.is_valid() and ('asy_encrypt' in request.POST):

            newfile = FileModel.objects.create(
                file=enform.cleaned_data["file"])

            s = asym.asymmetric_encryption(
                filename=newfile.file.name,
                receiver=enform.cleaned_data['mail'])

            if s == 1:
                enform.add_error('file',
                                       "File is too big, 256 bytes maximum")
            newfile.delete()
            return redirect('/')

        elif deform.is_valid() and ('asy_decrypt' in request.POST):

            asym.asymmetric_decryption(
                filename=f'media/{deform.cleaned_data["file"]}',
                privkey_file=f'media/{deform.cleaned_data["key"]}',
                file_type=f'{deform.cleaned_data["extension"]}',
                receiver=deform.cleaned_data['mail'])

            return redirect('/')

        return render(request, self.template_name, context=self.get_context_data(
            decrypt_form=deform,
            encrypt_form=enform,
        ))
