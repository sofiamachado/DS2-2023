from django.test import TestCase
from subscriptions.forms import SubscriptionForm
from django.core import mail

class SubscribeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """GET /inscricao/ must return status_code 200"""
        response = self.client.get('/inscricao/')
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_fotm.html"""
        self.assertTemplateUsed(
            self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        """HTML must contain 5 input tags"""
        self.assertContains(self.response, "<form")
        self.assertContains(self.response, "<input", 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        """HTML must contain CSRF"""
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.response.context["form"]
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        form = self.response.context['form']
        self.assertSequenceEqual(
            ['name', 'cpf', 'email', 'phone'], list(form.fields))


class SubscribeTestPost(TestCase):
    def setUp(self):
        data = dict(name="Sofia e Dego", cpf="12345678901", email="diego.avila@aluno.riogrande.ifrs.edu.br", phone="53-99101-1002")
        self.response = self.client.post('/inscricao/', data)


    def test_post(self):
        self.assertEqual(302, self.response.status_code)
        
    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = "Confirmação de inscrição"
        self.assertEqual(expect, email.subject)

    def test_subscription_email_sender(self):
        email = mail.outbox[0]
        expect = "contato@eventif.com.br"
        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@eventif.com.br', 'diego.avila@aluno.riogrande.ifrs.edu.br']
        self.assertEqual(expect, email.to)

    def test_subscription_body(self):
        email = mail.outbox[0]
        self.assertIn('Sofia e Dego', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('diego.avila@aluno.riogrande.ifrs.edu.br', email.body)
        self.assertIn('53-99101-1002', email.body)