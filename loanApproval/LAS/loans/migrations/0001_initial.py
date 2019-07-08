# Generated by Django 2.1.5 on 2019-04-06 11:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAdmin',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('TeamName', models.CharField(choices=[('A', 'A'), ('B', 'B')], default='A', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='CreditHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PaymentDelays', models.IntegerField(default=0)),
                ('CurrentDebt', models.IntegerField(default=0)),
                ('TimeSinceLastCredit', models.DateTimeField(verbose_name='date last credited')),
                ('AverageIncome', models.IntegerField(default=0)),
                ('AccountBalance', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('Gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=7)),
                ('Married', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=3)),
                ('Dependents', models.IntegerField(default=0)),
                ('Education', models.CharField(choices=[('Graduate', 'Graduate'), ('Not Graduate', 'Not Graduate')], default='Graduate', max_length=13)),
                ('history', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='loans.CreditHistory')),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TotalAmount', models.IntegerField(default=0)),
                ('Purpose', models.CharField(default='None', max_length=300)),
                ('MonthlyPayment', models.IntegerField(default=0)),
                ('Interest', models.FloatField(default=0)),
                ('LoanStatus', models.CharField(choices=[('Approved', 'Approved'), ('Waiting for Review', 'Waiting for Review'), ('Declined', 'Declined')], default='Waiting for Review', max_length=2)),
                ('Applicant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='loans.Customer')),
                ('coApplicant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partner', to='loans.Customer')),
            ],
        ),
    ]
