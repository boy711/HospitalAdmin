from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Sum
from django.utils import timezone
from .models import Patient, Staff, Appointment, InventoryItem, MedicalRecord, Invoice, Prescription
from .forms import (PatientForm, StaffForm, AppointmentForm, InventoryItemForm, MedicalRecordForm, InvoiceForm, PrescriptionForm)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Patient, Staff, Appointment, InventoryItem, MedicalRecord, Invoice, Prescription, UserProfile
from .forms import (PatientForm, StaffForm, AppointmentForm, InventoryItemForm, MedicalRecordForm, InvoiceForm, PrescriptionForm, UserProfileForm, UserInfoForm)

@login_required
def index(request):
    return render(request, 'dashboard/index.html')

@login_required
def settings(request):
    return render(request, 'dashboard/settings.html')


# ===================== PATIENTS =====================
@login_required
def patients(request):
    query = request.GET.get("q", "").strip()
    patients_qs = Patient.objects.all()
    if query:
        patients_qs = patients_qs.filter(Q(name__icontains=query) | Q(email__icontains=query))
    context = {
        "patients": patients_qs,
        "total_patients": Patient.objects.count(),
        "query": query,
    }
    return render(request, "dashboard/patients.html", context)

@login_required
def patient_add(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient added successfully.")
            return redirect("patients")
    else:
        form = PatientForm()
    return render(request, "dashboard/patient_form.html", {"form": form, "action": "Add"})

@login_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient updated successfully.")
            return redirect("patients")
    else:
        form = PatientForm(instance=patient)
    return render(request, "dashboard/patient_form.html", {"form": form, "action": "Edit", "patient": patient})

@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        patient.delete()
        messages.success(request, "Patient deleted.")
        return redirect("patients")
    return render(request, "dashboard/confirm_delete.html", {"object": patient, "type": "patient"})

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, "dashboard/patient_detail.html", {"patient": patient})


# ===================== STAFF =====================
@login_required
def staffmanagement(request):
    query = request.GET.get("q", "").strip()
    staff_qs = Staff.objects.all()
    if query:
        staff_qs = staff_qs.filter(Q(name__icontains=query) | Q(department__icontains=query))
    context = {
        "staff_list": staff_qs,
        "total_staff": Staff.objects.count(),
        "doctors_count": Staff.objects.filter(role="doctor").count(),
        "nurses_count": Staff.objects.filter(role="nurse").count(),
        "support_count": Staff.objects.filter(role="support").count(),
        "query": query,
    }
    return render(request, "dashboard/staffmanagement.html", context)

@login_required
def staff_add(request):
    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff member added successfully.")
            return redirect("staffmanagement")
    else:
        form = StaffForm()
    return render(request, "dashboard/staff_form.html", {"form": form, "action": "Add"})

@login_required
def staff_edit(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == "POST":
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff member updated successfully.")
            return redirect("staffmanagement")
    else:
        form = StaffForm(instance=staff)
    return render(request, "dashboard/staff_form.html", {"form": form, "action": "Edit", "staff": staff})

@login_required
def staff_delete(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == "POST":
        staff.delete()
        messages.success(request, "Staff member deleted.")
        return redirect("staffmanagement")
    return render(request, "dashboard/confirm_delete.html", {"object": staff, "type": "staff member"})


# ===================== APPOINTMENTS =====================
@login_required
def appointments(request):
    status_filter = request.GET.get("status", "all")
    appts_qs = Appointment.objects.select_related("patient", "doctor")
    if status_filter != "all":
        appts_qs = appts_qs.filter(status=status_filter)
    context = {
        "appointments": appts_qs,
        "total_scheduled": Appointment.objects.filter(status="scheduled").count(),
        "total_completed": Appointment.objects.filter(status="completed").count(),
        "total_cancelled": Appointment.objects.filter(status="cancelled").count(),
        "today_count": Appointment.objects.filter(date=timezone.localdate()).count(),
        "status_filter": status_filter,
    }
    return render(request, "dashboard/appointments.html", context)

@login_required
def appointment_add(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment scheduled successfully.")
            return redirect("appointments")
    else:
        form = AppointmentForm()
    return render(request, "dashboard/appointment_form.html", {"form": form, "action": "New"})

@login_required
def appointment_delete(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        appt.delete()
        messages.success(request, "Appointment deleted.")
        return redirect("appointments")
    return render(request, "dashboard/confirm_delete.html", {"object": appt, "type": "appointment"})


# ===================== INVENTORY =====================
@login_required
def inventory(request):
    category_filter = request.GET.get("category", "all")
    items_qs = InventoryItem.objects.all()
    if category_filter != "all":
        items_qs = items_qs.filter(category=category_filter)
    all_items = InventoryItem.objects.all()
    total_value = sum(item.total_value for item in all_items)
    low_stock_count = sum(1 for item in all_items if item.status == "low_stock")
    out_of_stock_count = sum(1 for item in all_items if item.status == "out_of_stock")
    context = {
        "items": items_qs,
        "total_items": all_items.count(),
        "low_stock_count": low_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "total_value": total_value,
        "category_filter": category_filter,
    }
    return render(request, "dashboard/inventory.html", context)

@login_required
def inventory_add(request):
    if request.method == "POST":
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item added successfully.")
            return redirect("inventory")
    else:
        form = InventoryItemForm()
    return render(request, "dashboard/inventory_form.html", {"form": form, "action": "Add"})

@login_required
def inventory_edit(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == "POST":
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated successfully.")
            return redirect("inventory")
    else:
        form = InventoryItemForm(instance=item)
    return render(request, "dashboard/inventory_form.html", {"form": form, "action": "Edit", "item": item})

@login_required
def inventory_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Item deleted.")
        return redirect("inventory")
    return render(request, "dashboard/confirm_delete.html", {"object": item, "type": "inventory item"})


# ===================== MEDICAL RECORDS =====================
@login_required
def medicalrecords(request):
    records_qs = MedicalRecord.objects.select_related("patient", "doctor")
    context = {
        "records": records_qs,
        "total_records": MedicalRecord.objects.count(),
        "filed_count": MedicalRecord.objects.filter(status="filed").count(),
        "pending_count": MedicalRecord.objects.filter(status="pending").count(),
    }
    return render(request, "dashboard/medicalrecords.html", context)

@login_required
def medicalrecord_add(request):
    if request.method == "POST":
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Medical record added successfully.")
            return redirect("medicalrecords")
    else:
        form = MedicalRecordForm()
    return render(request, "dashboard/medicalrecord_form.html", {"form": form, "action": "New"})

@login_required
def medicalrecord_delete(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == "POST":
        record.delete()
        messages.success(request, "Record deleted.")
        return redirect("medicalrecords")
    return render(request, "dashboard/confirm_delete.html", {"object": record, "type": "medical record"})


# ===================== BILLING =====================
@login_required
def billing(request):
    invoices_qs = Invoice.objects.select_related("patient")
    total_revenue = Invoice.objects.filter(status="paid").aggregate(t=Sum("amount"))["t"] or 0
    pending_amount = Invoice.objects.filter(status="pending").aggregate(t=Sum("amount"))["t"] or 0
    overdue_amount = Invoice.objects.filter(status="overdue").aggregate(t=Sum("amount"))["t"] or 0
    paid_count = Invoice.objects.filter(status="paid").count()
    context = {
        "invoices": invoices_qs,
        "total_revenue": total_revenue,
        "pending_amount": pending_amount,
        "overdue_amount": overdue_amount,
        "paid_count": paid_count,
    }
    return render(request, "dashboard/billing.html", context)

@login_required
def invoice_add(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Invoice created successfully.")
            return redirect("billing")
    else:
        form = InvoiceForm()
    return render(request, "dashboard/invoice_form.html", {"form": form, "action": "Create"})

@login_required
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == "POST":
        invoice.delete()
        messages.success(request, "Invoice deleted.")
        return redirect("billing")
    return render(request, "dashboard/confirm_delete.html", {"object": invoice, "type": "invoice"})


# ===================== PRESCRIPTIONS =====================
@login_required
def prescriptions(request):
    status_filter = request.GET.get("status", "active")
    rx_qs = Prescription.objects.select_related("patient", "doctor")
    if status_filter != "all":
        rx_qs = rx_qs.filter(status=status_filter)
    context = {
        "prescriptions": rx_qs,
        "status_filter": status_filter,
        "active_count": Prescription.objects.filter(status="active").count(),
        "completed_count": Prescription.objects.filter(status="completed").count(),
        "expired_count": Prescription.objects.filter(status="expired").count(),
    }
    return render(request, "dashboard/prescriptions.html", context)

@login_required
def prescription_add(request):
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Prescription added successfully.")
            return redirect("prescriptions")
    else:
        form = PrescriptionForm()
    return render(request, "dashboard/prescription_form.html", {"form": form, "action": "New"})

@login_required
def prescription_delete(request, pk):
    rx = get_object_or_404(Prescription, pk=pk)
    if request.method == "POST":
        rx.delete()
        messages.success(request, "Prescription deleted.")
        return redirect("prescriptions")
    return render(request, "dashboard/confirm_delete.html", {"object": rx, "type": "prescription"})

# ===================== PROFILE =====================

@login_required
def profile(request):
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        user_form = UserInfoForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile_obj)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        user_form = UserInfoForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile_obj)
    return render(request, "dashboard/profile.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "profile_obj": profile_obj,
    })


# ===================== SETTINGS (update) =====================

@login_required
def settings(request):
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, "dashboard/settings.html", {"profile_obj": profile_obj})