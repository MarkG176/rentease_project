from django.contrib.messages.context_processors import messages
from django.shortcuts import render, get_object_or_404, redirect
from datetime import timedelta, date
# Create your views here.
from django.shortcuts import render
from .models import Tenants, Properties, Payments

def tenants_view(request):
    tenants = Tenants.objects.all()
    return render(request, 'tenants.html', {'tenants': tenants})

def properties_view(request):
    properties = Properties.objects.all()
    return render(request, 'properties.html', {'properties': properties})

def payments_view(request):
    payments = Payments.objects.all()
    return render(request, 'payments.html', {'payments': payments})


def dashboard(request):
    return render(request,'dashboard.html')


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