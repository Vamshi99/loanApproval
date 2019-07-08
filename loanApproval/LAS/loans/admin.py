from django.contrib import admin

from .models import Loan,Customer,BankAdmin

#admin.site.register(Loan)

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display=('TotalAmount',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=('Gender','Married',)

@admin.register(BankAdmin)
class BankAdminAdmin(admin.ModelAdmin):
    list_display=('TeamName',)
