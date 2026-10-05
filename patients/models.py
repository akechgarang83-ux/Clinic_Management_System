from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    patient_number = models.CharField(
        max_length=20,
        unique=True
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    date_of_birth = models.DateField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    phone = models.CharField(
        max_length=20
    )

    address = models.TextField()

    emergency_contact = models.CharField(
        max_length=100,
        blank=True
    )

    emergency_phone = models.CharField(
        max_length=20,
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Active'
    )

    registration_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class MedicalRecord(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='medical_records'
    )

    visit_date = models.DateTimeField(
        auto_now_add=True
    )

    symptoms = models.TextField()

    diagnosis = models.TextField()

    treatment = models.TextField(
        blank=True
    )

    prescription = models.TextField(
        blank=True
    )

    doctor_notes = models.TextField(
        blank=True
    )

    follow_up = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.patient} - "
            f"{self.visit_date.strftime('%Y-%m-%d')}"
        )


class Appointment(models.Model):

    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Rescheduled', 'Rescheduled'),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    doctor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doctor_appointments'
    )

    appointment_date = models.DateField()

    appointment_time = models.TimeField()

    reason = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Scheduled'
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.patient} - "
            f"{self.appointment_date} "
            f"{self.appointment_time}"
        )


class DoctorAvailability(models.Model):

    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='availability'
    )

    day = models.CharField(
        max_length=10,
        choices=DAY_CHOICES
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    is_available = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.doctor.get_full_name() or self.doctor.username} - "
            f"{self.day} "
            f"{self.start_time.strftime('%H:%M')} - "
            f"{self.end_time.strftime('%H:%M')}"
        )


class Consultation(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='consultations'
    )

    doctor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consultations'
    )

    consultation_date = models.DateField(
        auto_now_add=True
    )

    consultation_time = models.TimeField(
        auto_now_add=True
    )

    chief_complaint = models.TextField()

    vital_signs = models.TextField(
        blank=True
    )

    symptoms = models.TextField(
        blank=True
    )

    diagnosis = models.TextField(
        blank=True
    )

    doctor_notes = models.TextField(
        blank=True
    )

    treatment_plan = models.TextField(
        blank=True
    )

    follow_up = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.patient} - "
            f"{self.consultation_date}"
        )


class Prescription(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Dispensed', 'Dispensed'),
        ('Cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='prescriptions'
    )

    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='prescriptions'
    )

    doctor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='prescriptions'
    )

    prescription_date = models.DateField(
        auto_now_add=True
    )

    medicine_name = models.CharField(
        max_length=200
    )

    dosage = models.CharField(
        max_length=100
    )

    frequency = models.CharField(
        max_length=100
    )

    duration = models.CharField(
        max_length=100
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    instructions = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.patient} - "
            f"{self.medicine_name} - "
            f"{self.prescription_date}"
        )

class MedicineCategory(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('Active', 'Active'),
            ('Inactive', 'Inactive'),
        ],
        default='Active'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class Medicine(models.Model):

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    category = models.ForeignKey(
        MedicineCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='medicines'
    )

    name = models.CharField(
        max_length=200,
        unique=True
    )

    generic_name = models.CharField(
        max_length=200,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    dosage_form = models.CharField(
        max_length=100,
        blank=True
    )

    strength = models.CharField(
        max_length=100,
        blank=True
    )

    manufacturer = models.CharField(
        max_length=200,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Active'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
class MedicineInventory(models.Model):

    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name='inventory_records'
    )

    batch_number = models.CharField(
        max_length=100
    )

    quantity_received = models.PositiveIntegerField(
        default=0
    )

    quantity_available = models.PositiveIntegerField(
        default=0
    )

    expiry_date = models.DateField()

    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    supplier = models.CharField(
        max_length=200,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.medicine.name} - "
            f"Batch {self.batch_number}"
        )
class StockAdjustment(models.Model):

    ADJUSTMENT_TYPES = [
        ('Stock In', 'Stock In'),
        ('Stock Out', 'Stock Out'),
        ('Correction', 'Correction'),
    ]

    inventory = models.ForeignKey(
        MedicineInventory,
        on_delete=models.CASCADE,
        related_name='stock_adjustments'
    )

    adjustment_type = models.CharField(
        max_length=20,
        choices=ADJUSTMENT_TYPES
    )

    quantity = models.PositiveIntegerField(
        default=0
    )

    reason = models.TextField(
        blank=True
    )

    adjustment_date = models.DateTimeField(
        auto_now_add=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.inventory.medicine.name} - "
            f"{self.adjustment_type} - "
            f"{self.quantity}"
        )  
class MedicineDispensing(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='medicine_dispensings'
    )

    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dispensings'
    )

    inventory = models.ForeignKey(
        MedicineInventory,
        on_delete=models.CASCADE,
        related_name='dispensings'
    )

    quantity_dispensed = models.PositiveIntegerField(
        default=1
    )

    dispensing_date = models.DateTimeField(
        auto_now_add=True
    )

    dispensed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='medicine_dispensings'
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.patient} - "
            f"{self.inventory.medicine.name} - "
            f"{self.quantity_dispensed}"
        )  
class Invoice(models.Model):

    STATUS_CHOICES = [
        ('Unpaid', 'Unpaid'),
        ('Partially Paid', 'Partially Paid'),
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='invoices'
    )

    invoice_number = models.CharField(
        max_length=50,
        unique=True
    )

    invoice_date = models.DateField(
        auto_now_add=True
    )

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    medicine_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    other_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Unpaid'
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
class ConsultationFee(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='consultation_fees'
    )

    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fees'
    )

    fee_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    description = models.TextField(
        blank=True
    )

    fee_date = models.DateField(
        auto_now_add=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.patient} - "
            f"{self.fee_amount} - "
            f"{self.fee_date}"
        )    

    def __str__(self):
        return (
            f"{self.invoice_number} - "
            f"{self.patient}"
        ) 
class MedicineCharge(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='medicine_charges'
    )

    dispensing = models.ForeignKey(
        MedicineDispensing,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='charges'
    )

    medicine_name = models.CharField(
        max_length=200
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    charge_date = models.DateField(
        auto_now_add=True
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.patient} - "
            f"{self.medicine_name} - "
            f"{self.total_charge}"
        ) 
class PaymentRecord(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Mobile Money', 'Mobile Money'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Card', 'Card'),
    ]

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='payment_records'
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='payment_records'
    )

    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES,
        default='Cash'
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    reference_number = models.CharField(
        max_length=100,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
class LabTestCategory(models.Model):

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Active'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class LabTestRequest(models.Model):

    STATUS_CHOICES = [
        ('Requested', 'Requested'),
        ('Sample Collected', 'Sample Collected'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Verified', 'Verified'),
        ('Cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='lab_test_requests'
    )

    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lab_test_requests'
    )

    test_category = models.ForeignKey(
        LabTestCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='test_requests'
    )

    test_name = models.CharField(
        max_length=200
    )

    clinical_notes = models.TextField(
        blank=True
    )

    request_date = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Requested'
    )

    requested_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lab_test_requests'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
class LabSampleCollection(models.Model):

    lab_test_request = models.OneToOneField(
        LabTestRequest,
        on_delete=models.CASCADE,
        related_name='sample_collection'
    )

    sample_type = models.CharField(
        max_length=100
    )

    collection_date = models.DateTimeField(
        auto_now_add=True
    )

    collected_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lab_sample_collections'
    )

    collection_notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return (
            f"{self.lab_test_request.patient} - "
            f"{self.sample_type}"
        )   
class LabTestProcessing(models.Model):

    lab_test_request = models.OneToOneField(
        LabTestRequest,
        on_delete=models.CASCADE,
        related_name='test_processing'
    )

    processing_date = models.DateTimeField(
        auto_now_add=True
    )

    processed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lab_test_processings'
    )

    processing_notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return (
            f"{self.lab_test_request.patient} - "
            f"{self.lab_test_request.test_name}"
        ) 
class LabTestResult(models.Model):

    lab_test_request = models.OneToOneField(
        LabTestRequest,
        on_delete=models.CASCADE,
        related_name='test_result'
    )

    result_value = models.TextField()

    reference_range = models.CharField(
        max_length=200,
        blank=True
    )

    unit = models.CharField(
        max_length=100,
        blank=True
    )

    result_notes = models.TextField(
        blank=True
    )

    result_date = models.DateTimeField(
        auto_now_add=True
    )

    recorded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lab_test_results'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return (
            f"{self.lab_test_request.patient} - "
            f"{self.lab_test_request.test_name}"
        ) 

class LabTestVerification(models.Model):

    lab_test_result = models.OneToOneField(
        LabTestResult,
        on_delete=models.CASCADE,
        related_name='verification'
    )

    verification_status = models.CharField(
        max_length=20,
        choices=[
            ('Verified', 'Verified'),
            ('Rejected', 'Rejected'),
        ],
        default='Verified'
    )

    verification_notes = models.TextField(
        blank=True
    )

    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lab_test_verifications'
    )

    verification_date = models.DateTimeField(
        auto_now_add=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return (
            f"{self.lab_test_result.lab_test_request.patient} - "
            f"{self.lab_test_result.lab_test_request.test_name} - "
            f"{self.verification_status}"
        )                       

    def __str__(self):
        return f"{self.patient} - {self.test_name}"
    def __str__(self):
        return f"{self.patient} - {self.amount_paid} - {self.payment_date}"                                  
    def __str__(self):
        return self.name