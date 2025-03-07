from django.shortcuts import render
from django.views.generic import TemplateView
from .models import HomePageContent
from parkings.models import Parking
from residences.models import Residence
from reservations.models import Reservation

class HomePageView(TemplateView):
    """
    Home page view to display dynamic content and summary information
    """
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the most recent home page content, or create a default if none exists
        home_content = HomePageContent.objects.filter(is_active=True).first()
        if not home_content:
            home_content = HomePageContent.objects.create(
                title='Bienvenido a ProntoPark',
                subtitle='Mapa de estacionamientos',
                description='Esta plataforma permite gestionar la reserva de estacionamientos de manera rápida y sencilla. Más de 10 condominios ya confían en nosotros.',
                is_active=True
            )
        context['home_content'] = home_content

        # Add summary statistics
        context['total_parkings'] = Parking.objects.count()
        context['total_residences'] = Residence.objects.count()
        context['total_reservations'] = Reservation.objects.count()

        return context

def handler404(request, exception):
    """
    Custom 404 error page view
    """
    return render(request, 'home/404.html', status=404)

def handler500(request):
    """
    Custom 500 error page view
    """
    return render(request, 'home/500.html', status=500)
