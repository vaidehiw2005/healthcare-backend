from rest_framework import serializers
from .models import Patient, Doctor, PatientDoctorMapping


class PatientSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.email')

    class Meta:
        model = Patient
        fields = [
            'id', 'name', 'age', 'gender', 'phone',
            'address', 'medical_history', 'created_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def validate_age(self, value):
        if value <= 0 or value > 130:
            raise serializers.ValidationError("Age must be between 1 and 130.")
        return value


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'specialization', 'email',
            'phone', 'experience_years', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='patient.name')
    doctor_name = serializers.ReadOnlyField(source='doctor.name')
    doctor_specialization = serializers.ReadOnlyField(source='doctor.specialization')

    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id', 'patient', 'patient_name',
            'doctor', 'doctor_name', 'doctor_specialization',
            'assigned_at'
        ]
        read_only_fields = ['id', 'assigned_at']

    def validate(self, attrs):
        request = self.context.get('request')
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')

        # Ensure user can only assign doctors to their own patients
        if request and patient.created_by != request.user:
            raise serializers.ValidationError({"patient": "You can only assign doctors to your own patients."})

        # Prevent duplicate mapping with a clean 400 error
        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError("This doctor is already assigned to this patient.")

        return attrs