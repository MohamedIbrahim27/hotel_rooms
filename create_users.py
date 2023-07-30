from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.files import File
from accounts.models import Profile
from faker import Faker
from PIL import Image
import os


class Command(BaseCommand):
    help = 'Create multiple users with profiles'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='The number of users to create')

    def handle(self, *args, **options):
        fake = Faker()
        image_dir = "F:/Programing/1PyThon/django/hotel_rooms/static/images/New folder"

        # Get a list of all image files in the directory
        image_files = os.listdir(image_dir)

        count = options['count']

        for _ in range(count):
            # Generate fake data for the user profile
            username = fake.user_name()
            phone = fake.phone_number()
            country = fake.country()
            address = fake.address()

            # Create a new user
            user = User.objects.create(username=username)

            # Create a new profile instance
            profile = Profile(user=user, phone=phone, country=country, address=address)

            # Open the image file
            with open(os.path.join(image_dir, image_files[_ % len(image_files)]), 'rb') as f:
                # Create a Django File object from the image file
                django_file = File(f)
                # Assign the Django File object to the image field
                profile.image.save(image_files[_ % len(image_files)], django_file, save=True)

            # Save the profile instance
            profile.save()

            self.stdout.write(f'Successfully created user {username} with profile')
