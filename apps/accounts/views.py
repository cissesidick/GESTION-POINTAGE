from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import Utilisateur
from apps.employes.models import Employe


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'redirect_url': '/pointages/dashboard/'})
        else:
            return JsonResponse({'success': False, 'message': 'Identifiant ou mot de passe incorrect'}, status=400)

    return render(request, 'accounts/login.html')


def initialiser_compte(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        matricule = request.POST.get('matricule')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'accounts/init_password.html')

        emp = Employe.objects.filter(matricule=matricule, email=email).first()
        if not emp:
            messages.error(request, "Aucun employé trouvé avec ces informations.")
            return render(request, 'accounts/init_password.html')

        user = Utilisateur.objects.filter(username=matricule).first()
        if not user:
            user = Utilisateur.objects.create_user(
                username=matricule,
                email=email,
                password=password,
                employe=emp,
                role='employe'
            )
            messages.success(request, "Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
        else:
            user.set_password(password)
            user.save()
            messages.success(request, "Mot de passe configuré ! Connectez-vous.")

        return redirect('accounts:login')

    return render(request, 'accounts/init_password.html')