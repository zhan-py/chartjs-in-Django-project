from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Donation, BigType, SmallType
from .forms import DonationForm, DonationFilterForm, BigTypeForm, SmallTypeForm, DonationFilterForPDF, DonationFilterByYear
from django.http import JsonResponse
from user_registration.models import User
from django.db import models
from django.urls import reverse, reverse_lazy
from datetime import datetime
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
import json
from django.db.models import Sum, Count, F
from django.db.models.functions import ExtractMonth
from datetime import date, timedelta
from django.conf import settings
from django.views import View
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives



def dashboard(request):
    current_year = date.today().year 
    previous_year = current_year - 1
    MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    #metrics for cards on the left of the dashboard
    total_donation_amount = round(Donation.objects.filter(date__year=current_year).aggregate(Sum('amount'))['amount__sum']) or 0
    total_donation_amount_K = round(total_donation_amount/1000) 
    donation_count = Donation.objects.filter(date__year=current_year).count() or 0
    user_count = User.objects.count()

    ############# get donation data by month #############
    def get_monthly_donation_data(year):
        monthly_totals = Donation.objects.filter(date__year=year).annotate(
            month=ExtractMonth('date')
        ).values('month').annotate(
            total_amount=Sum('amount'),
            total_count=Count('id')
        ).order_by('month')

        months = list(monthly_totals.values_list('month', flat=True))
        amounts = list(monthly_totals.values_list('total_amount', flat=True))
        amounts_float = [float(amount) for amount in amounts]
        counts = list(monthly_totals.values_list('total_count', flat=True))

        return months, amounts_float, counts


    monthly_donation_data_current_year = get_monthly_donation_data(current_year)
    monthly_donation_data_previous_year = get_monthly_donation_data(previous_year)
    

    #donation amount of current year and previous year
    area_chart_data = {
        'labels': MONTHS,
        'data_current_year': monthly_donation_data_current_year[1],
        'data_last_year': monthly_donation_data_previous_year[1],
    }

    area_chart_data_json = json.dumps(area_chart_data)
    

    #donation count of current year and previous year
    column_chart_data = {
        'labels': MONTHS,
        'data_current_year': monthly_donation_data_current_year[2],
        'data_last_year': monthly_donation_data_previous_year[2],
    }

    double_column_chart_data_json = json.dumps(column_chart_data)

    
    ############# get donation data by category #############
    def get_small_type_donation_data(year):
        small_type_totals = Donation.objects.filter(date__year=year).values(
            'small_type__code'
        ).annotate(
            total_amount=Sum(F('amount'))
        ).order_by('small_type__code')

        small_types = list(small_type_totals.values_list('small_type__code', flat=True))
        amounts = list(small_type_totals.values_list('total_amount', flat=True))
        amounts_float = [float(amount) for amount in amounts]

        return small_types, amounts_float


    small_type_names = list(SmallType.objects.values_list('code', flat=True))

    def get_amounts_for_small_types(year, small_type_names):
        small_type_donation_data = get_small_type_donation_data(year)
        mapped_data = dict(zip(small_type_donation_data[0], small_type_donation_data[1]))
        amounts_for_small_types = [mapped_data.get(name, 0) for name in small_type_names]

        return amounts_for_small_types


    amounts_for_small_types_current_year = get_amounts_for_small_types(current_year, small_type_names)
    amounts_for_small_types_previous_year = get_amounts_for_small_types(previous_year, small_type_names)

    column_chart_data = {
        'labels': small_type_names,
        'data_current_year': amounts_for_small_types_current_year,
        'data_previous_year': amounts_for_small_types_previous_year,
    }

    column_chart_data_json = json.dumps(column_chart_data)

    ############# get donation data by year #############
    def get_annual_totals():
        annual_totals = Donation.objects.values('date__year').annotate(
            total_amount=Sum('amount')
        ).order_by('date__year')

        return annual_totals

    annual_totals = get_annual_totals()
    years = [entry['date__year'] for entry in annual_totals]
    amount_of_year = [float(entry['total_amount']) for entry in annual_totals]

    line_chart_data = {
        'labels': years,
        'data_set': amount_of_year,
    }

    line_chart_data_json = json.dumps(line_chart_data)


    context = {
                'total_donation_amount': total_donation_amount,
                'total_donation_amount_K': total_donation_amount_K,
                'donation_count': donation_count,
                'user_count': user_count,
                'area_chart_data_json': area_chart_data_json,
                'double_column_chart_data_json': double_column_chart_data_json,
                'line_chart_data_json': line_chart_data_json,
                'column_chart_data_json': column_chart_data_json,               
               }  

    return render(request, 'dashboard.html', context)
