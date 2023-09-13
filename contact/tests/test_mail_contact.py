from django.core import mail
from django.test import TestCase

class TestContactMail(TestCase):
    def setUp(self):
        data = dict(name='Sofia Machado',
                    email='sofia.machado@aluno.riogrande.ifrs.edu.br',
                    phone='53-99159-3121',
                    message='Dados para contato preenchidos!')
        
        self.response = self.client.post('/contact/', data)
        self.email = mail.outbox[0]

    def test_mail_contact_ubject(self):
        expect = 'Dados para contato preenchidos!'
        self.assertEqual(expect, self.email.subject)

    def test_email_contact_sender(self):
        expect = 'contato@eventif.com.br'
        self.assertEqual(expect, self.email.from_email)

    def test_email_contact_to(self):
        expect = ['contato@eventif.com.br',
                  'sofia.machado@aluno.riogrande.ifrs.edu.br']
        self.assertEqual(expect, self.email.to)

    def test_contact_contact_body(self):
        datas = ['Sofia Machado',
                    'sofia.machado@aluno.riogrande.ifrs.edu.br',
                    '53-99159-3121',
                    'Dados para contato preenchidos!']
        for data in datas:
            with self.subTest():
                self.assertIn(data, self.email.body)
