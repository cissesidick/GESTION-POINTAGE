from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.contrib import messages

class CustomLoginView(LoginView):
    def form_valid(self, form):
        # On authentifie l'utilisateur
        super().form_valid(form)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect_url': self.get_success_url()})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # On récupère le premier message d'erreur
            errors = form.errors.get('__all__', ['Identifiants invalides'])
            return JsonResponse({'success': False, 'message': errors[0]}, status=400)
        return super().form_invalid(form)
