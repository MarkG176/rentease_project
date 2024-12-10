from itertools import count

from calendar import month

from django.contrib.messages.context_processors import messages
from django.db.models import Count, ExpressionWrapper, Sum
from django.db.models.functions.datetime import TruncMonth
from django.forms import DurationField
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from datetime import timedelta, date
# Create your views here.
from django.shortcuts import render

from .app_forms import TenantForm, IncidentForm
from .models import Tenants, Properties, Payments, Incidents


def tenants_view(request):
    tenants = Tenants.objects.all()

    # Apply filters
    name = request.GET.get('name', '').strip()
    email = request.GET.get('email', '').strip()
    phone = request.GET.get('phone', '').strip()
    adm_no = request.GET.get('adm_no', '').strip()

    if name:
        tenants = tenants.filter(name__icontains=name)
    if email:
        tenants = tenants.filter(email__icontains=email)
    if phone:
        tenants = tenants.filter(phone__icontains=phone)
    if adm_no:
        tenants = tenants.filter(adm_no__icontains=adm_no)

    return render(request, 'tenants.html', {'tenants': tenants})


def delete_tenant(request, tenant):
    tenant = Tenants.objects.get()
    tenant.delete()
    # messages.info(request, f"Customer {tenant.name} was deleted!!")
    return redirect('customers')


# def delays_chart(request):
#     # Calculate delays for payments with a delay
#     payments_with_delay = Payments.objects.annotate(
#         delay=ExpressionWrapper(
#             f('payment_date') - f('expected_date'),
#             output_field=DurationField()
#         )
#     ).filter(delay__gt=timedelta(0))  # Filter only payments with positive delays
#
#     # Prepare data for the chart
#     labels = [f"Lot {payment.lot_no.lot_no}" for payment in payments_with_delay]
#     data = [payment.delay.days for payment in payments_with_delay]
#
#     return JsonResponse({
#         "data": {
#             "labels": labels,
#             "datasets": [{
#                 "label": "Delays (Days)",
#                 "data": data,
#                 "backgroundColor": "#f6c23e",
#                 "hoverBackgroundColor": "#dda20a",
#                 "borderColor": "#f1d6a5",
#             }],
#         },
#     })


def add_tenant(request):
    if request.method == "POST":
        form = TenantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # messages.success(request, f"Customer {form.cleaned_data['first_name']} was added!")
            return redirect('customers')
    else:
        form = TenantForm()
    return render(request, 'tenant_form.html', {"form": form})


def properties_view(request):
    # Get filter parameters
    lot_no = request.GET.get('lot_no', '')
    tenant = request.GET.get('tenant', '')
    min_area = request.GET.get('min_area', '')
    max_area = request.GET.get('max_area', '')
    price = request.GET.get('price', '')
    availability = request.GET.get('availability', '')

    # Filter the properties
    properties = Properties.objects.all()
    if lot_no:
        properties = properties.filter(lot_no__icontains=lot_no)
    if tenant:
        properties = properties.filter(tenant__name__icontains=tenant)
    if min_area:
        properties = properties.filter(area__gte=min_area)
    if max_area:
        properties = properties.filter(area__lte=max_area)
    if price:
        properties = properties.filter(price__lte=price)
    if availability:
        properties = properties.filter(available=(availability == 'True'))

    return render(request, 'properties.html', {'properties': properties})


from django.shortcuts import render
from .models import Payments


def payments_view(request):
    # Retrieve the 'sort_by' parameter from GET request
    sort_by = request.GET.get('sort_by', '')

    # Fetch and sort payments
    payments = Payments.objects.all()
    if sort_by:
        payments = payments.order_by(sort_by)

    return render(request, 'payments.html', {'payments': payments, 'request': request})

    return render(request, 'payments.html', {'payments': payments})


def dashboard(request):
    # Calculate total number of tenants
    from main.models import Tenants, Payments

    total_tenants = Tenants.objects.count()

    # Calculate earnings by month
    earnings_by_month = (
        Payments.objects
        .annotate(month=TruncMonth('payment_date'))  # Truncate to month
        .values('month')
        .annotate(total_earnings=Sum('payment_amount'))  # Use 'payment_amount' instead of 'amount'
        .order_by('month')
    )

    context = {
        'total_tenants': total_tenants,
        'earnings_by_month': earnings_by_month,
    }

    return render(request, 'dashboard.html', context)


def incident_view(request):
    from main.models import Incidents
    from main import app_forms
    incidents = Incidents.objects.all()  # Get all incidents
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            form.save()  # Save new incident
            return redirect('incident_view')  # Redirect to the same page after saving
    else:
        form = IncidentForm()

    return render(request, 'incidents.html', {'incidents': incidents, 'form': form})


def incidents_list(request):
    from main.models import Incidents
    lot_no_filter = request.GET.get('lot_no', '')

    if lot_no_filter:
        incidents = Incidents.objects.filter(lot_no=lot_no_filter)
    else:
        incidents = Incidents.objects.all()

    # Get distinct lot numbers to populate the filter dropdown
    lot_nos = Incidents.objects.values_list('lot_no', flat=True).distinct()

    return render(request, 'incidents_list.html', {
        'incidents': incidents,
        'lot_nos': lot_nos,
    })


def assign_lot(request, lot_no):
    if request.method == "POST":
        tenant_id = request.POST.get('tenant_id')
        tenant = get_object_or_404(Tenants, id=tenant_id)
        property = get_object_or_404(Properties, lot_no=lot_no)
        property.tenant = tenant
        property.save()
        # messages.success(request, f'Lot {property.lot_no} was reassigned to {tenant.name}')
        return redirect('properties')
    else:
        property = get_object_or_404(Properties, lot_no=lot_no)
        tenants = Tenants.objects.all()
        return render(request, 'assign.html', {'properties': property, 'tenants': tenants})


def incidents(request):
    return render(request, 'incidents.html')


def incident_detail(request, id):
    incident = get_object_or_404(Incidents, pk=id)
    return render(request, 'incident_detail.html', {'incident': incident})


def incident_edit(request, id):
    # Retrieve the incident or return 404 if not found
    incident = get_object_or_404(Incident, id=id)

    if request.method == 'POST':
        # Bind the form with POST data and the existing incident instance
        form = IncidentForm(request.POST, instance=incident)
        if form.is_valid():
            form.save()
            return redirect('incident_detail', id=incident.id)  # Redirect to the incident detail page after saving
    else:
        form = IncidentForm(instance=incident)

    return render(request, 'incident_edit.html', {'form': form, 'incident': incident})


# View for deleting an incident
def incident_delete(request, id):
    # Retrieve the incident or return 404 if not found
    incident = get_object_or_404(Incident, id=id)

    if request.method == 'POST':
        # Delete the incident if the POST request is made
        incident.delete()
        return redirect('incident_list')  # Redirect to the incident list page after deletion

    return render(request, 'incident_delete.html', {'incident': incident})
