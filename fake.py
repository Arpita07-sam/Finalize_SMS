
from app import app
from details import db, Signature

with app.app_context():

    Signature.query.delete()

    db.session.commit()

    print("All signatures deleted")