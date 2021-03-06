import datetime
from django import forms
from django.utils.translation import gettext as _
from django.contrib import messages
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from .models import (Applicant, Organization, Application)

gender_list = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

qualification_list = (
        ('secondary_school', 'Secondary School'),
        ('diploma', 'Diploma'),
        ('bsc', 'BSc'),
        ('high_diploma', 'High Diploma'),
        ('master', 'Master'),
        ('phd', 'PhD')
    )

nationality_list = (
        ('none', 'Select your nationality'),
        ('bahraini', 'Bahraini'),
        ('non_bahraini', 'None Bahraini')
    )

status_list = (
    ('Draft'),
    ('Submitted'),
    ('Verification'),       # add first formula         L1 emp
    ('Request Statements'), # add second formula        L2 emp
    ('Request Manager Approval/Reject'), #              L3 emp
    ('Initial Approval Completed'),
)

final_approval_status_list = (
    ('Draft'),
    ('Submitted'),
    ('Verification'),       # add first formula         L1 emp
    ('Request Statements'), # add second formula        L2 emp
    ('Payment Fees'),
    ('Request Manager Approval/Reject'),#               L3 emp
    ('Final Approval Completed'),
)

renew_license_status_list = (
    ('Draft'),
    ('Submitted'),
    ('Verification'),       # add first formula         L1 emp
    ('Request Statements'), # add second formula        L2 emp
    ('Payment Fees'),
    ('Request Manager Approval/Reject'),#               L3 emp
    ('Renewal License Completed'),
)

cancel_license_status_list = (
    ('Draft'),
    ('Submitted'),
    ('Verification'),       # add first formula         L1 emp
    ('Request Statements'), # add second formula        L2 emp
    ('Request Manager Approval/Reject'),#               L3 emp
    ('Cancel license Completed'),
)

class ApplicantForm(forms.ModelForm):

    user_id = forms.ModelChoiceField(User.objects.all())

    class Meta:
        model = Applicant
        fields = (
            'cpr',
            'cpr_expiry_date',
            'fullname',
            'gender',
            'nationality',
            'qualification',
            'occupcation',
            'flat_no',
            'building_no',
            'road_no',
            'area',
            'contact1',
            'contact2',
            'email',
            'user_id',
            'passport_expiry_date',
            # File Fields
            'cpr_doc',
            'passport_doc',
            'behavior_cert_doc',
            'bank_statement_doc'
        )


    def clean(self):
        cleaned_data = super().clean()
        cpr_expiry_date = cleaned_data.get("cpr_expiry_date")
        passport_expiry_date = cleaned_data.get("passport_expiry_date")

        if cpr_expiry_date <= datetime.datetime.now().date():
            self.add_error('cpr_expiry_date', "Please renew your CPR ")

        if passport_expiry_date <= datetime.datetime.now().date():
            self.add_error('passport_expiry_date', "Please renew your Passport")

        # form.instance.user_id = self.request.user
        # return super(ApplicantForm, self).form_valid(form)

class OrganizationForm(forms.ModelForm):
    user_id = forms.ModelChoiceField(User.objects.all())
    applicant_id = forms.ModelChoiceField(Applicant.objects.all())

    class Meta:
        model = Organization
        fields = (
            'cr',
            'cr_reg_date',
            'full_en_name',
            'license_no',
            'flat_no',
            'building_no',
            'road_no',
            'area',
            'contact1',
            'contact2',
            'email',
            'applicant_id',
            'user_id'
        )

class ApplicationForm(forms.ModelForm):
    user_id = forms.ModelChoiceField(User.objects.all())
    applicant_id = forms.ModelChoiceField(Applicant.objects.all())

    class Meta:
        model = Application
        fields = (
            'app_no',
            'app_date',
            'app_type',
            'app_status_index',
            'app_current_status',
            'app_next_status',
            'activty_type',
            'financial_guarantee',
            'financial_guarantee_expiry_date',
            # Company Details ---- Start
            'cr',
            'cr_reg_date',
            'full_en_name',
            'license_no',
            'license_expiry_date',
            'flat_no',
            'building_no',
            'road_no',
            'area',
            'contact1',
            'contact2',
            'email',
            # Company Details ---- End
            # Female Accommodation ---- Start
            'fh_flat_no',
            'fh_building_no',
            'fh_road_no',
            'fh_area',
            'fh_contact1',
            'fh_contact2',
            # Female Accommodation ---- End
            'staff_comments',
            'manager_comments',
            'approval',
            'qsreq',
            'qnreq',
            'dreq',

            'qsrec',
            'qnrec',
            'drec',

            'user_id',
            'applicant_id',
            'cr_doc',
            'bank_statement_doc',
            'lmra_agreement',
            'cert1_doc',
            'cert2_doc',
            'cert3_doc',
            'cr_rent_doc',
            'fh_rent_doc',
            'cr_ewa_bill_doc',
            'fh_ewa_bill_doc',
            'employment_office_receipt'
        )

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['app_status_index'].widget = forms.HiddenInput()
        self.fields['app_next_status'].widget = forms.HiddenInput()

        if not self.instance.id:
            self.fields['staff_comments'].widget = forms.HiddenInput()
            self.fields['manager_comments'].widget = forms.HiddenInput()
            self.fields['approval'].widget = forms.HiddenInput()
            self.fields['financial_guarantee'].widget = forms.HiddenInput()
            self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
            self.fields['qsreq'].widget = forms.HiddenInput()
            self.fields['qnreq'].widget = forms.HiddenInput()
            self.fields['dreq'].widget = forms.HiddenInput()
            self.fields['qsrec'].widget = forms.HiddenInput()
            self.fields['qnrec'].widget = forms.HiddenInput()
            self.fields['drec'].widget = forms.HiddenInput()

        if self.instance.app_type == 'initial':
            self.fields['cr'].widget = forms.HiddenInput()
            self.fields['cr_reg_date'].widget = forms.HiddenInput()
            self.fields['full_en_name'].widget = forms.HiddenInput()
            self.fields['license_no'].widget = forms.HiddenInput()
            self.fields['license_expiry_date'].widget = forms.HiddenInput()
            self.fields['flat_no'].widget = forms.HiddenInput()
            self.fields['building_no'].widget = forms.HiddenInput()
            self.fields['road_no'].widget = forms.HiddenInput()
            self.fields['area'].widget = forms.HiddenInput()
            self.fields['contact1'].widget = forms.HiddenInput()
            self.fields['contact2'].widget = forms.HiddenInput()
            self.fields['fh_flat_no'].widget = forms.HiddenInput()
            self.fields['fh_building_no'].widget = forms.HiddenInput()
            self.fields['fh_road_no'].widget = forms.HiddenInput()
            self.fields['fh_area'].widget = forms.HiddenInput()
            self.fields['fh_contact1'].widget = forms.HiddenInput()
            self.fields['fh_contact2'].widget = forms.HiddenInput()

            self.fields['cr_doc'].widget = forms.HiddenInput()
            self.fields['bank_statement_doc'].widget = forms.HiddenInput()
            self.fields['lmra_agreement'].widget = forms.HiddenInput()
            self.fields['cert1_doc'].widget = forms.HiddenInput()
            self.fields['cert2_doc'].widget = forms.HiddenInput()
            self.fields['cert3_doc'].widget = forms.HiddenInput()
            self.fields['cr_rent_doc'].widget = forms.HiddenInput()
            self.fields['fh_rent_doc'].widget = forms.HiddenInput()
            self.fields['cr_ewa_bill_doc'].widget = forms.HiddenInput()
            self.fields['fh_ewa_bill_doc'].widget = forms.HiddenInput()
            self.fields['employment_office_receipt'].widget = forms.HiddenInput()

            #open for update an exist record(instance)
            if self.instance.id:
                if self.instance.app_current_status == 'Draft':
                    self.fields['staff_comments'].widget = forms.HiddenInput()
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                    self.fields['qsreq'].widget = forms.HiddenInput()
                    self.fields['qnreq'].widget = forms.HiddenInput()
                    self.fields['dreq'].widget = forms.HiddenInput()
                    self.fields['qsrec'].widget = forms.HiddenInput()
                    self.fields['qnrec'].widget = forms.HiddenInput()
                    self.fields['drec'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Submitted':
                    self.fields['staff_comments'].widget = forms.HiddenInput()
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                    self.fields['qsreq'].widget = forms.HiddenInput()
                    self.fields['qnreq'].widget = forms.HiddenInput()
                    self.fields['dreq'].widget = forms.HiddenInput()
                    self.fields['qsrec'].widget = forms.HiddenInput()
                    self.fields['qnrec'].widget = forms.HiddenInput()
                    self.fields['drec'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Application Code':
                    self.fields['staff_comments'].widget = forms.HiddenInput()
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                    self.fields['qsreq'].widget = forms.HiddenInput()
                    self.fields['qnreq'].widget = forms.HiddenInput()
                    self.fields['dreq'].widget = forms.HiddenInput()
                    self.fields['qsrec'].widget = forms.HiddenInput()
                    self.fields['qnrec'].widget = forms.HiddenInput()
                    self.fields['drec'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Violations Verification':
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                    self.fields['qsreq'].widget = forms.HiddenInput()
                    self.fields['qnreq'].widget = forms.HiddenInput()
                    self.fields['dreq'].widget = forms.HiddenInput()
                    self.fields['qsrec'].widget = forms.HiddenInput()
                    self.fields['qnrec'].widget = forms.HiddenInput()
                    self.fields['drec'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Request Statements':
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Review Documents':
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Request Manager Approval/Reject':
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()

            #open new form for entering new date -- no instance exist
            elif self.fields['app_current_status'].initial == 'Draft':
                self.fields['qsreq'].widget = forms.HiddenInput()
                self.fields['qnreq'].widget = forms.HiddenInput()
                self.fields['dreq'].widget = forms.HiddenInput()
                self.fields['qsrec'].widget = forms.HiddenInput()
                self.fields['qnrec'].widget = forms.HiddenInput()
                self.fields['drec'].widget = forms.HiddenInput()
                self.fields['staff_comments'].widget = forms.HiddenInput()
                self.fields['manager_comments'].widget = forms.HiddenInput()
                self.fields['approval'].widget = forms.HiddenInput()
                self.fields['financial_guarantee'].widget = forms.HiddenInput()
                self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()

        elif self.instance.app_type == 'final':
            #open for update an exist record(instance)
            if self.instance.id:
                if self.instance.app_current_status == 'Draft':
                    self.fields['staff_comments'].widget = forms.HiddenInput()
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                    self.fields['qsreq'].widget = forms.HiddenInput()
                    self.fields['qnreq'].widget = forms.HiddenInput()
                    self.fields['dreq'].widget = forms.HiddenInput()
                    self.fields['qsrec'].widget = forms.HiddenInput()
                    self.fields['qnrec'].widget = forms.HiddenInput()
                    self.fields['drec'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Submitted':
                    self.fields['staff_comments'].widget = forms.HiddenInput()
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                    self.fields['qsreq'].widget = forms.HiddenInput()
                    self.fields['qnreq'].widget = forms.HiddenInput()
                    self.fields['dreq'].widget = forms.HiddenInput()
                    self.fields['qsrec'].widget = forms.HiddenInput()
                    self.fields['qnrec'].widget = forms.HiddenInput()
                    self.fields['drec'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Application Code':
                    self.fields['staff_comments'].widget = forms.HiddenInput()
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                    self.fields['qsreq'].widget = forms.HiddenInput()
                    self.fields['qnreq'].widget = forms.HiddenInput()
                    self.fields['dreq'].widget = forms.HiddenInput()
                    self.fields['qsrec'].widget = forms.HiddenInput()
                    self.fields['qnrec'].widget = forms.HiddenInput()
                    self.fields['drec'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Violations Verification':
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                    self.fields['qsreq'].widget = forms.HiddenInput()
                    self.fields['qnreq'].widget = forms.HiddenInput()
                    self.fields['dreq'].widget = forms.HiddenInput()
                    self.fields['qsrec'].widget = forms.HiddenInput()
                    self.fields['qnrec'].widget = forms.HiddenInput()
                    self.fields['drec'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Request Statements':
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Review Documents':
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Request Manager Approval/Reject':
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()

            #open new form for entering new date -- no instance exist
            elif self.fields['app_current_status'].initial == 'Draft':
                self.fields['qsreq'].widget = forms.HiddenInput()
                self.fields['qnreq'].widget = forms.HiddenInput()
                self.fields['dreq'].widget = forms.HiddenInput()
                self.fields['qsrec'].widget = forms.HiddenInput()
                self.fields['qnrec'].widget = forms.HiddenInput()
                self.fields['drec'].widget = forms.HiddenInput()
                self.fields['staff_comments'].widget = forms.HiddenInput()
                self.fields['manager_comments'].widget = forms.HiddenInput()
                self.fields['approval'].widget = forms.HiddenInput()
                self.fields['financial_guarantee'].widget = forms.HiddenInput()
                self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()

        elif self.instance.app_type == 'renew':
            #open for update an exist record(instance)
            if self.instance.id:
                if self.instance.app_current_status == 'Draft':
                    self.fields['staff_comments'].widget = forms.HiddenInput()
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                    self.fields['qsreq'].widget = forms.HiddenInput()
                    self.fields['qnreq'].widget = forms.HiddenInput()
                    self.fields['dreq'].widget = forms.HiddenInput()
                    self.fields['qsrec'].widget = forms.HiddenInput()
                    self.fields['qnrec'].widget = forms.HiddenInput()
                    self.fields['drec'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Submitted':
                    # self.fields['staff_comments'].widget = forms.HiddenInput()
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                    self.fields['qsreq'].widget = forms.HiddenInput()
                    self.fields['qnreq'].widget = forms.HiddenInput()
                    self.fields['dreq'].widget = forms.HiddenInput()
                    self.fields['qsrec'].widget = forms.HiddenInput()
                    self.fields['qnrec'].widget = forms.HiddenInput()
                    self.fields['drec'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Application Code':
                    # self.fields['staff_comments'].widget = forms.HiddenInput()
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                    self.fields['qsreq'].widget = forms.HiddenInput()
                    self.fields['qnreq'].widget = forms.HiddenInput()
                    self.fields['dreq'].widget = forms.HiddenInput()
                    self.fields['qsrec'].widget = forms.HiddenInput()
                    self.fields['qnrec'].widget = forms.HiddenInput()
                    self.fields['drec'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Verify Document':
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()

                    self.fields['qsrec'].widget = forms.HiddenInput()
                    self.fields['qnrec'].widget = forms.HiddenInput()
                    self.fields['drec'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Verify Requirements':
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                # elif self.instance.app_current_status == 'Review Documents':
                #     self.fields['manager_comments'].widget = forms.HiddenInput()
                #     self.fields['approval'].widget = forms.HiddenInput()
                #     self.fields['financial_guarantee'].widget = forms.HiddenInput()
                #     self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                # elif self.instance.app_current_status == 'Request Manager Approval/Reject':
                #     self.fields['financial_guarantee'].widget = forms.HiddenInput()
                #     self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()

            #open new form for entering new date -- no instance exist
            elif self.fields['app_current_status'].initial == 'Draft':
                self.fields['qsreq'].widget = forms.HiddenInput()
                self.fields['qnreq'].widget = forms.HiddenInput()
                self.fields['dreq'].widget = forms.HiddenInput()
                self.fields['qsrec'].widget = forms.HiddenInput()
                self.fields['qnrec'].widget = forms.HiddenInput()
                self.fields['drec'].widget = forms.HiddenInput()
                self.fields['staff_comments'].widget = forms.HiddenInput()
                self.fields['manager_comments'].widget = forms.HiddenInput()
                self.fields['approval'].widget = forms.HiddenInput()
                self.fields['financial_guarantee'].widget = forms.HiddenInput()
                self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()

        elif self.instance.app_type == 'cancel':
            #open for update an exist record(instance)
            if self.instance.id:
                if self.instance.app_current_status == 'Draft':
                    self.fields['staff_comments'].widget = forms.HiddenInput()
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                    self.fields['qsreq'].widget = forms.HiddenInput()
                    self.fields['qnreq'].widget = forms.HiddenInput()
                    self.fields['dreq'].widget = forms.HiddenInput()
                    self.fields['qsrec'].widget = forms.HiddenInput()
                    self.fields['qnrec'].widget = forms.HiddenInput()
                    self.fields['drec'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Submitted':
                    self.fields['staff_comments'].widget = forms.HiddenInput()
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                    self.fields['qsreq'].widget = forms.HiddenInput()
                    self.fields['qnreq'].widget = forms.HiddenInput()
                    self.fields['dreq'].widget = forms.HiddenInput()
                    self.fields['qsrec'].widget = forms.HiddenInput()
                    self.fields['qnrec'].widget = forms.HiddenInput()
                    self.fields['drec'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Application Code':
                    self.fields['staff_comments'].widget = forms.HiddenInput()
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                    self.fields['qsreq'].widget = forms.HiddenInput()
                    self.fields['qnreq'].widget = forms.HiddenInput()
                    self.fields['dreq'].widget = forms.HiddenInput()
                    self.fields['qsrec'].widget = forms.HiddenInput()
                    self.fields['qnrec'].widget = forms.HiddenInput()
                    self.fields['drec'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Violations Verification':
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                    self.fields['qsreq'].widget = forms.HiddenInput()
                    self.fields['qnreq'].widget = forms.HiddenInput()
                    self.fields['dreq'].widget = forms.HiddenInput()
                    self.fields['qsrec'].widget = forms.HiddenInput()
                    self.fields['qnrec'].widget = forms.HiddenInput()
                    self.fields['drec'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Request Statements':
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Review Documents':
                    self.fields['manager_comments'].widget = forms.HiddenInput()
                    self.fields['approval'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()
                elif self.instance.app_current_status == 'Request Manager Approval/Reject':
                    self.fields['financial_guarantee'].widget = forms.HiddenInput()
                    self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()

            #open new form for entering new date -- no instance exist
            elif self.fields['app_current_status'].initial == 'Draft':
                self.fields['qsreq'].widget = forms.HiddenInput()
                self.fields['qnreq'].widget = forms.HiddenInput()
                self.fields['dreq'].widget = forms.HiddenInput()
                self.fields['qsrec'].widget = forms.HiddenInput()
                self.fields['qnrec'].widget = forms.HiddenInput()
                self.fields['drec'].widget = forms.HiddenInput()
                self.fields['staff_comments'].widget = forms.HiddenInput()
                self.fields['manager_comments'].widget = forms.HiddenInput()
                self.fields['approval'].widget = forms.HiddenInput()
                self.fields['financial_guarantee'].widget = forms.HiddenInput()
                self.fields['financial_guarantee_expiry_date'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        applicant_id = cleaned_data.get("applicant_id")

        if applicant_id.has_application:
            # messages.warning(self.request, _('This applicant either received the license or has an application on going'))
            self.add_error('applicant_id', "Application Exist")

        qsreq = cleaned_data.get("qsreq")
        qnreq = cleaned_data.get("qnreq")

        qsrec = cleaned_data.get("qsrec")
        qnrec = cleaned_data.get("qnrec")

        if qnreq <= 0:
            self.add_error('qnreq','Value should be more than 0')

        if qnrec <= 0:
            self.add_error('qnrec','Value should be more than 0')

        if qnreq < qsreq:
            self.add_error('qnreq', 'Value should equal or greater than the Uploaded Docuements')

        if qnrec < qsrec:
            self.add_error('qnrec', 'Value should equal or greater than the Satisfying Recommendations')

    def save(self, *args, **kwargs):
        if self.instance.app_type == 'initial':

            if self.instance.id:  # if true then this is update form
                if self.instance.app_status_index < 7:
                    self.instance.app_current_status = status_list[self.instance.app_status_index]
                    self.instance.app_next_status = status_list[self.instance.app_status_index+1]
                    self.instance.app_status_index = self.instance.app_status_index +1

                if self.instance.app_current_status == 'Submitted':
                    self.instance.qsreq = 4
                    self.instance.qsrec = 4
                if self.instance.app_current_status == 'Application Code':
                    self.instance.app_no = "APP/" + str(datetime.datetime.now().year) + "/" + "{:02d}".format(datetime.datetime.now().month) + "/" + "{:04d}".format(self.instance.id)
                if self.instance.app_current_status == 'Request Statements':
                    self.instance.dreq = round(self.instance.qsreq / self.instance.qnreq * 100, 2)
                    self.instance.drec = round(self.instance.qsrec / self.instance.qnrec * 100, 2)
            else:
                self.instance.app_status_index = 0
                self.instance.app_current_status = status_list[self.instance.app_status_index]
                self.instance.app_next_status = status_list[self.instance.app_status_index+1]

        elif self.instance.app_type == 'final':
            if self.instance.id:  # if true then this is update form
                if self.instance.app_status_index <= 8:
                    self.instance.app_current_status = final_approval_status_list[self.instance.app_status_index]
                    if self.instance.app_status_index < 8:
                        self.instance.app_next_status = final_approval_status_list[self.instance.app_status_index+1]
                        self.instance.app_status_index = self.instance.app_status_index +1
                    else:
                        self.instance.app_next_status = final_approval_status_list[self.instance.app_status_index]
                        self.instance.app_status_index = self.instance.app_status_index

                if self.instance.app_current_status == 'Submitted':
                    self.instance.qsreq = 0
                    self.instance.qsrec = 0
                if self.instance.app_current_status == 'Application Code':
                    self.instance.app_no = "APP/" + str(datetime.datetime.now().year) + "/" + "{:02d}".format(datetime.datetime.now().month) + "/" + "{:04d}".format(self.instance.id)
                if self.instance.app_current_status == 'Request Statements':
                    self.instance.dreq = round(self.instance.qsreq / self.instance.qnreq * 100, 2)
                    self.instance.drec = round(self.instance.qsrec / self.instance.qnrec * 100, 2)
            else:
                self.instance.app_status_index = 0
                self.instance.app_current_status = final_approval_status_list[self.instance.app_status_index]
                self.instance.app_next_status = final_approval_status_list[self.instance.app_status_index+1]

        elif self.instance.app_type == 'renew':
            if self.instance.id:  # if true then this is update form
                if self.instance.app_status_index <= 8:
                    self.instance.app_current_status = final_approval_status_list[self.instance.app_status_index]
                    if self.instance.app_status_index < 8:
                        self.instance.app_next_status = final_approval_status_list[self.instance.app_status_index+1]
                        self.instance.app_status_index = self.instance.app_status_index +1
                    else:
                        self.instance.app_next_status = final_approval_status_list[self.instance.app_status_index]
                        self.instance.app_status_index = self.instance.app_status_index

                if self.instance.app_current_status == 'Submitted':
                    self.instance.qsreq = 0
                    self.instance.qsrec = 0
                if self.instance.app_current_status == 'Application Code':
                    self.instance.app_no = "APP/" + str(datetime.datetime.now().year) + "/" + "{:02d}".format(datetime.datetime.now().month) + "/" + "{:04d}".format(self.instance.id)
                if self.instance.app_current_status == 'Request Statements':
                    self.instance.dreq = round(self.instance.qsreq / self.instance.qnreq * 100, 2)
                    self.instance.drec = round(self.instance.qsrec / self.instance.qnrec * 100, 2)
            else:
                self.instance.app_status_index = 0
                self.instance.app_current_status = final_approval_status_list[self.instance.app_status_index]
                self.instance.app_next_status = final_approval_status_list[self.instance.app_status_index+1]

        elif self.instance.app_type == 'cancel':
            if self.instance.id:  # if true then this is update form
                if self.instance.app_status_index < 7:
                    self.instance.app_current_status = final_approval_status_list[self.instance.app_status_index]
                    self.instance.app_next_status = final_approval_status_list[self.instance.app_status_index+1]
                    self.instance.app_status_index = self.instance.app_status_index +1

                if self.instance.app_current_status == 'Submitted':
                    self.instance.qsreq = 4
                    self.instance.qsrec = 4
                if self.instance.app_current_status == 'Application Code':
                    self.instance.app_no = "APP/" + str(datetime.datetime.now().year) + "/" + "{:02d}".format(datetime.datetime.now().month) + "/" + "{:04d}".format(self.instance.id)
                if self.instance.app_current_status == 'Request Statements':
                    self.instance.dreq = round(self.instance.qsreq / self.instance.qnreq * 100, 2)
                    self.instance.drec = round(self.instance.qsrec / self.instance.qnrec * 100, 2)
            else:
                self.instance.app_status_index = 0
                self.instance.app_current_status = final_approval_status_list[self.instance.app_status_index]
                self.instance.app_next_status = final_approval_status_list[self.instance.app_status_index+1]

        super().save(*args, **kwargs)