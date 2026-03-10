from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .models import Utilisateur
from apps.employes.models import Employe

def initialiser_compte(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        matricule = request.POST.get('matricule')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'accounts/init_password.html')

        # Trouver l'employé par matricule et email
        emp = Employe.objects.filter(matricule=matricule, email=email).first()
        if not emp:
            messages.error(request, "Aucun employé trouvé avec ces informations.")
            return render(request, 'accounts/init_password.html')

        # Trouver ou créer l'utilisateur associé
        user = Utilisateur.objects.filter(username=matricule).first()
        if not user:
            # Si l'admin a créé l'employé mais pas l'utilisateur
            user = Utilisateur.objects.create_user(
                username=matricule,
                email=email,
                password=password,
                employe=emp,
                role='employe'
            )
            messages.success(request, "Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
        else:
            # Si l'utilisateur existe déjà (créé par l'admin)
            user.set_password(password)
            user.save()
            messages.success(request, "Mot de passe configuré ! Connectez-vous.")
            
        return redirect('accounts:login')

    return render(request, 'accounts/init_password.html')
