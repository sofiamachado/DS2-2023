from django.conf import settings
from django.core import mail
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.template.loader import render_to_string

from contact.forms import ContactForm

def contact(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)

def create(request):
    form = ContactForm(request.POST)
    if not form.is_valid():
        return render(request, 'contact/contact_form.html', {'form': form})
    
    _send_mail('Dados para contato preenchidos!',
               settings.DEFAULT_FROM_EMAIL,
               form.cleaned_data['email'],
               'contact/contact_email.txt',
               form.cleaned_data)
    messages.success(request, 'Dados para contato preenchidos!')
    return HttpResponseRedirect("/contact/")

def new(request):
    return render(request, 'contact/contact_form.html', {'form': ContactForm()})

def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])
