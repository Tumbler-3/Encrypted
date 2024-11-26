from django.shortcuts import render, redirect
from django.views.generic import ListView
from apps.Files.models import FileModel
from apps.Files.forms import EncryptForm, DecryptForm, AsymEncryptForm
from apps.crypt import symm, asym


class CryptModelView(ListView):
    template_name = 'main.html'
    model = FileModel

    def get_context_data(self, **kwargs):
        context = {
            'encrypt_form': kwargs['encrypt_form'],
            'decrypt_form': kwargs['decrypt_form'],
            'asym_enform': kwargs['asym_enform'],
        }
        return context

    def get(self, request, **kwargs):
        enform = EncryptForm()
        deform = DecryptForm()
        asym_enform = AsymEncryptForm()
        return render(request, self.template_name, context=self.get_context_data(
            decrypt_form=deform,
            encrypt_form=enform,
            asym_enform=asym_enform
        ))

    def post(self, request, **kwargs):
        enform = EncryptForm(request.POST, request.FILES)
        asym_enform = AsymEncryptForm(request.POST, request.FILES)
        deform = DecryptForm(request.POST, request.FILES)

        if enform.is_valid() and ('sym_encrypt' in request.POST):

            newfile = FileModel.objects.create(
                file=enform.cleaned_data["file"])

            symm.symmetric_encryption(
                filename=f'media/{enform.cleaned_data["file"]}',
                receiver=enform.cleaned_data['mail'])
            newfile.delete()
            return redirect('/')

        elif deform.is_valid() and ('sym_decrypt' in request.POST):

            symm.symmetric_decryption(
                filename=f'media/{deform.cleaned_data["file"]}',
                keyfile=f'media/{deform.cleaned_data["key"]}',
                file_type=f'{deform.cleaned_data["extension"]}',
                receiver=deform.cleaned_data['mail'])

            return redirect('/')

        elif asym_enform.is_valid() and ('asy_encrypt' in request.POST):
            newfile = FileModel.objects.create(
                file=asym_enform.cleaned_data["file"],
                key=asym_enform.cleaned_data["key"])

            asym.asymmetric_encryption(
                filename=newfile.file.name,
                receiver=asym_enform.cleaned_data['mail'],
                pubkey_file=newfile.key.name)

            newfile.delete()

        elif deform.is_valid() and ('asy_decrypt' in request.POST):

            newfile = FileModel.objects.create(
                file=asym_enform.cleaned_data["file"],
                key=asym_enform.cleaned_data["key"])

            asym.asymmetric_decryption(
                filename='media/'+newfile.file.name,
                privkey_file='media/'+newfile.key.name,
                file_type=f'{deform.cleaned_data["extension"]}',
                receiver=deform.cleaned_data['mail'])

            return redirect('/')

        return render(request, self.template_name, context=self.get_context_data(
            decrypt_form=deform,
            encrypt_form=enform,
            asym_enform=asym_enform
        ))
