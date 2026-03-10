import json, csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import timedelta, date

from apps.employes.models import Employe, Departement
from .models import Pointage, SeanceTravail
from .geofencing import geofencing_requis, verifier_zone
from .utils import get_statut_employe, enregistrer_pointage, calculer_heures_jour

@login_required
def dashboard(request):
    aujourd_hui = timezone.localdate()
    if request.user.role in ('admin', 'rh', 'manager'):
        employes = Employe.objects.filter(statut='actif').select_related('departement')
    else:
        employes = Employe.objects.filter(id=request.user.employe.id) if request.user.employe else Employe.objects.none()

    # KPIs
    total_emp = employes.count()
    
    if request.user.role in ('admin', 'rh', 'manager'):
        seances_du_jour = SeanceTravail.objects.filter(date=aujourd_hui).select_related('employe', 'employe__departement').order_by('-heure_entree')
        presents = sum(1 for e in employes if get_statut_employe(e.id) == 'present')
        kpi_data = {
            'label_1': 'PRÉSENTS', 'val_1': presents, 'color_1': 'primary',
            'label_2': 'RETARDS',  'val_2': 0, 'color_2': 'warning',
            'label_3': 'ABSENCES', 'val_3': total_emp - presents, 'color_3': 'danger',
            'label_4': 'TOTAL',    'val_4': total_emp, 'color_4': 'info'
        }
    else:
        seances_du_jour = SeanceTravail.objects.filter(employe=request.user.employe, date=aujourd_hui).order_by('-heure_entree')
        mes_heures = calculer_heures_jour(request.user.employe.id, aujourd_hui) if request.user.employe else 0
        mon_statut = get_statut_employe(request.user.employe.id) if request.user.employe else 'absent'
        kpi_data = {
            'label_1': 'MON STATUT', 'val_1': mon_statut.upper(), 'color_1': 'success' if mon_statut == 'present' else 'secondary',
            'label_2': 'MES HEURES', 'val_2': f"{mes_heures}h", 'color_2': 'primary',
            'label_3': 'DISTANCE',   'val_3': 'Zone OK' if mon_statut == 'present' else '-', 'color_3': 'info',
            'label_4': 'CONTRAT',    'val_4': f"{request.user.employe.heures_contrat}h" if request.user.employe else '-', 'color_4': 'warning'
        }

    # Graphique (7j)
    labels, valeurs = [], []
    for i in range(6, -1, -1):
        j = aujourd_hui - timedelta(days=i)
        labels.append(j.strftime('%a %d'))
        if request.user.role in ('admin', 'rh'):
            total_h = sum(calculer_heures_jour(e.id, j) for e in employes)
            valeurs.append(round(total_h, 1))
        else:
            valeurs.append(calculer_heures_jour(request.user.employe.id, j) if request.user.employe else 0)

    response = render(request, 'pointages/dashboard.html', {
        'kpis': kpi_data,
        'seances': seances_du_jour,
        'graph_labels': labels,
        'graph_data': valeurs,
        'aujourd_hui': aujourd_hui,
    })
    # Forcer l'actualisation toutes les 20 secondes au niveau HTTP
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@login_required
@geofencing_requis
def pointer(request):
    if request.user.role in ('admin', 'rh'):
        employes = Employe.objects.filter(statut='actif')
    else:
        employes = Employe.objects.filter(id=request.user.employe.id) if request.user.employe else Employe.objects.none()

    geo_status = getattr(request, 'geo_status', {'autorise': False, 'mode_lecture_seule': True})

    emp_statuts = []
    for e in employes:
        statut = get_statut_employe(e.id)
        emp_statuts.append({'employe': e, 'statut': statut})

    if request.method == 'POST':
        if geo_status.get('mode_lecture_seule') and not geo_status.get('bypass'):
            messages.error(request, "Pointage refusé : Hors zone.")
            return redirect('pointages:pointer')

        emp_id = request.POST.get('employe_id')
        if not emp_id:
            messages.error(request, "Veuillez choisir un employé.")
            return redirect('pointages:pointer')

        employe = get_object_or_404(Employe, id=emp_id)
        
        # VERIFICATION : Une seule session par jour
        statut_actuel = get_statut_employe(employe.id)
        if statut_actuel == 'sorti':
            messages.warning(request, f"Pointage impossible : {employe.nom_complet} a déjà terminé sa journée.")
            return redirect('pointages:pointer')

        type_p = 'sortie' if statut_actuel == 'present' else 'entree'
        
        # Enregistrement
        enregistrer_pointage(employe, type_p, geo_status)
        messages.success(request, f"Pointage '{type_p.upper()}' enregistré pour {employe.nom_complet} !")
        return redirect('pointages:dashboard')

    return render(request, 'pointages/pointer.html', {
        'employes_statuts': emp_statuts, 
        'geo_status': geo_status
    })

@login_required
def historique(request):
    seances = SeanceTravail.objects.select_related('employe', 'employe__departement', 'pointage_entree', 'pointage_sortie')
    
    if request.user.role == 'employe' and request.user.employe:
        seances = seances.filter(employe=request.user.employe)
    
    # Filtres par employé (Admin/RH)
    emp_id = request.GET.get('employe')
    if emp_id and request.user.role in ('admin', 'rh'):
        seances = seances.filter(employe_id=emp_id)

    return render(request, 'pointages/historique.html', {
        'seances': seances.order_by('-date', '-heure_entree')[:100],
        'employes': Employe.objects.all() if request.user.role in ('admin', 'rh') else None
    })

@login_required
def api_verifier_zone(request):
    if request.method != 'POST': return JsonResponse({'error': 'Method not allowed'}, status=405)
    data = json.loads(request.body)
    lat, lng = float(data['lat']), float(data['lng'])
    
    request.session['position_gps'] = {'lat': lat, 'lng': lng}
    if request.user.peut_bypasser_geo:
        return JsonResponse({'autorise': True, 'bypass': True, 'message': "Exclus du géofencing."})
    
    res = verifier_zone(lat, lng)
    request.session['position_gps']['distance'] = res['distance_metres']
    return JsonResponse(res)

@login_required
def rapport(request):
    if request.user.role not in ('admin', 'rh', 'manager'):
        return render(request, '403_zone.html')
    
    aujourd_hui = timezone.localdate()
    
    # Gestion du mois (par défaut mois actuel)
    try:
        selection_mois = request.GET.get('mois', aujourd_hui.strftime('%Y-%m'))
        annee, mois = map(int, selection_mois.split('-'))
        debut_mois = date(annee, mois, 1)
        # Calcul du dernier jour du mois
        if mois == 12:
            fin_mois = date(annee + 1, 1, 1) - timedelta(days=1)
        else:
            fin_mois = date(annee, mois + 1, 1) - timedelta(days=1)
            
        # Si c'est le mois en cours, on s'arrête à aujourd'hui
        if debut_mois.month == aujourd_hui.month and debut_mois.year == aujourd_hui.year:
            fin_calcul = aujourd_hui
        else:
            fin_calcul = fin_mois
    except:
        debut_mois = aujourd_hui.replace(day=1)
        fin_calcul = aujourd_hui

    employes = Employe.objects.filter(statut='actif').select_related('departement')
    
    data = []
    for e in employes:
        # Heures cumulées sur la période sélectionnée
        heures_periode = sum(calculer_heures_jour(e.id, debut_mois + timedelta(days=i)) 
                            for i in range((fin_calcul - debut_mois).days + 1))
        
        # Statut aujourd'hui (toujours utile)
        statut = get_statut_employe(e.id)
        
        # Dernier pointage ABSOLU (pour éviter N/A)
        dernier_p = Pointage.objects.filter(employe=e).order_by('-horodatage').first()
        
        data.append({
            'employe': e,
            'heures_mois': round(heures_periode, 2),
            'dernier_pointage': dernier_p.horodatage if dernier_p else None,
            'statut_actuel': statut
        })
        
    return render(request, 'pointages/rapport.html', {
        'rapport_data': data,
        'mois_actuel': debut_mois.strftime('%B %Y'),
        'selection_mois': selection_mois
    })

@login_required
def export_rapport_csv(request):
    if request.user.role not in ('admin', 'rh', 'manager'):
        return HttpResponse("Accès refusé", status=403)
    
    selection_mois = request.GET.get('mois', timezone.localdate().strftime('%Y-%m'))
    try:
        annee, mois = map(int, selection_mois.split('-'))
        debut = date(annee, mois, 1)
        if mois == 12: fin = date(annee+1, 1, 1) - timedelta(days=1)
        else: fin = date(annee, mois+1, 1) - timedelta(days=1)
    except:
        debut = timezone.localdate().replace(day=1)
        fin = timezone.localdate()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Rapport_Pointage_{selection_mois}.csv"'
    response.write(u'\ufeff'.encode('utf8')) 

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Matricule', 'Nom Complet', 'Département', 'Heures Cumulées', 'Dernier Pointage', 'Statut'])

    employes = Employe.objects.filter(statut='actif').select_related('departement')
    for e in employes:
        heures = sum(calculer_heures_jour(e.id, debut + timedelta(days=i)) 
                    for i in range((fin - debut).days + 1))
        
        # Statut aujourd'hui (toujours utile)
        statut = get_statut_employe(e.id)
        
        # Dernier pointage de l'histoire (pour éviter N/A)
        dernier_p = Pointage.objects.filter(employe=e).order_by('-horodatage').first()
        date_p = dernier_p.horodatage.strftime('%d/%m/%Y %H:%M') if dernier_p else 'N/A'

        writer.writerow([
            e.matricule,
            e.nom_complet,
            e.departement.nom if e.departement else '-',
            f"{round(heures, 2)}h",
            date_p,
            statut.upper()
        ])

    return response
