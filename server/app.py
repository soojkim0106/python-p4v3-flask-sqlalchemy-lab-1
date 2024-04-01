# # server/app.py
# #!/usr/bin/env python3

# from flask import Flask, make_response, request
# from flask_migrate import Migrate

# from models import db, Earthquake

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.json.compact = False

# migrate = Migrate(app, db)
# db.init_app(app)


# @app.route("/")
# def index():
#     body = {"message": "Flask SQLAlchemy Lab 1"}
#     return make_response(body, 200)


# # Add views here
# @app.route("/earthquakes/<int:id>", methods=["GET"])
# def earthquake_by_id(id):
#     if earthquake := Earthquake.query.get(Earthquake.id == id):
#         body = earthquake.to_dict()
#         status = 200
#     else:
#         body = {"message": f"Earthquake {id} not found."}
#         status = 404

#     return make_response(body, status)

#     # if request.method == "GET":
#     #     serialized_earthquake = [
#     #         earthquake.as_dict() for earthquake in Earthquake.query if earthquake.id == id
#     #     ]
#     #     return serialized_earthquake, 200
#     # else:
#     #     try:
#     #         data = request.get_json()
#     #         earthquake = Earthquake(**data)
#     #         db.session.add(earthquake)
#     #         db.session.commit()
#     #         return earthquake.as_dict(), 201
#     #     except Exception as e:
#     #         db.session.rollback()
#     #         return {"error": str(e)}, 400

#     # try:
#     #     earthquake = Earthquake.query.get_or404(id)
#     #     return earthquake.to_dict(), 200
#     # except Exception as e:
#     #     return {"message": f"Earthquake {id} not found."}, 400


# @app.route("/earthquakes/magnitude/<float:magnitude>", methods=["GET"])
# def earthquake_by_magnitude(magnitude):
#     earthquakes = []
#     for earthquake in Earthquake.query.filter(Earthquake.magnitude >= magnitude).all():
#         earthquakes.append(earthquake.to_dict())

#     body = {"count": len(earthquakes), "quakes": earthquakes}

#     return make_response(body, 200)

#     # if request.method == "GET":

#     #     #! ORM filter!
#     #     serialized_earthquake = [
#     #         earthquake.as_dict() for earthquake in Earthquake.query.filter(Earthquake.magnitude >= magnitude)
#     #     ]
#     #     # earthquakes.append(serialized_earthquake)
#     #     return {
#     #         "count": len(serialized_earthquake),
#     #         "quakes": serialized_earthquake
#     #         }, 200
#     # else:
#     #     try:
#     #         data = request.get_json()
#     #         earthquake = Earthquake(**data)
#     #         db.session.add(earthquake)
#     #         db.session.commit()
#     #         return earthquake.as_dict(), 201
#     #     except Exception as e:
#     #         db.session.rollback()
#     #         return {"error": str(e)}, 400


# if __name__ == "__main__":
#     app.run(port=5555, debug=True)

# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()
    
    if earthquake:
        body = earthquake.to_dict()
        status = 200
    else:
        body = {'message': f'Earthquake {id} not found.'}
        status = 404
    
    return make_response(body,status)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquake_by_magnitude(magnitude):
    earthquakes = []
    for earthquake in Earthquake.query.filter(Earthquake.magnitude >= magnitude).all():
        earthquakes.append(earthquake.to_dict())
    
    body = {'count': len(earthquakes),
            'quakes': earthquakes
            }
    
    return make_response(body,200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)