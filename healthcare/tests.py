from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Patient, Doctor, PatientDoctorMapping

User = get_user_model()


class HealthcareAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='alice@example.com', name='Alice', password='StrongPassword123!')
        self.other_user = User.objects.create_user(email='bob@example.com', name='Bob', password='StrongPassword123!')
        login_res = self.client.post('/api/auth/login/', {'email': 'alice@example.com', 'password': 'StrongPassword123!'})
        self.token = login_res.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_register_and_login(self):
        res = self.client.post('/api/auth/register/', {
            'name': 'Charlie',
            'email': 'charlie@example.com',
            'password': 'StrongPassword123!'
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_patient_crud_and_isolation(self):
        # Create patient
        res = self.client.post('/api/patients/', {
            'name': 'John Doe',
            'age': 34,
            'gender': 'Male',
            'phone': '9876543210',
            'address': 'Vadodara',
            'medical_history': 'None'
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Create patient under another user
        Patient.objects.create(created_by=self.other_user, name='Secret Patient', age=40, gender='Female', phone='1112223333')

        # Alice should only see her 1 patient
        list_res = self.client.get('/api/patients/')
        self.assertEqual(len(list_res.data), 1)

    def test_doctor_and_mapping_flow(self):
        patient = Patient.objects.create(created_by=self.user, name='Jane', age=28, gender='Female', phone='9998887776')
        doc_res = self.client.post('/api/doctors/', {
            'name': 'Dr. Sharma',
            'specialization': 'Cardiology',
            'email': 'sharma@hospital.com',
            'phone': '9123456789',
            'experience_years': 12
        })
        self.assertEqual(doc_res.status_code, status.HTTP_201_CREATED)
        doctor_id = doc_res.data['id']

        # Assign doctor
        map_res = self.client.post('/api/mappings/', {'patient': patient.id, 'doctor': doctor_id})
        self.assertEqual(map_res.status_code, status.HTTP_201_CREATED)

        # Duplicate assignment fails cleanly
        dup_res = self.client.post('/api/mappings/', {'patient': patient.id, 'doctor': doctor_id})
        self.assertEqual(dup_res.status_code, status.HTTP_400_BAD_REQUEST)

        # Fetch doctors for patient
        get_res = self.client.get(f'/api/mappings/{patient.id}/')
        self.assertEqual(len(get_res.data), 1)