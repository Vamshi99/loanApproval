from django.db import models
# from django.db.models import IntegerField,CharField,FloatField,DateTimeField,EmailField
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from math import floor



class BankAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    TeamName=models.CharField(max_length=7,choices=(('A','A'),('B','B')),default='A')

    # def __str__(self):
    #     return self.TeamName


class CreditHistory(models.Model):
    #credit info
    PaymentDelays=models.IntegerField(default=0)
    CurrentDebt=models.IntegerField(default=0)
    TimeSinceLastCredit=models.DateTimeField('date last credited')
    #bank account behavioral
    AverageIncome=models.IntegerField(default=0)
    AccountBalance=models.IntegerField(default=0)

    # def __str__(self):
    #     return self.AccountBalance + ', ' + self.AverageIncome


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    Gender=models.CharField(max_length=7,choices=(('Male','Male'),('Female','Female')),default='Male')
    Married=models.CharField(max_length=3,choices=(('Yes','Yes'),('No','No')),default='Yes')
    Dependents=models.IntegerField(default=0)
    Education=models.CharField(max_length=13,choices=(('Graduate','Graduate'),('Not Graduate','Not Graduate')),default='Graduate')
    history=models.OneToOneField('CreditHistory', on_delete=models.CASCADE,null=True,blank=True,default=None)


class Loan(models.Model):
    Applicant=models.ForeignKey('Customer',on_delete=models.CASCADE,related_name='customer',blank=True,null=True)
    coApplicant = models.ForeignKey('Customer', on_delete=models.CASCADE,related_name='partner',blank=True,null=True)
    TotalAmount=models.PositiveIntegerField(default=0)
    Purpose=models.CharField(max_length=300,default='None')
    Period=models.PositiveIntegerField(default=1, help_text='In number of months')
    LoanStatus=models.CharField(max_length=30,choices=(('Approved','Approved'),('Waiting for Review','Waiting for Review'),('Declined','Declined')),default='Waiting for Review')
    id_proof=models.ImageField(upload_to='media/',null=True, blank=True)
    MonthlyPayment=models.PositiveIntegerField(default=0)

    def save(self,*args,**kwargs):
        self.MonthlyPayment = floor(self.TotalAmount/self.Period)
        super(Loan, self).save(*args,**kwargs)

    # def __str__(self):
    #     return self.Purpose + ', ' + self.TotalAmount