from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .dashboards import role_based_dashboard

@login_required
def dashboard_view(request):
    """
    Bosh sahifa - roliga qarab dashboard ko'rsatadi.
    """
    return role_based_dashboard(request)


def logout_view(request):
    """Custom logout view - chiroyli sahifa ko'rsatadi"""
    logout(request)
    return render(request, 'registration/logged_out.html')
