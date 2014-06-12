from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError, ProgrammingError

class Command(BaseCommand):
    help = "Creates an unique index on the email field of the user table (PostgreSQL)"

    def handle(self, *args, **options):
        cursor = connection.cursor()
        try:
            cursor.execute("CREATE UNIQUE INDEX auth_user_unique_email ON auth_user (email)")
            print "Created unique index on email field."
        except OperationalError, e:
            print e
        except ProgrammingError, e:
            print e
        try:
            cursor.execute("ALTER TABLE auth_user ADD CONSTRAINT auth_user_unique_email_constraint UNIQUE (email)")
            print "Created unique constraint for email field."
        except OperationalError, e:
            print e
        except ProgrammingError, e:
            print e
