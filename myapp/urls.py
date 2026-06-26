from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings/', views.settings, name='settings'),

    # Patients
    path("patients/", views.patients, name="patients"),
    path("patients/add/", views.patient_add, name="patient_add"),
    path("patients/<int:pk>/edit/", views.patient_edit, name="patient_edit"),
    path("patients/<int:pk>/delete/", views.patient_delete, name="patient_delete"),
    path("patients/<int:pk>/", views.patient_detail, name="patient_detail"),

    # Staff
    path("staff-management/", views.staffmanagement, name="staffmanagement"),
    path("staff-management/add/", views.staff_add, name="staff_add"),
    path("staff-management/<int:pk>/edit/", views.staff_edit, name="staff_edit"),
    path("staff-management/<int:pk>/delete/", views.staff_delete, name="staff_delete"),

    # Appointments
    path("appointments/", views.appointments, name="appointments"),
    path("appointments/add/", views.appointment_add, name="appointment_add"),
    path("appointments/<int:pk>/delete/", views.appointment_delete, name="appointment_delete"),

    # Inventory
    path("inventory/", views.inventory, name="inventory"),
    path("inventory/add/", views.inventory_add, name="inventory_add"),
    path("inventory/<int:pk>/edit/", views.inventory_edit, name="inventory_edit"),
    path("inventory/<int:pk>/delete/", views.inventory_delete, name="inventory_delete"),

    # Medical Records
    path("medicalrecords/", views.medicalrecords, name="medicalrecords"),
    path("medicalrecords/add/", views.medicalrecord_add, name="medicalrecord_add"),
    path("medicalrecords/<int:pk>/delete/", views.medicalrecord_delete, name="medicalrecord_delete"),

    # Billing
    path("billing/", views.billing, name="billing"),
    path("billing/add/", views.invoice_add, name="invoice_add"),
    path("billing/<int:pk>/delete/", views.invoice_delete, name="invoice_delete"),

    # Prescriptions
    path("prescriptions/", views.prescriptions, name="prescriptions"),
    path("prescriptions/add/", views.prescription_add, name="prescription_add"),
    path("prescriptions/<int:pk>/delete/", views.prescription_delete, name="prescription_delete"),

    # Profile
    path("profile/", views.profile, name="profile"),
    
]
