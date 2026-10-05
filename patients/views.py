from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal, InvalidOperation
from accounts.models import UserProfile

from .models import (
    Patient,
    MedicalRecord,
    Appointment,
    DoctorAvailability,
    Consultation,
    Prescription,
    MedicineCategory,
    Medicine,
    MedicineInventory,
    StockAdjustment,
    MedicineDispensing,
    Invoice,
    ConsultationFee,
    MedicineCharge,
    PaymentRecord,
    LabTestCategory,
    LabTestRequest,
    LabSampleCollection,
    LabTestProcessing,
    LabTestResult,
    LabTestVerification,   
)

def dashboard(request):

    total_patients = Patient.objects.count()

    return render(
        request,
        'dashboard.html',
        {
            'total_patients': total_patients
        }
    )


def register_patient(request):

    if request.method == 'POST':

        patient_number = request.POST.get('patient_number')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        emergency_contact = request.POST.get('emergency_contact')
        emergency_phone = request.POST.get('emergency_phone')

        Patient.objects.create(
            patient_number=patient_number,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
            phone=phone,
            address=address,
            emergency_contact=emergency_contact,
            emergency_phone=emergency_phone
        )

        return redirect('patient_list')

    return render(
        request,
        'patients/register_patient.html'
    )


def patient_list(request):

    patients = Patient.objects.all().order_by(
        '-registration_date'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:

        patients = patients.filter(
            models.Q(
                first_name__icontains=search
            )
            |
            models.Q(
                last_name__icontains=search
            )
            |
            models.Q(
                patient_number__icontains=search
            )
            |
            models.Q(
                phone__icontains=search
            )
        )

    return render(
        request,
        'patients/patient_list.html',
        {
            'patients': patients,
            'search': search
        }
    )
def patient_management(request):

    patients = Patient.objects.all().order_by(
        '-registration_date'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:

        patients = patients.filter(
            models.Q(
                first_name__icontains=search
            )
            |
            models.Q(
                last_name__icontains=search
            )
            |
            models.Q(
                patient_number__icontains=search
            )
            |
            models.Q(
                phone__icontains=search
            )
        )

    return render(
        request,
        'patients/patient_management.html',
        {
            'patients': patients,
            'search': search
        }
    )

def patient_detail(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    medical_records = patient.medical_records.all().order_by(
        '-visit_date'
    )

    appointments = patient.appointments.all().order_by(
        '-appointment_date',
        '-appointment_time'
    )

    consultations = patient.consultations.all().select_related(
        'doctor'
    ).order_by(
        '-consultation_date',
        '-consultation_time'
    )

    prescriptions = patient.prescriptions.all().select_related(
        'doctor',
        'consultation'
    ).order_by(
        '-prescription_date',
        '-created_at'
    )

    return render(
        request,
        'patients/patient_detail.html',
        {
            'patient': patient,
            'medical_records': medical_records,
            'appointments': appointments,
            'consultations': consultations,
            'prescriptions': prescriptions,
        }
    )


def edit_patient(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    if request.method == 'POST':

        patient.patient_number = request.POST.get(
            'patient_number'
        )

        patient.first_name = request.POST.get(
            'first_name'
        )

        patient.last_name = request.POST.get(
            'last_name'
        )

        patient.date_of_birth = request.POST.get(
            'date_of_birth'
        )

        patient.gender = request.POST.get(
            'gender'
        )

        patient.phone = request.POST.get(
            'phone'
        )

        patient.address = request.POST.get(
            'address'
        )

        patient.emergency_contact = request.POST.get(
            'emergency_contact'
        )

        patient.emergency_phone = request.POST.get(
            'emergency_phone'
        )

        patient.status = request.POST.get(
            'status'
        )

        patient.save()

        return redirect(
            'patient_detail',
            patient_id=patient.id
        )

    return render(
        request,
        'patients/edit_patient.html',
        {
            'patient': patient
        }
    )


def delete_patient(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    if request.method == 'POST':

        patient.delete()

        return redirect('patient_list')

    return render(
        request,
        'patients/delete_patient.html',
        {
            'patient': patient
        }
    )


def add_medical_record(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    if request.method == 'POST':

        symptoms = request.POST.get('symptoms')
        diagnosis = request.POST.get('diagnosis')
        treatment = request.POST.get('treatment')
        prescription = request.POST.get('prescription')
        doctor_notes = request.POST.get('doctor_notes')
        follow_up = request.POST.get('follow_up')

        MedicalRecord.objects.create(
            patient=patient,
            symptoms=symptoms,
            diagnosis=diagnosis,
            treatment=treatment,
            prescription=prescription,
            doctor_notes=doctor_notes,
            follow_up=follow_up
        )

        return redirect(
            'patient_detail',
            patient_id=patient.id
        )

    return render(
        request,
        'patients/medical_record_form.html',
        {
            'patient': patient
        }
    )


def book_appointment(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    if request.method == 'POST':

        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get(
            'appointment_date'
        )
        appointment_time = request.POST.get(
            'appointment_time'
        )
        reason = request.POST.get('reason')
        notes = request.POST.get('notes')

        doctor = None

        if doctor_id:

            doctor = get_object_or_404(
                User,
                id=doctor_id
            )

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=reason,
            notes=notes
        )

        return redirect(
            'patient_detail',
            patient_id=patient.id
        )

    doctors = User.objects.all().order_by(
        'first_name',
        'last_name'
    )

    return render(
        request,
        'patients/book_appointment.html',
        {
            'patient': patient,
            'doctors': doctors,
        }
    )


def appointment_list(request):

    appointments = Appointment.objects.all().select_related(
        'patient',
        'doctor'
    ).order_by(
        'appointment_date',
        'appointment_time'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    appointment_date = request.GET.get(
        'appointment_date',
        ''
    ).strip()

    doctor_id = request.GET.get(
        'doctor',
        ''
    ).strip()

    status = request.GET.get(
        'status',
        ''
    ).strip()

    if search:

        appointments = appointments.filter(
            models.Q(
                patient__first_name__icontains=search
            )
            |
            models.Q(
                patient__last_name__icontains=search
            )
            |
            models.Q(
                patient__patient_number__icontains=search
            )
        )

    if appointment_date:

        appointments = appointments.filter(
            appointment_date=appointment_date
        )

    if doctor_id:

        appointments = appointments.filter(
            doctor_id=doctor_id
        )

    if status:

        appointments = appointments.filter(
            status=status
        )

    doctors = User.objects.all().order_by(
        'first_name',
        'last_name'
    )

    return render(
        request,
        'patients/appointment_list.html',
        {
            'appointments': appointments,
            'doctors': doctors,
            'search': search,
            'appointment_date': appointment_date,
            'selected_doctor': doctor_id,
            'selected_status': status,
        }
    )
def reschedule_appointment(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    if request.method == 'POST':

        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get(
            'appointment_date'
        )
        appointment_time = request.POST.get(
            'appointment_time'
        )
        reason = request.POST.get('reason')
        notes = request.POST.get('notes')

        doctor = None

        if doctor_id:

            doctor = get_object_or_404(
                User,
                id=doctor_id
            )

        appointment.doctor = doctor
        appointment.appointment_date = appointment_date
        appointment.appointment_time = appointment_time
        appointment.reason = reason
        appointment.notes = notes
        appointment.status = 'Rescheduled'

        appointment.save()

        return redirect(
            'patient_detail',
            patient_id=appointment.patient.id
        )

    doctors = User.objects.all().order_by(
        'first_name',
        'last_name'
    )

    return render(
        request,
        'patients/reschedule_appointment.html',
        {
            'appointment': appointment,
            'doctors': doctors,
        }
    )
def cancel_appointment(request, appointment_id):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    if request.method == 'POST':

        appointment.status = 'Cancelled'

        appointment.save()

        return redirect(
            'patient_detail',
            patient_id=appointment.patient.id
        )

    return render(
        request,
        'patients/cancel_appointment.html',
        {
            'appointment': appointment
        }
    )        
def appointment_calendar(request):

    appointments = Appointment.objects.all().select_related(
        'patient',
        'doctor'
    ).order_by(
        'appointment_date',
        'appointment_time'
    )

    return render(
        request,
        'patients/appointment_calendar.html',
        {
            'appointments': appointments
        }
    )
def doctor_availability(request):

    availability = DoctorAvailability.objects.all().select_related(
        'doctor'
    ).order_by(
        'doctor__first_name',
        'doctor__last_name',
        'day',
        'start_time'
    )

    return render(
        request,
        'patients/doctor_availability.html',
        {
            'availability': availability
        }
    )
def add_doctor_availability(request):

    if request.method == 'POST':

        doctor_id = request.POST.get('doctor')
        day = request.POST.get('day')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        is_available = request.POST.get('is_available')

        doctor = get_object_or_404(
            User,
            id=doctor_id
        )

        DoctorAvailability.objects.create(
            doctor=doctor,
            day=day,
            start_time=start_time,
            end_time=end_time,
            is_available=is_available == 'True'
        )

        return redirect('doctor_availability')

    doctors = User.objects.all().order_by(
        'first_name',
        'last_name'
    )

    days = DoctorAvailability.DAY_CHOICES

    return render(
        request,
        'patients/add_doctor_availability.html',
        {
            'doctors': doctors,
            'days': days,
        }
    )  
def add_consultation(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    doctors = User.objects.filter(
        is_active=True
    ).order_by(
        'first_name',
        'last_name'
    )

    if request.method == 'POST':

        doctor_id = request.POST.get(
            'doctor'
        )

        chief_complaint = request.POST.get(
            'chief_complaint'
        )

        vital_signs = request.POST.get(
            'vital_signs'
        )

        symptoms = request.POST.get(
            'symptoms'
        )

        diagnosis = request.POST.get(
            'diagnosis'
        )

        doctor_notes = request.POST.get(
            'doctor_notes'
        )

        treatment_plan = request.POST.get(
            'treatment_plan'
        )

        follow_up = request.POST.get(
            'follow_up'
        )

        doctor = None

        if doctor_id:

            doctor = get_object_or_404(
                User,
                id=doctor_id,
                is_active=True
            )

        Consultation.objects.create(

            patient=patient,

            doctor=doctor,

            chief_complaint=chief_complaint,

            vital_signs=vital_signs,

            symptoms=symptoms,

            diagnosis=diagnosis,

            doctor_notes=doctor_notes,

            treatment_plan=treatment_plan,

            follow_up=follow_up
        )

        return redirect(
            'patient_detail',
            patient_id=patient.id
        )

    context = {
        'patient': patient,
        'doctors': doctors,
    }

    return render(
        request,
        'patients/add_consultation.html',
        context
    )

def consultation_list(request):

    consultations = Consultation.objects.select_related(
        'patient',
        'doctor'
    ).order_by(
        '-consultation_date',
        '-consultation_time'
    )

    context = {
        'consultations': consultations
    }

    return render(
        request,
        'patients/consultation_list.html',
        context
    )
def prescription_list(request):

    prescriptions = Prescription.objects.all().select_related(
        'patient',
        'doctor',
        'consultation'
    ).order_by(
        '-prescription_date',
        '-created_at'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    status = request.GET.get(
        'status',
        ''
    ).strip()

    if search:

        prescriptions = prescriptions.filter(
            models.Q(
                patient__first_name__icontains=search
            )
            |
            models.Q(
                patient__last_name__icontains=search
            )
            |
            models.Q(
                patient__patient_number__icontains=search
            )
            |
            models.Q(
                medicine_name__icontains=search
            )
        )

    if status:

        prescriptions = prescriptions.filter(
            status=status
        )

    return render(
        request,
        'patients/prescription_list.html',
        {
            'prescriptions': prescriptions,
            'search': search,
            'selected_status': status,
        }
    )


def add_prescription(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    if request.method == 'POST':

        doctor_id = request.POST.get(
            'doctor'
        )

        consultation_id = request.POST.get(
            'consultation'
        )

        medicine_name = request.POST.get(
            'medicine_name'
        )

        dosage = request.POST.get(
            'dosage'
        )

        frequency = request.POST.get(
            'frequency'
        )

        duration = request.POST.get(
            'duration'
        )

        quantity = request.POST.get(
            'quantity'
        )

        instructions = request.POST.get(
            'instructions'
        )

        doctor = None

        if doctor_id:

            doctor = get_object_or_404(
                User,
                id=doctor_id
            )

        consultation = None

        if consultation_id:

            consultation = get_object_or_404(
                Consultation,
                id=consultation_id,
                patient=patient
            )

        Prescription.objects.create(
            patient=patient,
            consultation=consultation,
            doctor=doctor,
            medicine_name=medicine_name,
            dosage=dosage,
            frequency=frequency,
            duration=duration,
            quantity=quantity,
            instructions=instructions
        )

        return redirect(
            'patient_detail',
            patient_id=patient.id
        )

    doctors = User.objects.all().order_by(
        'first_name',
        'last_name'
    )

    consultations = patient.consultations.all().order_by(
        '-consultation_date',
        '-consultation_time'
    )

    return render(
        request,
        'patients/add_prescription.html',
        {
            'patient': patient,
            'doctors': doctors,
            'consultations': consultations,
        }
    ) 
def select_patient_for_prescription(request): 
    patients = Patient.objects.all().order_by( 
    'first_name', 
    'last_name' 
    ) 
    
    return render( request, 
    'patients/select_patient_for_prescription.html', 
    { 'patients':
        patients 
    } 
    
    )    
    
def medicine_list(request):

    medicines = Medicine.objects.all().order_by(
        'name'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    status = request.GET.get(
        'status',
        ''
    ).strip()

    if search:

        medicines = medicines.filter(
            models.Q(
                name__icontains=search
            )
            |
            models.Q(
                generic_name__icontains=search
            )
            |
            models.Q(
                manufacturer__icontains=search
            )
        )

    if status:

        medicines = medicines.filter(
            status=status
        )

    return render(
        request,
        'patients/medicine_list.html',
        {
            'medicines': medicines,
            'search': search,
            'selected_status': status,
        }
    )


def add_medicine(request):

    if request.method == 'POST':

        name = request.POST.get(
            'name'
        )

        generic_name = request.POST.get(
            'generic_name'
        )

        description = request.POST.get(
            'description'
        )

        dosage_form = request.POST.get(
            'dosage_form'
        )

        strength = request.POST.get(
            'strength'
        )

        manufacturer = request.POST.get(
            'manufacturer'
        )

        status = request.POST.get(
            'status'
        )

        Medicine.objects.create(
            name=name,
            generic_name=generic_name,
            description=description,
            dosage_form=dosage_form,
            strength=strength,
            manufacturer=manufacturer,
            status=status
        )

        return redirect(
            'medicine_list'
        )

    return render(
        request,
        'patients/add_medicine.html'
    )   
def medicine_category_list(request):

    categories = MedicineCategory.objects.all().order_by(
        'name'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    status = request.GET.get(
        'status',
        ''
    ).strip()

    if search:

        categories = categories.filter(
            models.Q(
                name__icontains=search
            )
            |
            models.Q(
                description__icontains=search
            )
        )

    if status:

        categories = categories.filter(
            status=status
        )

    return render(
        request,
        'patients/medicine_category_list.html',
        {
            'categories': categories,
            'search': search,
            'selected_status': status,
        }
    )


def add_medicine_category(request):

    if request.method == 'POST':

        name = request.POST.get(
            'name'
        )

        description = request.POST.get(
            'description'
        )

        status = request.POST.get(
            'status'
        )

        MedicineCategory.objects.create(
            name=name,
            description=description,
            status=status
        )

        return redirect(
            'medicine_category_list'
        )

    return render(
        request,
        'patients/add_medicine_category.html'
    )
def medicine_inventory_list(request):

    inventory = MedicineInventory.objects.all().select_related(
        'medicine'
    ).order_by(
        'medicine__name',
        'expiry_date'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:

        inventory = inventory.filter(
            models.Q(
                medicine__name__icontains=search
            )
            |
            models.Q(
                medicine__generic_name__icontains=search
            )
            |
            models.Q(
                batch_number__icontains=search
            )
            |
            models.Q(
                supplier__icontains=search
            )
        )

    return render(
        request,
        'patients/medicine_inventory_list.html',
        {
            'inventory': inventory,
            'search': search,
        }
    )


def add_medicine_inventory(request):

    if request.method == 'POST':

        medicine_id = request.POST.get(
            'medicine'
        )

        batch_number = request.POST.get(
            'batch_number'
        )

        quantity_received = request.POST.get(
            'quantity_received'
        )

        quantity_available = request.POST.get(
            'quantity_available'
        )

        expiry_date = request.POST.get(
            'expiry_date'
        )

        purchase_price = request.POST.get(
            'purchase_price'
        )

        selling_price = request.POST.get(
            'selling_price'
        )

        supplier = request.POST.get(
            'supplier'
        )

        medicine = get_object_or_404(
            Medicine,
            id=medicine_id
        )

        MedicineInventory.objects.create(
            medicine=medicine,
            batch_number=batch_number,
            quantity_received=quantity_received,
            quantity_available=quantity_available,
            expiry_date=expiry_date,
            purchase_price=purchase_price,
            selling_price=selling_price,
            supplier=supplier
        )

        return redirect(
            'medicine_inventory_list'
        )

    medicines = Medicine.objects.filter(
        status='Active'
    ).order_by(
        'name'
    )

    return render(
        request,
        'patients/add_medicine_inventory.html',
        {
            'medicines': medicines,
        }
    ) 
def stock_adjustment_list(request):

    adjustments = StockAdjustment.objects.all().select_related(
        'inventory',
        'inventory__medicine'
    ).order_by(
        '-adjustment_date'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    adjustment_type = request.GET.get(
        'adjustment_type',
        ''
    ).strip()

    if search:

        adjustments = adjustments.filter(
            models.Q(
                inventory__medicine__name__icontains=search
            )
            |
            models.Q(
                inventory__batch_number__icontains=search
            )
            |
            models.Q(
                reason__icontains=search
            )
        )

    if adjustment_type:

        adjustments = adjustments.filter(
            adjustment_type=adjustment_type
        )

    return render(
        request,
        'patients/stock_adjustment_list.html',
        {
            'adjustments': adjustments,
            'search': search,
            'selected_adjustment_type': adjustment_type,
        }
    )


def add_stock_adjustment(request):

    if request.method == 'POST':

        inventory_id = request.POST.get(
            'inventory'
        )

        adjustment_type = request.POST.get(
            'adjustment_type'
        )

        quantity = request.POST.get(
            'quantity'
        )

        reason = request.POST.get(
            'reason'
        )

        inventory = get_object_or_404(
            MedicineInventory,
            id=inventory_id
        )

        quantity = int(quantity)

        if adjustment_type == 'Stock In':

            inventory.quantity_available += quantity

        elif adjustment_type == 'Stock Out':

            if quantity > inventory.quantity_available:

                return render(
                    request,
                    'patients/add_stock_adjustment.html',
                    {
                        'inventory_records': MedicineInventory.objects.all().select_related(
                            'medicine'
                        ).order_by(
                            'medicine__name'
                        ),
                        'error': 'Stock Out quantity cannot be greater than the available stock.',
                    }
                )

            inventory.quantity_available -= quantity

        elif adjustment_type == 'Correction':

            inventory.quantity_available = quantity

        inventory.save()

        StockAdjustment.objects.create(
            inventory=inventory,
            adjustment_type=adjustment_type,
            quantity=quantity,
            reason=reason
        )

        return redirect(
            'stock_adjustment_list'
        )

    inventory_records = MedicineInventory.objects.all().select_related(
        'medicine'
    ).order_by(
        'medicine__name',
        'batch_number'
    )

    return render(
        request,
        'patients/add_stock_adjustment.html',
        {
            'inventory_records': inventory_records,
        }
    ) 
def medicine_dispensing_list(request):

    dispensings = MedicineDispensing.objects.all().select_related(
        'patient',
        'prescription',
        'inventory',
        'inventory__medicine',
        'dispensed_by'
    ).order_by(
        '-dispensing_date'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:

        dispensings = dispensings.filter(
            models.Q(
                patient__first_name__icontains=search
            )
            |
            models.Q(
                patient__last_name__icontains=search
            )
            |
            models.Q(
                inventory__medicine__name__icontains=search
            )
            |
            models.Q(
                inventory__batch_number__icontains=search
            )
        )

    return render(
        request,
        'patients/medicine_dispensing_list.html',
        {
            'dispensings': dispensings,
            'search': search,
        }
    )


def add_medicine_dispensing(request):

    if request.method == 'POST':

        patient_id = request.POST.get(
            'patient'
        )

        prescription_id = request.POST.get(
            'prescription'
        )

        inventory_id = request.POST.get(
            'inventory'
        )

        quantity = request.POST.get(
            'quantity_dispensed'
        )

        notes = request.POST.get(
            'notes'
        )

        patient = get_object_or_404(
            Patient,
            id=patient_id
        )

        inventory = get_object_or_404(
            MedicineInventory,
            id=inventory_id
        )

        prescription = None

        if prescription_id:

            prescription = get_object_or_404(
                Prescription,
                id=prescription_id
            )

        quantity = int(quantity)

        if quantity <= 0:

            return render(
                request,
                'patients/add_medicine_dispensing.html',
                {
                    'patients': Patient.objects.all().order_by(
                        'first_name',
                        'last_name'
                    ),
                    'prescriptions': Prescription.objects.filter(
                        status='Pending'
                    ).select_related(
                        'patient'
                    ).order_by(
                        '-prescription_date'
                    ),
                    'inventory_records': MedicineInventory.objects.filter(
                        quantity_available__gt=0
                    ).select_related(
                        'medicine'
                    ).order_by(
                        'medicine__name',
                        'batch_number'
                    ),
                    'error': 'Quantity dispensed must be greater than zero.',
                }
            )

        if quantity > inventory.quantity_available:

            return render(
                request,
                'patients/add_medicine_dispensing.html',
                {
                    'patients': Patient.objects.all().order_by(
                        'first_name',
                        'last_name'
                    ),
                    'prescriptions': Prescription.objects.filter(
                        status='Pending'
                    ).select_related(
                        'patient'
                    ).order_by(
                        '-prescription_date'
                    ),
                    'inventory_records': MedicineInventory.objects.filter(
                        quantity_available__gt=0
                    ).select_related(
                        'medicine'
                    ).order_by(
                        'medicine__name',
                        'batch_number'
                    ),
                    'error': (
                        'Cannot dispense more than the '
                        'available stock.'
                    ),
                }
            )

        inventory.quantity_available -= quantity

        inventory.save()

        MedicineDispensing.objects.create(
            patient=patient,
            prescription=prescription,
            inventory=inventory,
            quantity_dispensed=quantity,
            dispensed_by=request.user,
            notes=notes
        )

        StockAdjustment.objects.create(
            inventory=inventory,
            adjustment_type='Stock Out',
            quantity=quantity,
            reason='Medicine dispensed'
        )

        if prescription:

            prescription.status = 'Dispensed'

            prescription.save()

        return redirect(
            'medicine_dispensing_list'
        )

    patients = Patient.objects.all().order_by(
        'first_name',
        'last_name'
    )

    prescriptions = Prescription.objects.filter(
        status='Pending'
    ).select_related(
        'patient'
    ).order_by(
        '-prescription_date'
    )

    inventory_records = MedicineInventory.objects.filter(
        quantity_available__gt=0
    ).select_related(
        'medicine'
    ).order_by(
        'medicine__name',
        'batch_number'
    )

    return render(
        request,
        'patients/add_medicine_dispensing.html',
        {
            'patients': patients,
            'prescriptions': prescriptions,
            'inventory_records': inventory_records,
        }
    )  
def low_stock_alert(request):

    low_stock_items = MedicineInventory.objects.filter(
        quantity_available__lte=10
    ).select_related(
        'medicine'
    ).order_by(
        'quantity_available',
        'medicine__name'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:

        low_stock_items = low_stock_items.filter(
            models.Q(
                medicine__name__icontains=search
            )
            |
            models.Q(
                batch_number__icontains=search
            )
        )

    return render(
        request,
        'patients/low_stock_alert.html',
        {
            'low_stock_items': low_stock_items,
            'search': search,
        }
    )  
def prescription_history(request):

    prescriptions = Prescription.objects.all().select_related(
        'patient',
        'doctor',
        'consultation'
    ).order_by(
        '-prescription_date',
        '-created_at'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    status = request.GET.get(
        'status',
        ''
    ).strip()

    if search:

        prescriptions = prescriptions.filter(
            models.Q(
                patient__first_name__icontains=search
            )
            |
            models.Q(
                patient__last_name__icontains=search
            )
            |
            models.Q(
                medicine_name__icontains=search
            )
            |
            models.Q(
                dosage__icontains=search
            )
        )

    if status:

        prescriptions = prescriptions.filter(
            status=status
        )

    return render(
        request,
        'patients/prescription_history.html',
        {
            'prescriptions': prescriptions,
            'search': search,
            'selected_status': status,
        }
    )
def invoice_list(request):

    invoices = Invoice.objects.all().select_related(
        'patient'
    ).order_by(
        '-invoice_date',
        '-created_at'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    status = request.GET.get(
        'status',
        ''
    ).strip()

    if search:

        invoices = invoices.filter(
            models.Q(
                invoice_number__icontains=search
            )
            |
            models.Q(
                patient__first_name__icontains=search
            )
            |
            models.Q(
                patient__last_name__icontains=search
            )
        )

    if status:

        invoices = invoices.filter(
            status=status
        )

    return render(
        request,
        'patients/invoice_list.html',
        {
            'invoices': invoices,
            'search': search,
            'selected_status': status,
        }
    )


def add_invoice(request):

    if request.method == 'POST':

        patient_id = request.POST.get(
            'patient'
        )

        invoice_number = request.POST.get(
            'invoice_number'
        )

        consultation_fee = request.POST.get(
            'consultation_fee',
            '0'
        )

        medicine_charge = request.POST.get(
            'medicine_charge',
            '0'
        )

        other_charge = request.POST.get(
            'other_charge',
            '0'
        )

        amount_paid = request.POST.get(
            'amount_paid',
            '0'
        )

        description = request.POST.get(
            'description'
        )

        patient = get_object_or_404(
            Patient,
            id=patient_id
        )

        consultation_fee = float(
            consultation_fee or 0
        )

        medicine_charge = float(
            medicine_charge or 0
        )

        other_charge = float(
            other_charge or 0
        )

        amount_paid = float(
            amount_paid or 0
        )

        total_amount = (
            consultation_fee
            + medicine_charge
            + other_charge
        )

        balance = (
            total_amount
            - amount_paid
        )

        if balance < 0:

            balance = 0

        if amount_paid <= 0:

            status = 'Unpaid'

        elif amount_paid >= total_amount:

            status = 'Paid'

        else:

            status = 'Partially Paid'

        Invoice.objects.create(
            patient=patient,
            invoice_number=invoice_number,
            consultation_fee=consultation_fee,
            medicine_charge=medicine_charge,
            other_charge=other_charge,
            total_amount=total_amount,
            amount_paid=amount_paid,
            balance=balance,
            status=status,
            description=description
        )

        return redirect(
            'invoice_list'
        )

    patients = Patient.objects.all().order_by(
        'first_name',
        'last_name'
    )

    return render(
        request,
        'patients/add_invoice.html',
        {
            'patients': patients,
        }
    )  
def consultation_fee_list(request):

    fees = ConsultationFee.objects.all().select_related(
        'patient',
        'consultation'
    ).order_by(
        '-fee_date',
        '-created_at'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:

        fees = fees.filter(
            models.Q(
                patient__first_name__icontains=search
            )
            |
            models.Q(
                patient__last_name__icontains=search
            )
            |
            models.Q(
                patient__patient_number__icontains=search
            )
            |
            models.Q(
                description__icontains=search
            )
        )

    return render(
        request,
        'patients/consultation_fee_list.html',
        {
            'fees': fees,
            'search': search,
        }
    )


def add_consultation_fee(request):

    if request.method == 'POST':

        patient_id = request.POST.get(
            'patient'
        )

        consultation_id = request.POST.get(
            'consultation'
        )

        fee_amount = request.POST.get(
            'fee_amount',
            '0'
        )

        description = request.POST.get(
            'description'
        )

        patient = get_object_or_404(
            Patient,
            id=patient_id
        )

        consultation = None

        if consultation_id:

            consultation = get_object_or_404(
                Consultation,
                id=consultation_id
            )

        fee_amount = float(
            fee_amount or 0
        )

        if fee_amount < 0:

            return render(
                request,
                'patients/add_consultation_fee.html',
                {
                    'patients': Patient.objects.all().order_by(
                        'first_name',
                        'last_name'
                    ),
                    'consultations': Consultation.objects.all().select_related(
                        'patient',
                        'doctor'
                    ).order_by(
                        '-consultation_date',
                        '-consultation_time'
                    ),
                    'error': 'Consultation fee cannot be negative.',
                }
            )

        ConsultationFee.objects.create(
            patient=patient,
            consultation=consultation,
            fee_amount=fee_amount,
            description=description
        )

        return redirect(
            'consultation_fee_list'
        )

    patients = Patient.objects.all().order_by(
        'first_name',
        'last_name'
    )

    consultations = Consultation.objects.all().select_related(
        'patient',
        'doctor'
    ).order_by(
        '-consultation_date',
        '-consultation_time'
    )

    return render(
        request,
        'patients/add_consultation_fee.html',
        {
            'patients': patients,
            'consultations': consultations,
        }
    )  
def medicine_charge_list(request):

    charges = MedicineCharge.objects.all().select_related(
        'patient',
        'dispensing',
        'dispensing__inventory',
        'dispensing__inventory__medicine'
    ).order_by(
        '-charge_date',
        '-created_at'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:

        charges = charges.filter(
            models.Q(
                patient__first_name__icontains=search
            )
            |
            models.Q(
                patient__last_name__icontains=search
            )
            |
            models.Q(
                patient__patient_number__icontains=search
            )
            |
            models.Q(
                medicine_name__icontains=search
            )
        )

    return render(
        request,
        'patients/medicine_charge_list.html',
        {
            'charges': charges,
            'search': search,
        }
    )


def add_medicine_charge(request):

    if request.method == 'POST':

        patient_id = request.POST.get(
            'patient'
        )

        dispensing_id = request.POST.get(
            'dispensing'
        )

        medicine_name = request.POST.get(
            'medicine_name'
        )

        quantity = request.POST.get(
            'quantity',
            '1'
        )

        unit_price = request.POST.get(
            'unit_price',
            '0'
        )

        description = request.POST.get(
            'description'
        )

        patient = get_object_or_404(
            Patient,
            id=patient_id
        )

        dispensing = None

        if dispensing_id:

            dispensing = get_object_or_404(
                MedicineDispensing,
                id=dispensing_id
            )

        quantity = int(
            quantity or 1
        )

        unit_price = float(
            unit_price or 0
        )

        if quantity <= 0:

            return render(
                request,
                'patients/add_medicine_charge.html',
                {
                    'patients': Patient.objects.all().order_by(
                        'first_name',
                        'last_name'
                    ),
                    'dispensings': MedicineDispensing.objects.all().select_related(
                        'patient',
                        'inventory',
                        'inventory__medicine'
                    ).order_by(
                        '-dispensing_date'
                    ),
                    'error': 'Quantity must be greater than zero.',
                }
            )

        if unit_price < 0:

            return render(
                request,
                'patients/add_medicine_charge.html',
                {
                    'patients': Patient.objects.all().order_by(
                        'first_name',
                        'last_name'
                    ),
                    'dispensings': MedicineDispensing.objects.all().select_related(
                        'patient',
                        'inventory',
                        'inventory__medicine'
                    ).order_by(
                        '-dispensing_date'
                    ),
                    'error': 'Unit price cannot be negative.',
                }
            )

        total_charge = quantity * unit_price

        MedicineCharge.objects.create(
            patient=patient,
            dispensing=dispensing,
            medicine_name=medicine_name,
            quantity=quantity,
            unit_price=unit_price,
            total_charge=total_charge,
            description=description
        )

        return redirect(
            'medicine_charge_list'
        )

    patients = Patient.objects.all().order_by(
        'first_name',
        'last_name'
    )

    dispensings = MedicineDispensing.objects.all().select_related(
        'patient',
        'inventory',
        'inventory__medicine'
    ).order_by(
        '-dispensing_date'
    )

    return render(
        request,
        'patients/add_medicine_charge.html',
        {
            'patients': patients,
            'dispensings': dispensings,
        }
    )  
def payment_record_list(request):

    payments = PaymentRecord.objects.all().select_related(
        'invoice',
        'patient'
    ).order_by(
        '-payment_date',
        '-created_at'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:

        payments = payments.filter(
            models.Q(
                patient__first_name__icontains=search
            )
            |
            models.Q(
                patient__last_name__icontains=search
            )
            |
            models.Q(
                patient__patient_number__icontains=search
            )
            |
            models.Q(
                invoice__invoice_number__icontains=search
            )
            |
            models.Q(
                reference_number__icontains=search
            )
        )

    return render(
        request,
        'patients/payment_record_list.html',
        {
            'payments': payments,
            'search': search,
        }
    )


def add_payment_record(request):

    if request.method == 'POST':

        invoice_id = request.POST.get(
            'invoice'
        )

        amount_paid = request.POST.get(
            'amount_paid',
            '0'
        )

        payment_method = request.POST.get(
            'payment_method'
        )

        reference_number = request.POST.get(
            'reference_number',
            ''
        ).strip()

        notes = request.POST.get(
            'notes',
            ''
        ).strip()

        invoice = get_object_or_404(
            Invoice,
            id=invoice_id
        )

        try:

            amount_paid = Decimal(
                amount_paid or '0'
            )

        except (InvalidOperation, ValueError):

            return render(
                request,
                'patients/add_payment_record.html',
                {
                    'invoices': Invoice.objects.all().select_related(
                        'patient'
                    ).order_by(
                        '-invoice_date'
                    ),
                    'error': 'Please enter a valid payment amount.',
                }
            )

        if amount_paid <= Decimal('0'):

            return render(
                request,
                'patients/add_payment_record.html',
                {
                    'invoices': Invoice.objects.all().select_related(
                        'patient'
                    ).order_by(
                        '-invoice_date'
                    ),
                    'error': 'Payment amount must be greater than zero.',
                }
            )

        if amount_paid > invoice.balance:

            return render(
                request,
                'patients/add_payment_record.html',
                {
                    'invoices': Invoice.objects.all().select_related(
                        'patient'
                    ).order_by(
                        '-invoice_date'
                    ),
                    'error': 'Payment amount cannot be greater than the outstanding balance.',
                }
            )

        PaymentRecord.objects.create(
            invoice=invoice,
            patient=invoice.patient,
            amount_paid=amount_paid,
            payment_method=payment_method,
            reference_number=reference_number,
            notes=notes
        )

        invoice.amount_paid = (
            invoice.amount_paid
            + amount_paid
        )

        invoice.balance = (
            invoice.total_amount
            - invoice.amount_paid
        )

        if invoice.balance <= Decimal('0'):

            invoice.balance = Decimal('0.00')
            invoice.status = 'Paid'

        elif invoice.amount_paid > Decimal('0'):

            invoice.status = 'Partially Paid'

        else:

            invoice.status = 'Unpaid'

        invoice.save()

        return redirect(
            'payment_record_list'
        )

    invoices = Invoice.objects.all().select_related(
        'patient'
    ).order_by(
        '-invoice_date'
    )

    return render(
        request,
        'patients/add_payment_record.html',
        {
            'invoices': invoices,
        }
    )  
def delete_payment_record(request, payment_id):

    payment = get_object_or_404(
        PaymentRecord,
        id=payment_id
    )

    if request.method == 'POST':

        invoice = payment.invoice

        payment.delete()

        total_paid = PaymentRecord.objects.filter(
            invoice=invoice
        ).aggregate(
            total=models.Sum('amount_paid')
        )['total'] or Decimal('0.00')

        invoice.amount_paid = total_paid

        invoice.balance = (
            invoice.total_amount
            - invoice.amount_paid
        )

        if invoice.balance <= Decimal('0'):

            invoice.balance = Decimal('0.00')
            invoice.status = 'Paid'

        elif invoice.amount_paid > Decimal('0'):

            invoice.status = 'Partially Paid'

        else:

            invoice.status = 'Unpaid'

        invoice.save()

        return redirect(
            'payment_record_list'
        )

    return render(
        request,
        'patients/delete_payment_record.html',
        {
            'payment': payment,
        }
    )              

def payment_receipt(request, payment_id):

    payment = get_object_or_404(
        PaymentRecord.objects.select_related(
            'invoice',
            'patient'
        ),
        id=payment_id
    )

    invoice = payment.invoice

    previous_payments = PaymentRecord.objects.filter(
        invoice=invoice,
        payment_date__lt=payment.payment_date
    ).aggregate(
        total=models.Sum('amount_paid')
    )['total'] or Decimal('0.00')

    current_balance = (
        invoice.total_amount
        - invoice.amount_paid
    )

    return render(
        request,
        'patients/payment_receipt.html',
        {
            'payment': payment,
            'invoice': invoice,
            'patient': payment.patient,
            'previous_payments': previous_payments,
            'current_balance': current_balance,
        }
    ) 
    
def outstanding_balance(request):

    invoices = Invoice.objects.filter(
        balance__gt=Decimal('0.00')
    ).select_related(
        'patient'
    ).order_by(
        '-invoice_date'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:

        invoices = invoices.filter(
            models.Q(
                patient__first_name__icontains=search
            )
            |
            models.Q(
                patient__last_name__icontains=search
            )
            |
            models.Q(
                patient__patient_number__icontains=search
            )
            |
            models.Q(
                invoice_number__icontains=search
            )
        )

    total_outstanding = invoices.aggregate(
        total=models.Sum('balance')
    )['total'] or Decimal('0.00')

    return render(
        request,
        'patients/outstanding_balance.html',
        {
            'invoices': invoices,
            'search': search,
            'total_outstanding': total_outstanding,
        }
    ) 

def lab_test_request_list(request):

    requests = LabTestRequest.objects.all().select_related(
        'patient',
        'consultation',
        'test_category',
        'requested_by'
    ).order_by(
        '-request_date'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:

        requests = requests.filter(
            models.Q(
                patient__first_name__icontains=search
            )
            |
            models.Q(
                patient__last_name__icontains=search
            )
            |
            models.Q(
                patient__patient_number__icontains=search
            )
            |
            models.Q(
                test_name__icontains=search
            )
            |
            models.Q(
                test_category__name__icontains=search
            )
        )

    return render(
        request,
        'patients/lab_test_request_list.html',
        {
            'requests': requests,
            'search': search,
        }
    )


def add_lab_test_request(request):

    patients = Patient.objects.all().order_by(
        'first_name',
        'last_name'
    )

    consultations = Consultation.objects.all().select_related(
        'patient'
    ).order_by(
        '-consultation_date',
        '-consultation_time'
    )

    categories = LabTestCategory.objects.filter(
        status='Active'
    ).order_by(
        'name'
    )

    if request.method == 'POST':

        patient_id = request.POST.get(
            'patient'
        )

        consultation_id = request.POST.get(
            'consultation'
        )

        category_id = request.POST.get(
            'test_category'
        )

        test_name = request.POST.get(
            'test_name',
            ''
        ).strip()

        clinical_notes = request.POST.get(
            'clinical_notes',
            ''
        ).strip()

        patient = get_object_or_404(
            Patient,
            id=patient_id
        )

        consultation = None

        if consultation_id:

            consultation = get_object_or_404(
                Consultation,
                id=consultation_id
            )

        test_category = None

        if category_id:

            test_category = get_object_or_404(
                LabTestCategory,
                id=category_id
            )

        if not test_name:

            return render(
                request,
                'patients/add_lab_test_request.html',
                {
                    'patients': patients,
                    'consultations': consultations,
                    'categories': categories,
                    'error': 'Please enter the laboratory test name.',
                }
            )

        LabTestRequest.objects.create(
            patient=patient,
            consultation=consultation,
            test_category=test_category,
            test_name=test_name,
            clinical_notes=clinical_notes,
            requested_by=request.user if request.user.is_authenticated else None
        )

        return redirect(
            'lab_test_request_list'
        )

    return render(
        request,
        'patients/add_lab_test_request.html',
        {
            'patients': patients,
            'consultations': consultations,
            'categories': categories,
        }
    )  
def lab_test_category_list(request):

    categories = LabTestCategory.objects.all().order_by(
        'name'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:

        categories = categories.filter(
            models.Q(
                name__icontains=search
            )
            |
            models.Q(
                description__icontains=search
            )
        )

    return render(
        request,
        'patients/lab_test_category_list.html',
        {
            'categories': categories,
            'search': search,
        }
    )


def add_lab_test_category(request):

    if request.method == 'POST':

        name = request.POST.get(
            'name',
            ''
        ).strip()

        description = request.POST.get(
            'description',
            ''
        ).strip()

        status = request.POST.get(
            'status',
            'Active'
        )

        if not name:

            return render(
                request,
                'patients/add_lab_test_category.html',
                {
                    'error': 'Please enter the laboratory test category name.',
                }
            )

        if LabTestCategory.objects.filter(
            name__iexact=name
        ).exists():

            return render(
                request,
                'patients/add_lab_test_category.html',
                {
                    'error': 'This laboratory test category already exists.',
                    'name': name,
                    'description': description,
                    'status': status,
                }
            )

        LabTestCategory.objects.create(
            name=name,
            description=description,
            status=status
        )

        return redirect(
            'lab_test_category_list'
        )

    return render(
        request,
        'patients/add_lab_test_category.html'
    )
def lab_sample_collection_list(request):

    collections = LabSampleCollection.objects.all().select_related(
        'lab_test_request',
        'lab_test_request__patient',
        'lab_test_request__test_category',
        'collected_by'
    ).order_by(
        '-collection_date'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:

        collections = collections.filter(
            models.Q(
                lab_test_request__patient__first_name__icontains=search
            )
            |
            models.Q(
                lab_test_request__patient__last_name__icontains=search
            )
            |
            models.Q(
                lab_test_request__patient__patient_number__icontains=search
            )
            |
            models.Q(
                lab_test_request__test_name__icontains=search
            )
            |
            models.Q(
                sample_type__icontains=search
            )
        )

    return render(
        request,
        'patients/lab_sample_collection_list.html',
        {
            'collections': collections,
            'search': search,
        }
    )


def add_lab_sample_collection(request):

    test_requests = LabTestRequest.objects.filter(
        status='Requested'
    ).exclude(
        sample_collection__isnull=False
    ).select_related(
        'patient',
        'test_category'
    ).order_by(
        '-request_date'
    )

    if request.method == 'POST':

        test_request_id = request.POST.get(
            'lab_test_request'
        )

        sample_type = request.POST.get(
            'sample_type',
            ''
        ).strip()

        collection_notes = request.POST.get(
            'collection_notes',
            ''
        ).strip()

        if not test_request_id:

            return render(
                request,
                'patients/add_lab_sample_collection.html',
                {
                    'test_requests': test_requests,
                    'error': 'Please select a laboratory test request.',
                }
            )

        if not sample_type:

            return render(
                request,
                'patients/add_lab_sample_collection.html',
                {
                    'test_requests': test_requests,
                    'error': 'Please enter the sample type.',
                }
            )

        lab_test_request = get_object_or_404(
            LabTestRequest,
            id=test_request_id
        )

        if hasattr(
            lab_test_request,
            'sample_collection'
        ):

            return render(
                request,
                'patients/add_lab_sample_collection.html',
                {
                    'test_requests': test_requests,
                    'error': 'A sample has already been collected for this test request.',
                }
            )

        LabSampleCollection.objects.create(
            lab_test_request=lab_test_request,
            sample_type=sample_type,
            collection_notes=collection_notes,
            collected_by=request.user if request.user.is_authenticated else None
        )

        lab_test_request.status = 'Sample Collected'

        lab_test_request.save(
            update_fields=[
                'status',
                'updated_at'
            ]
        )

        return redirect(
            'lab_sample_collection_list'
        )

    return render(
        request,
        'patients/add_lab_sample_collection.html',
        {
            'test_requests': test_requests,
        }
    ) 
def lab_test_processing_list(request):

    processings = LabTestProcessing.objects.all().select_related(
        'lab_test_request',
        'lab_test_request__patient',
        'lab_test_request__test_category',
        'processed_by'
    ).order_by(
        '-processing_date'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:

        processings = processings.filter(
            models.Q(
                lab_test_request__patient__first_name__icontains=search
            )
            |
            models.Q(
                lab_test_request__patient__last_name__icontains=search
            )
            |
            models.Q(
                lab_test_request__patient__patient_number__icontains=search
            )
            |
            models.Q(
                lab_test_request__test_name__icontains=search
            )
            |
            models.Q(
                processing_notes__icontains=search
            )
        )

    return render(
        request,
        'patients/lab_test_processing_list.html',
        {
            'processings': processings,
            'search': search,
        }
    )


def add_lab_test_processing(request):

    test_requests = LabTestRequest.objects.filter(
        status='Sample Collected'
    ).exclude(
        test_processing__isnull=False
    ).select_related(
        'patient',
        'test_category'
    ).order_by(
        '-request_date'
    )

    if request.method == 'POST':

        test_request_id = request.POST.get(
            'lab_test_request'
        )

        processing_notes = request.POST.get(
            'processing_notes',
            ''
        ).strip()

        if not test_request_id:

            return render(
                request,
                'patients/add_lab_test_processing.html',
                {
                    'test_requests': test_requests,
                    'error': 'Please select a laboratory test request.',
                }
            )

        lab_test_request = get_object_or_404(
            LabTestRequest,
            id=test_request_id
        )

        if hasattr(
            lab_test_request,
            'test_processing'
        ):

            return render(
                request,
                'patients/add_lab_test_processing.html',
                {
                    'test_requests': test_requests,
                    'error': 'This laboratory test has already been processed.',
                }
            )

        LabTestProcessing.objects.create(
            lab_test_request=lab_test_request,
            processing_notes=processing_notes,
            processed_by=request.user
            if request.user.is_authenticated
            else None
        )

        lab_test_request.status = 'Processing'

        lab_test_request.save(
            update_fields=[
                'status',
                'updated_at'
            ]
        )

        return redirect(
            'lab_test_processing_list'
        )

    return render(
        request,
        'patients/add_lab_test_processing.html',
        {
            'test_requests': test_requests,
        }
    ) 
def lab_test_result_list(request):

    results = LabTestResult.objects.all().select_related(
        'lab_test_request',
        'lab_test_request__patient',
        'lab_test_request__test_category',
        'recorded_by'
    ).order_by(
        '-result_date'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:

        results = results.filter(
            models.Q(
                lab_test_request__patient__first_name__icontains=search
            )
            |
            models.Q(
                lab_test_request__patient__last_name__icontains=search
            )
            |
            models.Q(
                lab_test_request__patient__patient_number__icontains=search
            )
            |
            models.Q(
                lab_test_request__test_name__icontains=search
            )
            |
            models.Q(
                result_value__icontains=search
            )
            |
            models.Q(
                result_notes__icontains=search
            )
        )

    return render(
        request,
        'patients/lab_test_result_list.html',
        {
            'results': results,
            'search': search,
        }
    )

def add_lab_test_result(request):
    """
    Record the result of a completed laboratory test.
    Tests that have completed processing are available for result entry.
    """

    # Get laboratory test requests that have completed processing
    processed_requests = LabTestRequest.objects.filter(
        status__in=['Processing', 'Completed']
    ).select_related(
        'patient',
        'test_category'
    ).order_by('-request_date')

    if request.method == 'POST':
        test_request_id = request.POST.get('test_request')
        result_value = request.POST.get('result_value')
        result_unit = request.POST.get('result_unit')
        reference_range = request.POST.get('reference_range')
        interpretation = request.POST.get('interpretation')
        remarks = request.POST.get('remarks')

        if not test_request_id:
            return render(
                request,
                'patients/add_lab_test_result.html',
                {
                    'processed_requests': processed_requests,
                    'error': 'Please select a laboratory test.'
                }
            )

        test_request = get_object_or_404(
            LabTestRequest,
            id=test_request_id
        )

        # Allow results only after processing has started/completed
        if test_request.status not in ['Processing', 'Completed']:
            return render(
                request,
                'patients/add_lab_test_result.html',
                {
                    'processed_requests': processed_requests,
                    'error': (
                        'Only laboratory tests that are Processing '
                        'or Completed can have results recorded.'
                    )
                }
            )

        LabTestResult.objects.create(
            test_request=test_request,
            result_value=result_value,
            result_unit=result_unit,
            reference_range=reference_range,
            interpretation=interpretation,
            remarks=remarks,
            recorded_by=request.user
        )

        # Move the laboratory request to result-recorded stage
        test_request.status = 'Result Recorded'
        test_request.save()

        return redirect('lab_test_result_list')

    context = {
        'processed_requests': processed_requests,
    }

    return render(
        request,
        'patients/add_lab_test_result.html',
        context
    )
  

def lab_test_verification_list(request):

    verifications = LabTestVerification.objects.all().select_related(
        'lab_test_result',
        'lab_test_result__lab_test_request',
        'lab_test_result__lab_test_request__patient',
        'lab_test_result__lab_test_request__test_category',
        'verified_by'
    ).order_by(
        '-verification_date'
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:

        verifications = verifications.filter(
            models.Q(
                lab_test_result__lab_test_request__patient__first_name__icontains=search
            )
            |
            models.Q(
                lab_test_result__lab_test_request__patient__last_name__icontains=search
            )
            |
            models.Q(
                lab_test_result__lab_test_request__patient__patient_number__icontains=search
            )
            |
            models.Q(
                lab_test_result__lab_test_request__test_name__icontains=search
            )
            |
            models.Q(
                lab_test_result__result_value__icontains=search
            )
            |
            models.Q(
                verification_status__icontains=search
            )
        )

    return render(
        request,
        'patients/lab_test_verification_list.html',
        {
            'verifications': verifications,
            'search': search,
        }
    )


def add_lab_test_verification(request):

    test_results = LabTestResult.objects.filter(
        lab_test_request__status='Completed'
    ).exclude(
        verification__isnull=False
    ).select_related(
        'lab_test_request',
        'lab_test_request__patient',
        'lab_test_request__test_category'
    ).order_by(
        '-result_date'
    )

    if request.method == 'POST':

        test_result_id = request.POST.get(
            'lab_test_result'
        )

        verification_status = request.POST.get(
            'verification_status',
            'Verified'
        )

        verification_notes = request.POST.get(
            'verification_notes',
            ''
        ).strip()

        if not test_result_id:

            return render(
                request,
                'patients/add_lab_test_verification.html',
                {
                    'test_results': test_results,
                    'error': 'Please select a laboratory test result.',
                }
            )

        lab_test_result = get_object_or_404(
            LabTestResult,
            id=test_result_id
        )

        if hasattr(
            lab_test_result,
            'verification'
        ):

            return render(
                request,
                'patients/add_lab_test_verification.html',
                {
                    'test_results': test_results,
                    'error': 'This laboratory test result has already been verified.',
                }
            )

        LabTestVerification.objects.create(
            lab_test_result=lab_test_result,
            verification_status=verification_status,
            verification_notes=verification_notes,
            verified_by=request.user
            if request.user.is_authenticated
            else None
        )

        lab_test_request = lab_test_result.lab_test_request

        if verification_status == 'Verified':

            lab_test_request.status = 'Verified'

        elif verification_status == 'Rejected':

            lab_test_request.status = 'Completed'

        lab_test_request.save(
            update_fields=[
                'status',
                'updated_at'
            ]
        )

        return redirect(
            'lab_test_verification_list'
        )

    return render(
        request,
        'patients/add_lab_test_verification.html',
        {
            'test_results': test_results,
        }
    )  
def laboratory_history(request):
    history = LabTestRequest.objects.all().select_related(
        'patient',
        'consultation',
        'test_category',
        'requested_by'
    ).prefetch_related(
        'sample_collection',
        'test_processing',
        'test_result',
        'test_result__verification'
    ).order_by('-request_date')

    search = request.GET.get('search', '').strip()

    if search:
        history = history.filter(
            models.Q(patient__first_name__icontains=search)
            |
            models.Q(patient__last_name__icontains=search)
            |
            models.Q(patient__patient_number__icontains=search)
            |
            models.Q(test_name__icontains=search)
            |
            models.Q(test_category__name__icontains=search)
            |
            models.Q(status__icontains=search)
        )

    return render(
        request,
        'patients/laboratory_history.html',
        {
            'history': history,
            'search': search,
        }
    )


def laboratory_history_detail(request, test_request_id):
    test_request = get_object_or_404(
        LabTestRequest.objects.select_related(
            'patient',
            'consultation',
            'test_category',
            'requested_by'
        ).prefetch_related(
            'sample_collection',
            'test_processing',
            'test_result',
            'test_result__verification'
        ),
        id=test_request_id
    )

    return render(
        request,
        'patients/laboratory_history_detail.html',
        {
            'test_request': test_request,
        }
    ) 
def patient_report(request):
    patients = Patient.objects.all().order_by(
        'first_name',
        'last_name'
    )

    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()

    if search:
        patients = patients.filter(
            models.Q(patient_number__icontains=search)
            | models.Q(first_name__icontains=search)
            | models.Q(last_name__icontains=search)
            | models.Q(phone__icontains=search)
        )

    if status:
        patients = patients.filter(status=status)

    patient_data = []

    for patient in patients:
        patient_data.append({
            'patient': patient,
            'appointment_count': patient.appointments.count(),
            'consultation_count': patient.consultations.count(),
            'prescription_count': patient.prescriptions.count(),
            'laboratory_count': patient.lab_test_requests.count(),
        })

    return render(
        request,
        'patients/patient_report.html',
        {
            'patients': patients,
            'patient_data': patient_data,
            'search': search,
            'status': status,
        }
    )
   
def appointment_report(request):

    appointments = Appointment.objects.select_related(
        'patient',
        'doctor'
    ).order_by(
        '-appointment_date',
        '-appointment_time'
    )

    context = {
        'appointments': appointments
    }

    return render(
        request,
        'patients/appointment_report.html',
        context
    ) 
def consultation_report(request):

    consultations = Consultation.objects.select_related(
        'patient',
        'doctor'
    ).order_by(
        '-consultation_date'
    )

    context = {
        'consultations': consultations
    }

    return render(
        request,
        'patients/consultation_report.html',
        context
    )
def prescription_report(request):

    prescriptions = Prescription.objects.select_related(
        'patient',
        'doctor',
        'consultation'
    ).order_by(
        '-prescription_date'
    )

    context = {
        'prescriptions': prescriptions
    }

    return render(
        request,
        'patients/prescription_report.html',
        context
    )
def medicine_inventory_report(request):

    inventory_records = MedicineInventory.objects.select_related(
        'medicine'
    ).order_by(
        'medicine__name',
        'expiry_date'
    )

    context = {
        'inventory_records': inventory_records
    }

    return render(
        request,
        'patients/medicine_inventory_report.html',
        context
    ) 
def invoice_report(request):

    invoices = Invoice.objects.select_related(
        'patient'
    ).order_by(
        '-invoice_date',
        '-invoice_number'
    )

    context = {
        'invoices': invoices
    }

    return render(
        request,
        'patients/invoice_report.html',
        context
    )  
def payment_report(request):
    payments = PaymentRecord.objects.select_related(
        'invoice',
        'patient'
    ).order_by(
        '-payment_date'
    )

    context = {
        'payments': payments
    }

    return render(
        request,
        'patients/payment_report.html',
        context
    ) 
def laboratory_report(request):
    lab_tests = LabTestRequest.objects.select_related(
        'patient',
        'consultation',
        'test_category',
        'requested_by'
    ).prefetch_related(
        'sample_collection',
        'test_processing',
        'test_result__verification'
    ).order_by(
        '-request_date'
    )

    context = {
        'lab_tests': lab_tests
    }

    return render(
        request,
        'patients/laboratory_report.html',
        context
    )
def stock_adjustment_report(request):
    adjustments = StockAdjustment.objects.select_related(
        'inventory',
        'inventory__medicine'
    ).order_by(
        '-adjustment_date'
    )

    context = {
        'adjustments': adjustments
    }

    return render(
        request,
        'patients/stock_adjustment_report.html',
        context
    )  
def medicine_dispensing_report(request):
    dispensings = MedicineDispensing.objects.select_related(
        'patient',
        'prescription',
        'inventory',
        'inventory__medicine',
        'dispensed_by'
    ).order_by(
        '-dispensing_date'
    )

    context = {
        'dispensings': dispensings
    }

    return render(
        request,
        'patients/medicine_dispensing_report.html',
        context
    )  

def daily_monthly_yearly_report(request):

    report_type = request.GET.get(
        'report_type',
        'daily'
    ).strip()

    selected_date = request.GET.get(
        'date',
        ''
    ).strip()

    selected_month = request.GET.get(
        'month',
        ''
    ).strip()

    selected_year = request.GET.get(
        'year',
        ''
    ).strip()

    from datetime import date
    from django.utils import timezone

    today = timezone.localdate()

    # Default date
    if not selected_date:
        selected_date = today.strftime('%Y-%m-%d')

    # Default month
    if not selected_month:
        selected_month = today.strftime('%Y-%m')

    # Default year
    if not selected_year:
        selected_year = str(today.year)

    patients = Patient.objects.all()
    appointments = Appointment.objects.all()
    consultations = Consultation.objects.all()
    prescriptions = Prescription.objects.all()
    lab_tests = LabTestRequest.objects.all()
    dispensings = MedicineDispensing.objects.all()
    invoices = Invoice.objects.all()
    payments = PaymentRecord.objects.all()

    if report_type == 'daily':

        patients = patients.filter(
            registration_date=selected_date
        )

        appointments = appointments.filter(
            appointment_date=selected_date
        )

        consultations = consultations.filter(
            consultation_date=selected_date
        )

        prescriptions = prescriptions.filter(
            prescription_date=selected_date
        )

        lab_tests = lab_tests.filter(
            request_date__date=selected_date
        )

        dispensings = dispensings.filter(
            dispensing_date__date=selected_date
        )

        invoices = invoices.filter(
            invoice_date=selected_date
        )

        payments = payments.filter(
            payment_date__date=selected_date
        )

    elif report_type == 'monthly':

        try:
            year, month = selected_month.split('-')

            year = int(year)
            month = int(month)

            patients = patients.filter(
                registration_date__year=year,
                registration_date__month=month
            )

            appointments = appointments.filter(
                appointment_date__year=year,
                appointment_date__month=month
            )

            consultations = consultations.filter(
                consultation_date__year=year,
                consultation_date__month=month
            )

            prescriptions = prescriptions.filter(
                prescription_date__year=year,
                prescription_date__month=month
            )

            lab_tests = lab_tests.filter(
                request_date__year=year,
                request_date__month=month
            )

            dispensings = dispensings.filter(
                dispensing_date__year=year,
                dispensing_date__month=month
            )

            invoices = invoices.filter(
                invoice_date__year=year,
                invoice_date__month=month
            )

            payments = payments.filter(
                payment_date__year=year,
                payment_date__month=month
            )

        except (ValueError, TypeError):

            report_type = 'monthly'

    elif report_type == 'yearly':

        try:
            year = int(selected_year)

            patients = patients.filter(
                registration_date__year=year
            )

            appointments = appointments.filter(
                appointment_date__year=year
            )

            consultations = consultations.filter(
                consultation_date__year=year
            )

            prescriptions = prescriptions.filter(
                prescription_date__year=year
            )

            lab_tests = lab_tests.filter(
                request_date__year=year
            )

            dispensings = dispensings.filter(
                dispensing_date__year=year
            )

            invoices = invoices.filter(
                invoice_date__year=year
            )

            payments = payments.filter(
                payment_date__year=year
            )

        except (ValueError, TypeError):

            report_type = 'yearly'

    total_patients = patients.count()

    total_appointments = appointments.count()

    total_consultations = consultations.count()

    total_prescriptions = prescriptions.count()

    total_lab_tests = lab_tests.count()

    total_dispensings = dispensings.count()

    total_invoices = invoices.count()

    total_payments = payments.count()

    total_invoice_amount = invoices.aggregate(
        total=models.Sum('total_amount')
    )['total'] or Decimal('0.00')

    total_amount_paid = payments.aggregate(
        total=models.Sum('amount_paid')
    )['total'] or Decimal('0.00')

    total_outstanding = invoices.aggregate(
        total=models.Sum('balance')
    )['total'] or Decimal('0.00')

    context = {
        'report_type': report_type,

        'selected_date': selected_date,

        'selected_month': selected_month,

        'selected_year': selected_year,

        'total_patients': total_patients,

        'total_appointments': total_appointments,

        'total_consultations': total_consultations,

        'total_prescriptions': total_prescriptions,

        'total_lab_tests': total_lab_tests,

        'total_dispensings': total_dispensings,

        'total_invoices': total_invoices,

        'total_payments': total_payments,

        'total_invoice_amount': total_invoice_amount,

        'total_amount_paid': total_amount_paid,

        'total_outstanding': total_outstanding,

        'patients': patients,

        'appointments': appointments,

        'consultations': consultations,

        'prescriptions': prescriptions,

        'lab_tests': lab_tests,

        'dispensings': dispensings,

        'invoices': invoices,

        'payments': payments,
    }

    return render(
        request,
        'patients/daily_monthly_yearly_report.html',
        context
    )

    
def reports_dashboard(request):
    return render(
        request,
        'patients/reports_dashboard.html'
    )  
    
def administration_dashboard(request):

    users = User.objects.all().order_by(
        '-date_joined'
    )

    total_users = User.objects.count()

    active_users = User.objects.filter(
        is_active=True
    ).count()

    staff_users = User.objects.filter(
        is_staff=True
    ).count()

    superusers = User.objects.filter(
        is_superuser=True
    ).count()

    recent_users = User.objects.all().order_by(
        '-date_joined'
    )[:10]

    # User role statistics

    role_counts = {
        'Administrator': 0,
        'Doctor': 0,
        'Nurse': 0,
        'Receptionist': 0,
        'Pharmacist': 0,
        'Laboratory Technician': 0,
        'Accountant': 0,
    }

    for user in users:

        profile = UserProfile.objects.filter(
            user=user
        ).first()

        if profile:

            role = profile.role

            if role in role_counts:
                role_counts[role] += 1

    context = {
        'users': users,
        'total_users': total_users,
        'active_users': active_users,
        'staff_users': staff_users,
        'superusers': superusers,
        'recent_users': recent_users,

        'administrator_count': role_counts['Administrator'],
        'doctor_count': role_counts['Doctor'],
        'nurse_count': role_counts['Nurse'],
        'receptionist_count': role_counts['Receptionist'],
        'pharmacist_count': role_counts['Pharmacist'],
        'laboratory_technician_count': role_counts[
            'Laboratory Technician'
        ],
        'accountant_count': role_counts['Accountant'],
    }

    return render(
        request,
        'patients/administration_dashboard.html',
        context
    )

