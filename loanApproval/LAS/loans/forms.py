from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.db import transaction
from django.forms import ModelForm
from django.utils import timezone
from django.contrib.auth.models import User


from .models import Customer, BankAdmin, Loan

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2

class PasswordResetForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)

class PasswordInputForm(forms.Form):
    password = forms.CharField(label=("Current Password"), widget=forms.PasswordInput())


class CustomerInfoForm(forms.ModelForm):
    class Meta():
        model = Customer
        fields = ('Gender','Married','Dependents','Education')

    # def save(self, user=None):
    #     user_profile = super(CustomerInfoForm, self).save(commit=False)
    #     if user:
    #         user_profile.user = user
    #     user_profile.save()
    #     return user_profile


class LoanViewForm(forms.ModelForm):
    class Meta():
        model = Loan
        fields = ('id','TotalAmount','Purpose','Period','MonthlyPayment','LoanStatus')


class LoanInfoForm(forms.ModelForm):
    class Meta():
        model = Loan
        fields = ('TotalAmount','Purpose','Period','id_proof',)

# class CustomerSignUpForm(UserCreationForm):
#     class Meta:
#         model = Customer
#         fields = ('Creator', 'TotalAmount', 'Purpose','MonthlyPayment','Interest','LoanStatus')

class CustomerSignUpForm(UserCreationForm):
    Gender = forms.CharField(
        max_length=7,
        widget=forms.Select(choices=(('Male','Male'),('Female','Female'))),
    )
    Married = forms.CharField(
        max_length=3,
        widget=forms.Select(choices=(('Yes','Yes'),('No','No'))),
    )
    Dependents = forms.IntegerField()
    Education = forms.CharField(
        max_length=13,
        widget=forms.Select(choices=(('Graduate','Graduate'),('Not Graduate','Not Graduate'))),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # fields = '__all__'
        # fields = ('first_name', 'email', 'password')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(user=user)
        customer.Gender = self.cleaned_data['Gender']
        customer.Married = self.cleaned_data['Married']
        customer.Dependents= self.cleaned_data['Dependents']
        customer.Education = self.cleaned_data['Education']
        return customer

# class CustomerChangeForm(ModelForm):
#     class Meta:
#         model = Customer
#         fields = ('user', 'Gender', 'Married','Dependents','Education')
#         #fields = ('user', 'Gender', 'Married','Dependents','Education','ApplicantIncome','CoapplicantIncome','Housing','PropertyArea', 'ExistingClient','TotalDebt','AccountBalance','PaymentDelays','CurrentDebt','lengthOfCreditHistory','TimeSinceLastCredit','AverageIncome','MaximumIncome','MinimumIncome','CreditTurnover','NumberofMissedPayments','TimesExceedCreditLimit','TimesChangedAddress')

class BankAdminSignUpForm(UserCreationForm):
    TeamName = forms.CharField(
        max_length=7,
        widget=forms.Select(choices=(('A','A'),('B','B')))
    )
    class Meta(UserCreationForm.Meta):
        model = User
    #     fields = '__all__'

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_bank_admin = True
        user.save()
        bankadmin = BankAdmin.objects.create(user=user)
        bankadmin = self.cleaned_data['TeamName']
        return bankadmin