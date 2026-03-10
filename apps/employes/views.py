from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import role_requis
from .models import Employe

@login_required
@role_requis('admin', 'rh', 'manager') # Seuls les cadres voient la liste complète
def liste_employes(request):
    employes = Employe.objects.all().select_related('departement')
    return render(request, 'employes/liste.html', {'employes': employes})

@login_required
def detail_employe(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    # Un employé ne peut voir que son détail, sauf Admin/RH
    if request.user.role not in ('admin', 'rh') and request.user.employe != employe:
        return render(request, '403_zone.html')
    return render(request, 'employes/detail.html', {'employe': employe})
