from flaskblog import db
from flaskblog.models import User

db.create_all()

print("DB created.")