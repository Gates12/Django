from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models import Contact, SpamReport

class ContactTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.contact1 = Contact.objects.create(user=self.user, name='John Doe', phone_number='1234567890', email='john@example.com')
        self.contact2 = Contact.objects.create(user=self.user, name='Jane Doe', phone_number='0987654321', email='jane@example.com')

    def test_create_contact(self):
        url = reverse('contact-list')  # Corrected URL name
        data = {'name': 'Sam Smith', 'phone_number': '5551234567', 'email': 'sam@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 3)

    def test_delete_contact(self):
        url = reverse('contact-detail', args=[self.contact1.id])  # Corrected URL name
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 1)


class SpamReportTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_create_spam_report(self):
        url = reverse('spamreport-list')  # Corrected URL name
        data = {'reported_number': '1234567890'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SpamReport.objects.count(), 1)
        self.assertEqual(SpamReport.objects.first().spam_count, 1)

    def test_increment_spam_report(self):
        SpamReport.objects.create(reported_number='1234567890', reported_by=self.user, spam_count=1)
        url = reverse('spamreport-list')  # Corrected URL name
        data = {'reported_number': '1234567890'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SpamReport.objects.first().spam_count, 2)

    def test_retrieve_spam_count(self):
        SpamReport.objects.create(reported_number='1234567890', reported_by=self.user, spam_count=3)
        url = reverse('spamreport-get_spam_count') + '?phone_number=1234567890'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['spam_count'], 3)

    def test_spam_report_not_found(self):
        url = reverse('spamreport-get_spam_count') + '?phone_number=1111111111'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
