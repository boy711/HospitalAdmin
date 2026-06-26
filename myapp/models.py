from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    BLOOD_TYPE_CHOICES = [
        ("O+", "O+"), ("O-", "O-"),
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
    ]
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    age = models.PositiveIntegerField()
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES)
    last_visit = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-last_visit"]

    def __str__(self):
        return self.name


class Staff(models.Model):
    ROLE_CHOICES = [
        ("doctor", "Doctor"),
        ("nurse", "Nurse"),
        ("support", "Support Staff"),
    ]
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]

    name = models.CharField(max_length=150)
    title = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    department = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    start_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Staff"

    def __str__(self):
        return self.name


class Appointment(models.Model):
    TYPE_CHOICES = [
        ("consultation", "Consultation"),
        ("follow_up", "Follow-up"),
        ("check_up", "Check-up"),
    ]
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True,
                               limit_choices_to={"role": "doctor"}, related_name="appointments")
    appointment_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="consultation")
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="scheduled")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-time"]

    def __str__(self):
        return f"{self.patient.name} - {self.date}"


class InventoryItem(models.Model):
    CATEGORY_CHOICES = [
        ("ppe", "PPE"),
        ("medical_supplies", "Medical Supplies"),
        ("equipment", "Equipment"),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    quantity = models.PositiveIntegerField(default=0)
    min_stock = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def total_value(self):
        return self.quantity * self.unit_price

    @property
    def status(self):
        if self.quantity == 0:
            return "out_of_stock"
        elif self.quantity < self.min_stock:
            return "low_stock"
        return "in_stock"


class MedicalRecord(models.Model):
    RECORD_TYPE_CHOICES = [
        ("consultation_notes", "Consultation Notes"),
        ("lab_results", "Lab Results"),
        ("imaging_report", "Imaging Report"),
        ("surgery_report", "Surgery Report"),
        ("other", "Other"),
    ]
    STATUS_CHOICES = [
        ("filed", "Filed"),
        ("pending", "Pending"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="records")
    doctor = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="records")
    record_type = models.CharField(max_length=30, choices=RECORD_TYPE_CHOICES)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.patient.name} - {self.get_record_type_display()}"


class Invoice(models.Model):
    STATUS_CHOICES = [
        ("paid", "Paid"),
        ("pending", "Pending"),
        ("overdue", "Overdue"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="invoices")
    invoice_number = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.invoice_number} - {self.patient.name}"


class Prescription(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("expired", "Expired"),
    ]
    FREQUENCY_CHOICES = [
        ("once_daily", "Once daily"),
        ("twice_daily", "Twice daily"),
        ("three_daily", "Three times daily"),
        ("as_needed", "As needed"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="prescriptions")
    doctor = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={"role": "doctor"}, related_name="prescriptions")
    medication = models.CharField(max_length=150)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    duration = models.CharField(max_length=50, help_text="e.g. 30 days")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.patient.name} - {self.medication}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    full_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"