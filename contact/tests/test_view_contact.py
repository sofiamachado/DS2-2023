from django.core import mail
from django.test import TestCase
from contact.forms import ContactForm


class ContactGet(TestCase):
    def setUp(self):
        self.response = self.client.get('/contact/')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'contact/contact_form.html')

    def test_html(self):
        tags = (('<form', 1),
                ('<input', 5),
                ('type="text"', 2),
                ('type="email"', 1),
                ('type="submit"', 1))
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_has_form(self):
        form = self.response.context["form"]
        self.assertIsInstance(form, ContactForm)


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name="Sofia Machado",
                    email="sofia.machado@aluno.riogrande.ifrs.edu.br",
                    phone="53-99159-3121")
        self.response = self.client.post('/contact/', data)

    def test_post(self):
        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))


class SubscribePostInvalid(TestCase):
    def setUp(self):
        self.response = self.client.post('/contact/', {})

    def test_post(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(
            self.response, 'contact/contact_form.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, ContactForm)

    def test_form_has_error(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)

class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name="Sofia Machado", 
                    email="sofia.machado@aluno.riogrande.ifrs.edu.br", phone="53-99159-3121")
        response = self.client.post('/contact/', data, follow=True)
        self.assertContains(response, 'Dados para contato preenchidos!')
