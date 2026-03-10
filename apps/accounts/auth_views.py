from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.http import JsonResponse

class CustomLoginView(LoginView):
    def form_valid(self, form):
        # On connecte l'utilisateur sans rediriger
        login(self.request, form.get_user())
        
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'redirect_url': self.get_success_url()})
        
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = form.errors.get('__all__', ['Identifiants invalides'])
            return JsonResponse({'success': False, 'message': errors[0]}, status=400)
        return super().form_invalid(form)