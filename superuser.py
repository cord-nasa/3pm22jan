import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Cord.settings")
django.setup()

User = get_user_model()

# --- CHANGE THESE TO YOUR REAL LOGIN DETAILS ---
USERNAME = "anand"             # Your desired username
EMAIL = "puthusseryantonyanand@gmail.com"    # Your desired email
PASSWORD = "Enroute@1999"       # Your desired password
# -----------------------------------------------

if not User.objects.filter(username=USERNAME).exists():
    print(f"Creating superuser: {USERNAME}")
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
else:
    print(f"Superuser {USERNAME} already exists.")