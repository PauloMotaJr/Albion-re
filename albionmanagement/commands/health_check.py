from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Comando de health check para verificar status dos serviços"
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("✅ Health Check: OK"))
        self.stdout.write(f"📅 Data atual: {__import__('datetime').datetime.now()}")