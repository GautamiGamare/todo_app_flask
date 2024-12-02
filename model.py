from app import app, db  # Import your app and db instances

# Create an application context
with app.app_context():
    db.create_all()  # Or any other code requiring the application context

