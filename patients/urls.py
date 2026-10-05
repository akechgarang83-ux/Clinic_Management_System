from django.urls import path

from .views import (
    patient_list,
    register_patient,
    patient_detail,
    edit_patient,
    delete_patient,
    add_medical_record,
    book_appointment,
    appointment_list,
    appointment_calendar,
    reschedule_appointment,
    cancel_appointment,
    doctor_availability,
    add_doctor_availability,
    add_consultation,
    consultation_list,
    prescription_list,
    add_prescription,
    medicine_list,
    add_medicine,
    medicine_category_list,
    add_medicine_category,
    medicine_inventory_list,
    add_medicine_inventory,
    stock_adjustment_list,
    add_stock_adjustment,
    medicine_dispensing_list,
    add_medicine_dispensing,
    low_stock_alert,
    prescription_history,
    invoice_list,
    add_invoice,
    consultation_fee_list,
    add_consultation_fee,
    medicine_charge_list,
    add_medicine_charge,
    payment_record_list,
    add_payment_record,
    delete_payment_record,
    payment_receipt,
    outstanding_balance,
    lab_test_request_list,
    add_lab_test_request,
    lab_test_category_list,
    add_lab_test_category,
    lab_sample_collection_list,
    add_lab_sample_collection,
    lab_test_processing_list,
    add_lab_test_processing,
    lab_test_result_list,
    add_lab_test_result,
    lab_test_verification_list,
    add_lab_test_verification,
    laboratory_history,
    laboratory_history_detail,
    patient_report,
    appointment_report,
    consultation_report,
    prescription_report,
    medicine_inventory_report,
    invoice_report,
    payment_report,
    laboratory_report,
    stock_adjustment_report,
    medicine_dispensing_report,
    reports_dashboard,
    administration_dashboard,
    patient_management,
    select_patient_for_prescription,
    daily_monthly_yearly_report,
)


urlpatterns = [

    # ============================================================
    # PATIENT MANAGEMENT
    # ============================================================

    path(
        '',
        patient_list,
        name='patient_list'
    ),
    path(
    'patients/',
    patient_management,
    name='patient_management'
),

    path(
        'register/',
        register_patient,
        name='register_patient'
    ),

    path(
        '<int:patient_id>/',
        patient_detail,
        name='patient_detail'
    ),

    path(
        '<int:patient_id>/edit/',
        edit_patient,
        name='edit_patient'
    ),

    path(
        '<int:patient_id>/delete/',
        delete_patient,
        name='delete_patient'
    ),

    path(
        '<int:patient_id>/medical-record/add/',
        add_medical_record,
        name='add_medical_record'
    ),


    # ============================================================
    # APPOINTMENT MANAGEMENT
    # ============================================================

    path(
        '<int:patient_id>/appointment/book/',
        book_appointment,
        name='book_appointment'
    ),

    path(
        'appointments/',
        appointment_list,
        name='appointment_list'
    ),

    path(
        'appointments/calendar/',
        appointment_calendar,
        name='appointment_calendar'
    ),

    path(
        'appointments/<int:appointment_id>/reschedule/',
        reschedule_appointment,
        name='reschedule_appointment'
    ),

    path(
        'appointments/<int:appointment_id>/cancel/',
        cancel_appointment,
        name='cancel_appointment'
    ),

    path(
        'appointments/doctor-availability/',
        doctor_availability,
        name='doctor_availability'
    ),

    path(
        'appointments/doctor-availability/add/',
        add_doctor_availability,
        name='add_doctor_availability'
    ),


    # ============================================================
    # CONSULTATION & DIAGNOSIS
    # ============================================================

    path(
        '<int:patient_id>/consultation/add/',
        add_consultation,
        name='add_consultation'
    ),
    path(
    'consultations/',
    consultation_list,
    name='consultation_list'
),


    # ============================================================
    # PRESCRIPTION MANAGEMENT
    # ============================================================

    path( 'prescriptions/', prescription_list, 
        name='prescription_list' ), 
    path( 'prescription-history/', prescription_history, name='prescription_history' ), 
    
    # SELECT PATIENT BEFORE ADDING PRESCRIPTION 
    path( 'prescriptions/select-patient/', select_patient_for_prescription, name='select_patient_for_prescription' ), 
    
    # ADD PRESCRIPTION FOR SELECTED PATIENT 
    path( '<int:patient_id>/prescriptions/add/', add_prescription, name='add_prescription' ),


    # ============================================================
    # MEDICINE MANAGEMENT
    # ============================================================

    path(
        'medicines/',
        medicine_list,
        name='medicine_list'
    ),

    path(
        'medicines/add/',
        add_medicine,
        name='add_medicine'
    ),

    path(
        'medicine-categories/',
        medicine_category_list,
        name='medicine_category_list'
    ),

    path(
        'medicine-categories/add/',
        add_medicine_category,
        name='add_medicine_category'
    ),


    # ============================================================
    # MEDICINE INVENTORY
    # ============================================================

    path(
        'medicine-inventory/',
        medicine_inventory_list,
        name='medicine_inventory_list'
    ),

    path(
        'medicine-inventory/add/',
        add_medicine_inventory,
        name='add_medicine_inventory'
    ),

    path(
        'stock-adjustments/',
        stock_adjustment_list,
        name='stock_adjustment_list'
    ),

    path(
        'stock-adjustments/add/',
        add_stock_adjustment,
        name='add_stock_adjustment'
    ),

    path(
        'medicine-dispensings/',
        medicine_dispensing_list,
        name='medicine_dispensing_list'
    ),

    path(
        'medicine-dispensings/add/',
        add_medicine_dispensing,
        name='add_medicine_dispensing'
    ),

    path(
        'low-stock-alert/',
        low_stock_alert,
        name='low_stock_alert'
    ),


    # ============================================================
    # BILLING & PAYMENT
    # ============================================================

    path(
        'invoices/',
        invoice_list,
        name='invoice_list'
    ),

    path(
        'invoices/add/',
        add_invoice,
        name='add_invoice'
    ),

    path(
        'consultation-fees/',
        consultation_fee_list,
        name='consultation_fee_list'
    ),

    path(
        'consultation-fees/add/',
        add_consultation_fee,
        name='add_consultation_fee'
    ),

    path(
        'medicine-charges/',
        medicine_charge_list,
        name='medicine_charge_list'
    ),

    path(
        'medicine-charges/add/',
        add_medicine_charge,
        name='add_medicine_charge'
    ),

    path(
        'payment-records/',
        payment_record_list,
        name='payment_record_list'
    ),

    path(
        'payment-records/add/',
        add_payment_record,
        name='add_payment_record'
    ),

    path(
        'payment-records/<int:payment_id>/delete/',
        delete_payment_record,
        name='delete_payment_record'
    ),

    path(
        'payment-records/<int:payment_id>/receipt/',
        payment_receipt,
        name='payment_receipt'
    ),

    path(
        'outstanding-balances/',
        outstanding_balance,
        name='outstanding_balance'
    ),


    # ============================================================
    # LABORATORY
    # ============================================================

    path(
        'laboratory/test-requests/',
        lab_test_request_list,
        name='lab_test_request_list'
    ),

    path(
        'laboratory/test-requests/add/',
        add_lab_test_request,
        name='add_lab_test_request'
    ),

    path(
        'laboratory/test-categories/',
        lab_test_category_list,
        name='lab_test_category_list'
    ),

    path(
        'laboratory/test-categories/add/',
        add_lab_test_category,
        name='add_lab_test_category'
    ),

    path(
        'laboratory/sample-collections/',
        lab_sample_collection_list,
        name='lab_sample_collection_list'
    ),

    path(
        'laboratory/sample-collections/add/',
        add_lab_sample_collection,
        name='add_lab_sample_collection'
    ),

    path(
        'laboratory/test-processing/',
        lab_test_processing_list,
        name='lab_test_processing_list'
    ),

    path(
        'laboratory/test-processing/add/',
        add_lab_test_processing,
        name='add_lab_test_processing'
    ),

    path(
        'laboratory/test-results/',
        lab_test_result_list,
        name='lab_test_result_list'
    ),

    path(
        'laboratory/test-results/add/',
        add_lab_test_result,
        name='add_lab_test_result'
    ),

    path(
        'laboratory/test-verification/',
        lab_test_verification_list,
        name='lab_test_verification_list'
    ),

    path(
        'laboratory/test-verification/add/',
        add_lab_test_verification,
        name='add_lab_test_verification'
    ),

    path(
        'laboratory/history/',
        laboratory_history,
        name='laboratory_history'
    ),

    path(
        'laboratory/history/<int:test_request_id>/',
        laboratory_history_detail,
        name='laboratory_history_detail'
    ),


    # ============================================================
    # REPORTS
    # ============================================================

    path(
        'reports/patients/',
        patient_report,
        name='patient_report'
    ),

    path(
        'reports/appointments/',
        appointment_report,
        name='appointment_report'
    ),

    path(
        'reports/consultations/',
        consultation_report,
        name='consultation_report'
    ),

    path(
        'reports/prescriptions/',
        prescription_report,
        name='prescription_report'
    ),

    path(
        'reports/medicine-inventory/',
        medicine_inventory_report,
        name='medicine_inventory_report'
    ),

    path(
        'reports/invoices/',
        invoice_report,
        name='invoice_report'
    ),

    path(
        'reports/payments/',
        payment_report,
        name='payment_report'
    ),

    path(
        'reports/laboratory/',
        laboratory_report,
        name='laboratory_report'
    ),

    path(
        'reports/stock-adjustments/',
        stock_adjustment_report,
        name='stock_adjustment_report'
    ),

    path(
        'reports/medicine-dispensings/',
        medicine_dispensing_report,
        name='medicine_dispensing_report'
    ),

    path(
        'reports/',
        reports_dashboard,
        name='reports_dashboard'
    ),


    # ============================================================
    # ADMINISTRATION
    # ============================================================

    path(
        'administration/',
        administration_dashboard,
        name='administration_dashboard'
    ),
    
    path(
    'reports/daily-monthly-yearly/',
    daily_monthly_yearly_report,
    name='daily_monthly_yearly_report'
),
]