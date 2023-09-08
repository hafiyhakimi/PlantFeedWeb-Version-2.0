from django.core.management.base import BaseCommand
from oauth2_provider.models import Application

class Command(BaseCommand):
    help = 'Create OAuth2 Application for PlantLink'

    def handle(self, *args, **kwargs):
        # Check if the application already exists
        application, created = Application.objects.get_or_create(
            name='PlantLink',
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )

        if created:
            # Print the client_id and client_secret
            self.stdout.write(self.style.SUCCESS(f'Client ID: {application.client_id}'))
            self.stdout.write(self.style.SUCCESS(f'Client Secret: {application.client_secret}'))
        else:
            self.stdout.write(self.style.SUCCESS('Application already exists.'))
            
            # Client ID: mIwwuTNkKDGuAIROks9ILTc36ESDOvpcYsXRwNqj
            # Client Secret: pbkdf2_sha256$600000$5pSvxJhmIDwnkr2jHj0yow$WAROr+eEFLHJCcODpi+rPLoqblkaBuL1I7u3VXQCoVA=
