from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError

class Command(BaseCommand):
    help = "Creates an unique index on the email field of the user table (PostgreSQL)"

    def handle(self, *args, **options):
        cursor = connection.cursor()
        try:
            cursor.execute("CREATE UNIQUE INDEX auth_user_unique_email ON auth_user (email)")
            print "Created unique index on email field."
        except OperationalError, e:
            print e
