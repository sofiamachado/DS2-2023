from django.core import mail
from django.test import TestCase

class ValidContact(TestCase):
    def setUp(self):
        data = dict(name='Sofia Machado',
                    email='sofia.machado@aluno.riogrande.ifrs.edu.br',
                    phone='53-99159-3121',
                    message='Dados para contato preenchidos!')
        
        self.response = self.client.post('/contact/', data)

    def test_contact_status_code_302(self):
        self.assertEqual(302, self.response.status_code)

    def test_contact_subscribe_email(self):
        self.email = mail.outbox
        self.assertEqual(1, len(self.email))

class InvalidContact(TestCase):
    def setUp(self):
        self.response = self.client.post('/contact/', {})

    def test_contact_template(self):
        self.assertTemplateUsed(self.response, 'contact/contact_form.html')

    def test_contact_has_error(self):
        self.assertTrue(self.response.context['form'].errors)

class ContactMessage(TestCase):
    def test_message(self):
        data = dict(name='Sofia Machado',
                    email='sofia.machado@aluno.riogrande.ifrs.edu.br',
                    phone='53-99159-3121',
                    message='Dados para contato preenchidos!')
        response = self.client.post('/contact/', data, follow=True)
        self.assertContains(response, 'Dados para contato preenchidos!')
