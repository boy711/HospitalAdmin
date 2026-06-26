from django import forms
from .models import Patient, Staff, Appointment, InventoryItem, MedicalRecord, Invoice, Prescription
from django.contrib.auth.models import User
from .models import Patient, Staff, Appointment, InventoryItem, MedicalRecord, Invoice, Prescription, UserProfile

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["name", "email", "phone", "age", "blood_type", "last_visit", "status"]
        widgets = {"last_visit": forms.DateInput(attrs={"type": "date"})}


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ["name", "title", "role", "department", "email", "phone", "start_date", "status"]
        widgets = {"start_date": forms.DateInput(attrs={"type": "date"})}


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["patient", "doctor", "appointment_type", "date", "time", "status"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
        }


class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ["name", "category", "quantity", "min_stock", "unit_price"]


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ["patient", "doctor", "record_type", "notes", "status", "date"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ["patient", "invoice_number", "amount", "status", "date"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ["patient", "doctor", "medication", "dosage", "frequency", "duration", "status"]
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["avatar", "full_name", "phone", "bio"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
        }

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]