from django.test import TestCase
from contact.forms import ContactForm

class ContactGetTest(TestCase):
    def setUp(self):
        self.form = ContactForm()
        self.response = self.client.post('/contact/')

    def test_form_fields(self):
        self.assertSequenceEqual(
            ['name', 'email', 'phone', 'message'], list(self.form.fields))
        
    def test_contact_get_status_200(self):
        self.assertEqual(200, self.response.status_code)

    def test_contact_template(self):
        self.assertTemplateUsed(self.response, 'contact/contact_form.html')

    def test_contact_has_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contact_html(self):
        _html = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="hidden"',1),
                ('type="submit"', 1))
        for type, number in _html:
            with self.subTest():
                self.assertContains(self.response, type, number)

    def test_contact_has_form(self):
        self.assertIsInstance(self.response.context['form'], ContactForm)
