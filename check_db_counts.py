import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.apps import apps

def check_counts():
    app_labels = ['users', 'programs', 'projects', 'blog', 'gallery', 'contact', 'volunteers', 'partnerships', 'impact']
    for app_label in app_labels:
        print(f"--- App: {app_label} ---")
        try:
            app_config = apps.get_app_config(app_label)
            for model_name, model in app_config.models.items():
                count = model.objects.count()
                print(f"{model_name}: {count} rows")
        except Exception as e:
            print(f"Error checking app {app_label}: {e}")

if __name__ == "__main__":
    check_counts()
