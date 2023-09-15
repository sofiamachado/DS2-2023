from datetime import datetime
from django.test import TestCase
from subscriptions.models import Subscription

class SubscriptionsModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name="Sofia Machado",
            cpf="12345678901",
            email="sofia.machado@aluno.riogrande.ifrs.edu.br",
            phone="53-99159-3121",
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)
    
    def test_str(self):
        self.assertEqual("Sofia Machado", str(self.obj))