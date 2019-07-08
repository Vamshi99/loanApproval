from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls import url
from loans import views


# urlpatterns = [
#     path('signup/submit',views.BankAdminSignUpView.as_view(),name='submit'),
#     path('h',views.index),
#     # path('admi/', admin.site.urls),
# ]


# SET THE NAMESPACE!
app_name = 'loans'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'cust_index/(?P<loan_status>review|approved|declined)/$', views.cust_loans_index, name='cust_index'),
    url(r'cust_index/$', views.cust_loans_index, name='cust_index_all'),
    url(r'index/(?P<loan_status>review|approved|declined)/$', views.loans_index, name='loans_index'),
    url(r'index/$', views.loans_index, name='loans_all'),
    url(r'review/(?P<loan_id>[0-9]+)/$', views.review_loan, name='review_loan'),
    url(r'create/$', views.create_loan, name='create_loan'),
    url(r'^edit_loan/(?P<loan_id>[0-9]+)/$',views.edit_loan,name='edit_loan'),
]