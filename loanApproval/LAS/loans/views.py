from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required

from loans.forms import CustomerSignUpForm, BankAdminSignUpForm, UserForm, CustomerInfoForm, LoanInfoForm, LoanViewForm, PasswordResetForm, SetPasswordForm, PasswordInputForm
from django.conf import settings
from loans.models import Customer, Loan
from django.forms.models import model_to_dict


from django.contrib.auth.tokens import default_token_generator
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
# from django.core.mail import send_mail
from django.conf import settings
# from django.views.generic import *
# from utils.forms.reset_password_form import PasswordResetRequestForm
from django.contrib.auth.models import User


status = {'review': 'Waiting for Review', 'approved': 'Approved', 'declined': 'Declined'}



def index(request):
    return render(request,'registration/base.html')

# def password_reset(request):
#     if request.method == 'POST':
#         email = User.objects.get(email=request.POST.get('email'))
#     return render(request,'registration/password_reset.html',{'pform':pform})

@login_required
def loans_index(request,loan_status=None):
    review = True if loan_status=='review' else False
    if loan_status:
        loans_list = Loan.objects.filter(LoanStatus=status[loan_status])
    else:
        loans_list = Loan.objects.all()
    objects = {}
    for loan in loans_list:
        objects[loan.id] = LoanViewForm(data=model_to_dict(Loan.objects.get(pk=loan.id)))
    return render(request,'registration/loans_list.html',{'objects':objects,'approve':True,'review':review,'empty': empty})

@login_required
def cust_loans_index(request,loan_status=None):
    review = True if loan_status=='review' else False
    if loan_status:
        loans_list = Loan.objects.filter(Applicant=Customer.objects.filter(user=request.user)[0], LoanStatus=status[loan_status])
    else:
       loans_list = Loan.objects.filter(Applicant=Customer.objects.filter(user=request.user)[0])
    objects = {}
    empty = False if loans_list else True
    for loan in loans_list:
        objects[loan.id] = LoanViewForm(data=model_to_dict(Loan.objects.get(pk=loan.id)))
    return render(request,'registration/loans_list.html',{'objects':objects,'review':review,'approve':True,'empty': empty})

@login_required
def review_loan(request,loan_id):
    loan = Loan.objects.get(pk=loan_id)
    message=''
    buttons=False if loan.LoanStatus in ('Approved', 'Declined') else True
    if request.method == 'POST':
        loan_form = LoanInfoForm(request.POST,request.FILES,instance = Loan.objects.get(id=loan_id))
        if loan_form.is_valid():
            if 'approve' in request.POST:
                loan.LoanStatus = 'Approved'
            else:
                loan.LoanStatus = 'Declined'
            loan_form.save()
            loan.save()
            message = loan.LoanStatus + ' Loan Application!'
    else:
        loan_form = LoanInfoForm(instance = Loan.objects.get(id=loan_id))
    return render(request,'registration/edit_info.html',{'form':loan_form,'review':True,'message':message,'buttons':buttons})


@login_required
def edit_loan(request,loan_id):
    message = ''
    if request.method == 'POST':
        loan_form = LoanInfoForm(request.POST,request.FILES,instance = Loan.objects.get(id=loan_id))
        if loan_form.is_valid():
            loan_form.save()
            message = 'Updated Loan Application!'
    else:
        loan_form = LoanInfoForm(instance = Loan.objects.get(id=loan_id))
    return render(request,'registration/edit_info.html',{'form':loan_form,'message':message})


@login_required
def change_password(request):
    p_text = ''
    button_val = 'Change Password'
    if request.method == 'POST':
        inp_form = PasswordInputForm(data=request.POST)
        reset_form = SetPasswordForm(data=request.POST)
        if inp_form.is_valid() and reset_form.is_valid():
            user = authenticate(username=request.user.username, password=inp_form.cleaned_data['password'])
            if user:
                user.set_password(reset_form.cleaned_data['new_password2'])
                user.save()
                p_text = "Password Changed"
            else:
                print(inp_form.errors,reset_form.errors)
    else:
        inp_form = PasswordInputForm()
        reset_form = SetPasswordForm()
    return render(request,'registration/signup_form.html',
                          {'user_form':inp_form,
                           'profile_form':reset_form,
                           'button_val': button_val,
                           'p_text':p_text})


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def edit_profile(request):
    message = ''
    if request.method == 'POST':
        profile_form = CustomerInfoForm(data=request.POST,instance = Customer.objects.get(user=request.user))
        if profile_form.is_valid():
            profile_form.save()
            message = 'Updated Profile!'
    else:
        profile_form = CustomerInfoForm(instance = Customer.objects.get(user=request.user))
    return render(request,'registration/edit_info.html',{'form':profile_form,'message':message})


@login_required
def create_loan(request):
    created = False
    if request.method == 'POST':
        loan_form = LoanInfoForm(request.POST,request.FILES)
        if loan_form.is_valid():
            loan = loan_form.save(commit=False)
            loan.Applicant = Customer.objects.filter(user=request.user)[0]
            loan.save()
            created = True
            print(loan.Applicant)
        else:
            print(loan_form.errors)
    else:
        loan_form = LoanInfoForm()
    return render(request,'registration/loan_entry.html',
                          {'loan_form':loan_form, 'created': created})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))   


def register(request):
    button_val = 'Register'
    p_text = ''
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = CustomerInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            p_text = 'Registration Successfull!'
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = CustomerInfoForm()
    return render(request,'registration/signup_form.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'button_val': button_val,
                           'p_text': p_text})


def user_login(request):
    p_text = ""
    typ = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        typ = True
        if user:
            if user.is_active:
                login(request,user)
                p_text = "Login Successfull"
                #return HttpResponseRedirect(reverse('special'))
            else:
                p_text = "Your account was inactive."
                #return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            p_text = "Invalid login details given"
        return render(request, 'registration/login.html', {'p_text': p_text,'typ': typ})
    else:
        return render(request, 'registration/login.html', {'p_text': p_text,'typ': typ})



def validate_email_address(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def reset_password(request):
    form = PasswordResetForm()
    message = ''
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email_or_username']
            if validate_email_address(data):
                user = User.objects.get(email=data)
            elif User.objects.get(username=data):
                user = User.objects.get(username=data)
            else:
                message = 'No user or email address exists with given input.'
                return render(request,'registration/reset_password.html',{'form':form,'message':message})
            c = {
                'email': user.email,
                'domain': request.META['HTTP_HOST'],
                'site_name': 'example',
                'uid': user.pk,
                'user': user,
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
            }
            # subject_template_name='registration/password_reset_subject.txt'
            # email_template_name='registration/password_reset_email.html'
            # subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            # subject = ''.join(subject.splitlines())
            # email = loader.render_to_string(email_template_name, c)
            # send_mail(subject, email, settings.DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
            message = 'Password reset link sent to email!'
            print('{}/reset_password_confirm/{}-{}/'.format(request.META['HTTP_HOST'],c['uid'],c['token']))
    return render(request,'registration/reset_password.html',{'form':form,'message':message})


def confirm(request, uidb64,token):
    assert uidb64 is not None and token is not None
    user = User.objects.get(pk=uidb64)
    form = SetPasswordForm()
    message = ''
    done = False
    if (user is None) or not default_token_generator.check_token(user, token):
        message = "Invalid link. Try again."
    else:
        if request.method == 'POST':
            form = SetPasswordForm(request.POST)
            if form.is_valid():
                new_password= form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                done=True
                message = 'Password has been reset!'
    return render(request,'registration/confirm.html',{'form':form,'message':message,'done':done})
