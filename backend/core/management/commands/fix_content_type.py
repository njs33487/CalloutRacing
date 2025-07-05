from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Fix django_content_type table by removing rows with NULL name values'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # First, let's see what we're dealing with
            cursor.execute("SELECT id, app_label, model, name FROM django_content_type WHERE name IS NULL")
            null_rows = cursor.fetchall()
            
            if null_rows:
                self.stdout.write(f"Found {len(null_rows)} rows with NULL name values:")
                for row in null_rows:
                    self.stdout.write(f"  ID: {row[0]}, App: {row[1]}, Model: {row[2]}, Name: {row[3]}")
                
                # Delete the problematic rows
                cursor.execute("DELETE FROM django_content_type WHERE name IS NULL")
                deleted_count = cursor.rowcount
                
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully deleted {deleted_count} rows with NULL name values")
                )
            else:
                self.stdout.write("No rows with NULL name values found.")
            
            # Also check for the specific problematic row mentioned in the error
            cursor.execute("SELECT id, app_label, model, name FROM django_content_type WHERE id = 18")
            row_18 = cursor.fetchone()
            if row_18:
                self.stdout.write(f"Row 18: {row_18}")
                if row_18[3] is None:  # name is NULL
                    cursor.execute("DELETE FROM django_content_type WHERE id = 18")
                    self.stdout.write("Deleted row 18 with NULL name")
            
            # Let's also check for any other potential issues
            cursor.execute("SELECT COUNT(*) FROM django_content_type")
            total_count = cursor.fetchone()[0]
            self.stdout.write(f"Total rows in django_content_type: {total_count}")
            
            # Show all rows for debugging
            cursor.execute("SELECT id, app_label, model, name FROM django_content_type ORDER BY id")
            all_rows = cursor.fetchall()
            self.stdout.write("All content type rows:")
            for row in all_rows:
                self.stdout.write(f"  ID: {row[0]}, App: {row[1]}, Model: {row[2]}, Name: {row[3]}") 