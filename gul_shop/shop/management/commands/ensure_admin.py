import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "ADMIN_USERNAME / ADMIN_PASSWORD берилсе, ээсинин аккаунтун түзөт (бар болсо өткөрүп жиберет)"

    def handle(self, *args, **opts):
        username = os.environ.get("ADMIN_USERNAME")
        password = os.environ.get("ADMIN_PASSWORD")
        if not username or not password:
            self.stdout.write("ADMIN_USERNAME/ADMIN_PASSWORD жок — админ түзүлгөн жок.")
            return
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write(f"'{username}' мурунтан бар.")
            return
        User.objects.create_superuser(username=username, email=os.environ.get("ADMIN_EMAIL", ""), password=password)
        self.stdout.write(self.style.SUCCESS(f"'{username}' админ түзүлдү."))
