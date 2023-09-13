from django.conf import settings
from django.core import mail
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from contact.forms import ContactForm

def contact(request):
    if request.method == 'POST':
        return formCreate(request)
    return formNew(request)

def formNew(request):
    form = ContactForm(request.POST)

    return render(request, 'contact/contact_form.html', {'form': form})

def formCreate(request):
    form = ContactForm(request.POST)

    if not form.is_valid():
        return render(request, 'contact/contact_form.html', {'form': form})
    
    mail.send_mail('Dados para contato preenchidos!', render_to_string('contact/contact_email.txt', form.cleaned_data), settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL, form.cleaned_data['email']])

    messages.success(request, 'Dados para contato preenchidos!')
    
    return HttpResponseRedirect('/contact/')