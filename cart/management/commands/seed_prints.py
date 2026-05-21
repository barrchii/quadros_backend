from django.core.management.base import BaseCommand
from cart.models import Print


class Command(BaseCommand):
    def handle(self, *args, **options):
        prints = [
            {'name': 'Puerto Dream', 'slug': 'puerto-dream'},
            {'name': 'Bacocho', 'slug': 'bacocho'},
            {'name': 'Colorada', 'slug': 'colorada'},
            {'name': 'Roger', 'slug': 'roger'},
            {'name': 'Vortex', 'slug': 'vortex'},
            {'name': 'Palmera', 'slug': 'palmera'},
            {'name': 'Agua Blanca', 'slug': 'agua-blanca'},
            {'name': 'Pesca', 'slug': 'pesca'},
        ]

        for p in prints:
            Print.objects.get_or_create(**p)

        self.stdout.write(f'Prints in database: {Print.objects.count()}')