from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .dashboards import role_based_dashboard

@login_required
def dashboard_view(request):
    """
    Bosh sahifa - roliga qarab dashboard ko'rsatadi.
    """
    return role_based_dashboard(request)