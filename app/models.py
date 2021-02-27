from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

class Applicant(models.Model):

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
        ('phd', 'PhD'),
    )

    nationality_list = (
        ('none', 'Select your nationality'),
        ('bahraini', 'Bahraini'),
        ('non_bahraini', 'None Bahraini')
    )

    cpr = models.CharField(_("CPR No"), max_length=9)
    cpr_expiry_date = models.DateField(_("CPR Expire Date"), auto_now=False, auto_now_add=False)
    passport_expiry_date = models.DateField(_("Passport Expire Date"), auto_now=False, auto_now_add=False)
    fullname = models.CharField(_("Full Name"), max_length=100)
    nationality =  models.CharField(_("Nationality"), max_length=50, choices=nationality_list, default='none')
    gender = models.CharField(_("Gender"), max_length=10, choices=gender_list)
    qualification = models.CharField(_("Qualification"), max_length=50, choices=qualification_list)
    occupcation = models.CharField(_("Occupation"), max_length=50)
    has_application = models.BooleanField(_("Has Applicatino on process"), default=False)

    # Address fields
    flat_no = models.IntegerField(_("Flat No"), default=0)
    building_no = models.IntegerField(_("Building No"), default=0)
    road_no = models.IntegerField(_("Road No"), default=0)
    area = models.CharField(_("Area"), max_length=50, blank=True)
    contact1 = models.CharField(_("Phone"), max_length=50, blank=True)
    contact2 = models.CharField(_("Mobile"), max_length=50, blank=True)
    email = models.EmailField(_("Email"), max_length=254, blank=True)
    user_id = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)

    # Applicant Uploaded Doc fields
    cpr_doc = models.FileField(_("CPR Doc"), upload_to='doc_library', max_length=100)
    passport_doc = models.FileField(_("Passport Doc"), upload_to='doc_library', max_length=100)
    behavior_cert_doc = models.FileField(_("Behavior Certificate Doc"), upload_to='doc_library', max_length=100)

    # Applicant Bank Related Fields
    bank_statement_doc = models.FileField(_("Bank Statement Doc"), upload_to='doc_library', max_length=100)
    is_10000_exist = models.BooleanField(_("Is 10000 BD exist in Applicant Bank Statement"), default=False)

    # class Meta:
    #     verbose_name = _("Applicant")
    #     verbose_name_plural = _("Applicants")

    def __str__(self):
        return self.fullname

    # def get_absolute_url(self):
    #     return reverse("applicant-list") #, kwargs={"pk": self.pk})

    # def get_success_url(self):
    #     return reverse('applicant-list') #, args=(somethinguseful,))
    # def form_valid(self, form):
    #     print("====================================================================== 000000")
    #     if form.instance.cpr_expiry_date <= datetime.datetime.now().date():
    #         messages.warning(self.request, f'Please renew your CPR')
    #         return super(ApplicantForm, self).form_invalid(form)

    #     if form.instance.passport_expiry_date <= datetime.datetime.now().date():
    #         messages.warning(self.request, f'Please renew your Passport')
    #         return super(ApplicantForm, self).form_invalid(form)

    #     form.instance.user_id = self.request.user
    #     return super(ApplicantForm, self).form_valid(form)

class Organization(models.Model):

    cr = models.CharField(_("CR No"), max_length=50, blank=True)
    cr_reg_date = models.DateField(_("Registration Date"), auto_now=False, auto_now_add=False)
    full_en_name = models.CharField(_("Commercial Eng Name"), max_length=250, blank=True)
    license_no = models.CharField(_("License No"), max_length=50, blank=True)
    flat_no = models.IntegerField(_("Flat No"), default=0)
    building_no = models.IntegerField(_("Building No"), default=0)
    road_no = models.IntegerField(_("Road No"), default=0)
    area = models.CharField(_("Area"), max_length=50, blank=True)
    contact1 = models.CharField(_("Phone"), max_length=50, blank=True)
    contact2 = models.CharField(_("Fax"), max_length=50, blank=True)
    email = models.EmailField(_("Email"), max_length=254, blank=True)
    applicant_id = models.ForeignKey(Applicant, verbose_name=_(""), on_delete=models.CASCADE, blank=True)
    user_id = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE, blank=True)

    # cr_doc = models.FileField(_("CR Doc"), upload_to='doc_library', max_length=100)
    # bank_statement_doc = models.FileField(_("Bank Statement Doc"), upload_to='doc_library', max_length=100)
    # lmra_agreement = models.FileField(_("LMRA Agreement"), upload_to='doc_library', max_length=100)

    # class Meta:
    #     verbose_name = _("Organization")
    #     verbose_name_plural = _("Organizations")

    def __str__(self):
        return self.full_en_name

    # def get_absolute_url(self):
    #     return reverse("organization-list") #, kwargs={"pk": self.pk})

class Application(models.Model):
    activity_type_list = (
        ('demostic', 'Demostic Labour Employment'),
        ('foreign', 'Foreign Labour Employement'),
        ('local', 'Bahraini Labour Employment')
    )

    financial_guarantee_list = (
        ('manager_cheque', 'Manager Cheque'),
        ('bank_guarantee', 'Bank Guarantee')
    )

    intial_approval_list = (
        ('approve', 'Approve'),
        ('reject', 'Reject')
    )

    app_no = models.CharField(_("Application No"), max_length=50, default='Draft Application')
    app_date = models.DateField(_("Application Date"), default=datetime.date.today)
    app_type = models.CharField(_("Application Type"), max_length=50, default='Initial Approval')
    app_status = models.CharField(_("Status"), max_length=50, default='Draft')
    activty_type = models.CharField(_("Activity Type"), max_length=50, choices=activity_type_list)
    staff_comments = models.TextField(_("Comments"), blank=True)
    manager_comments = models.TextField(_("Manager Comments"), blank=True)
    intial_approval = models.CharField(_("Manager Decision"), max_length=50, choices=intial_approval_list, blank=True)

    financial_guarantee = models.CharField(_("Financial Guarantee"), max_length=50, choices=financial_guarantee_list, blank=True)
    financial_guarantee_expiry_date = models.DateField(_("Financial Guarantee Expiry Date"), null=True, blank=True)

    # start -- org details
    cr = models.CharField(_("CR No"), max_length=50, blank=True)
    cr_reg_date = models.DateField(_("Registration Date"), null=True, blank=True)
    full_en_name = models.CharField(_("Commercial Eng Name"), max_length=250, blank=True)
    license_no = models.CharField(_("License No"), max_length=50, blank=True)
    license_expiry_date = models.DateField(_("License Expiry Date"), null=True, blank=True)
    flat_no = models.IntegerField(_("Flat No"), default=0)
    building_no = models.IntegerField(_("Building No"), default=0)
    road_no = models.IntegerField(_("Road No"), default=0)
    area = models.CharField(_("Area"), max_length=50, blank=True)
    contact1 = models.CharField(_("Phone"), max_length=50, blank=True)
    contact2 = models.CharField(_("Fax"), max_length=50, blank=True)
    email = models.EmailField(_("Email"), max_length=254, blank=True)
    # end -- org details

    # start -- female accomodation
    fh_flat_no = models.IntegerField(_("Flat No"), default=0)
    fh_building_no = models.IntegerField(_("Building No"), default=0)
    fh_road_no = models.IntegerField(_("Road No"), default=0)
    fh_area = models.CharField(_("Area"), max_length=50, blank=True)
    fh_contact1 = models.CharField(_("Phone"), max_length=50, blank=True)
    fh_contact2 = models.CharField(_("Fax"), max_length=50, blank=True)

    # start -- files section
    # cert1_doc = models.FileField(_("MOIS Cert"), upload_to='doc_library', max_length=100, default='')
    # cert2_doc = models.FileField(_("MOH Cert"), upload_to='doc_library', max_length=100, default='')
    # cert3_doc = models.FileField(_("MOL Cert"), upload_to='doc_library', max_length=100, default='')

    # cr_rent_doc = models.FileField(_("CR Rental Agreement Doc"), upload_to='doc_library', max_length=100, null=True, blank=True)
    # fh_rent_doc = models.FileField(_("Temp FH Rental Agreement Doc"), upload_to='doc_library', max_length=100, null=True, blank=True)

    # cr_ewa_bill_doc = models.FileField(_("CR EWA Bill Doc"), upload_to='doc_library', max_length=100, null=True, blank=True)
    # fh_ewa_bill_doc = models.FileField(_("Temp FH EWA Bill Doc"), upload_to='doc_library', max_length=100, null=True, blank=True)

    # employment_office_receipt = models.FileField(_("Employment Office Receipt"), upload_to='doc_library', max_length=100, null=True, blank=True)
    # end -- files section

    applicant_id = models.ForeignKey(Applicant, verbose_name=_(""), on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)

    # class Meta:
    #     verbose_name = _("Application")
    #     verbose_name_plural = _("Application")

    def __str__(self):
        return self.app_no

    # def get_absolute_url(self):
    #     return reverse("application-list") #, kwargs={"pk": self.pk})

