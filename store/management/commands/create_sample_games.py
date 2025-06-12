from django.core.management.base import BaseCommand
from store.models import Game, Category
from datetime import date

class Command(BaseCommand):
    help = 'Creates sample games'

    def handle(self, *args, **kwargs):
        # Get or create categories
        action_category, _ = Category.objects.get_or_create(
            name='Action',
            defaults={
                'description': 'Fast-paced games with emphasis on combat and movement',
                'icon': 'fa-running'
            }
        )

        adventure_category, _ = Category.objects.get_or_create(
            name='Adventure',
            defaults={
                'description': 'Story-driven games with exploration and puzzle-solving',
                'icon': 'fa-compass'
            }
        )

        # Sample games
        games = [
            {
                'title': 'Cyber Warriors 2077',
                'description': 'An action-packed cyberpunk game set in a dystopian future where players navigate through a neon-lit city filled with danger and opportunity.',
                'price': 59.99,
                'category': action_category,
                'developer': 'Future Games Studio',
                'publisher': 'Neon Entertainment',
                'release_date': date(2024, 1, 15),
                'is_featured': True,
                'system_requirements': 'Windows 10/11, 16GB RAM, RTX 3060 or better'
            },
            {
                'title': 'Lost in Time',
                'description': 'An epic adventure game where players travel through different historical periods, solving puzzles and uncovering ancient mysteries.',
                'price': 49.99,
                'category': adventure_category,
                'developer': 'Time Travel Games',
                'publisher': 'Adventure Works',
                'release_date': date(2024, 2, 1),
                'is_featured': True,
                'system_requirements': 'Windows 10/11, 8GB RAM, GTX 1660 or better'
            }
        ]

        for game_data in games:
            Game.objects.get_or_create(
                title=game_data['title'],
                defaults=game_data
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created game "{game_data["title"]}"')
            ) 