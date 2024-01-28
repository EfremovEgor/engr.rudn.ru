from django.test import TestCase
from django.urls import reverse
from profiles.models import EmployeeProfile


class EmployeeProfileCase(TestCase):
    def setUp(self):
        EmployeeProfile.objects.create(
            full_name="Новый Новый Новый",
            job_title=["Должность1", "Должность2"],
            office="425",
            emails=["sample@email.com"],
            phone_numbers=["+79004000101"],
            working_hours="18:00-19:00",
            content="Content",
        )

    def test_employee_creation(self):
        employee = EmployeeProfile.objects.get(full_name="Новый Новый Новый")
        self.assertTrue(isinstance(employee, EmployeeProfile))
        self.assertEqual(str(employee), "Новый Новый Новый")

    def test_profiles_view(self):
        employee = EmployeeProfile.objects.get(full_name="Новый Новый Новый")

        url = reverse("profiles", kwargs={"id": employee.id})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
