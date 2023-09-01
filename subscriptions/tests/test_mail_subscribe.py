from django.core import mail
from django.test import TestCase


class MailTest(TestCase):
    def setUp(self):
        data = dict(name="Sofia e Dego",
                    cpf="12345678901",
                    email="diego.avila@aluno.riogrande.ifrs.edu.br",
                    phone="53-99101-1002")
        self.response = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = "Confirmação de inscrição"
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_sender(self):
        expect = "contato@eventif.com.br"
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventif.com.br',
                  'diego.avila@aluno.riogrande.ifrs.edu.br']
        self.assertEqual(expect, self.email.to)

    def test_subscription_body(self):
        contents = ['Sofia e Dego',
                    '12345678901',
                    'diego.avila@aluno.riogrande.ifrs.edu.br',
                    '53-99101-1002']
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
