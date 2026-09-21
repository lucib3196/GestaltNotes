from firebase_admin import auth

from src.core import initialize_firebase_app

initialize_firebase_app()


duplicates = ["503bfea3-6085-4577-84b1-f8ab19b1b342"]
to_delete = []


for d in duplicates:
    try:
        user = auth.get_user(d)
        print("Found user", user.uid)
    except Exception:
        print("Adding user to delete")
        to_delete.append(d)
print("Total to delete", to_delete)
