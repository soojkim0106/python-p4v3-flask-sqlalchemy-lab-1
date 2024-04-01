# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, request
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/")
def index():
    body = {"message": "Flask SQLAlchemy Lab 1"}
    return make_response(body, 200)


# Add views here
@app.route("/earthquakes/<int:id>", methods=["GET"])
def earthquake_by_id(id):

    if request.method == "GET":
        serialized_earthquake = [
            earthquake.as_dict() for earthquake in Earthquake.query if earthquake.id == id
        ]
        return serialized_earthquake, 200
    else:
        try:
            data = request.get_json()
            earthquake = Earthquake(**data)
            db.session.add(earthquake)
            db.session.commit()
            return earthquake.as_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


@app.route("/earthquakes/magnitude/<float:magnitude>", methods=["GET"])
def earthquake_by_magnitude(magnitude):
    
    if request.method == "GET":
        #! ORM filter!
        serialized_earthquake = [
            earthquake.as_dict() for earthquake in Earthquake.query.filter(Earthquake.magnitude >= magnitude) 
        ]

        return {
            "count": len(serialized_earthquake),
            "quakes": serialized_earthquake
            }, 200
    else:
        try:
            data = request.get_json()
            earthquake = Earthquake(**data)
            db.session.add(earthquake)
            db.session.commit()
            return earthquake.as_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)
