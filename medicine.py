from flask import Flask,render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

class Config():
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://root:1234@localhost/hospital'

class Development_Config(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://root:1234@localhost/hospital'

class Production_Config(Config):
    uri = os.environ.get('DATABASE_URL')
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://","postgresql://",1)
    SQLALCHEMY_DATABASE_URI = uri

env = os.environ.get("ENV","Development")

if env == "Production":
    config_str = Production_Config
else:
    config_str = Development_Config

app = Flask(__name__)
app.config.from_object(config_str)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:welcome$1234@localhost/hospital'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

class Medicine(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    medicine_name = db.Column(db.String(150),  nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    rate = db.Column(db.String(50), nullable = False)

@app.route('/',methods=['GET'])
def home_page():
    return render_template("home.html")

@app.route('/register_medicine',methods=['GET','POST'])
def register_medicine():
    if request.method == "GET":
        return render_template("medicine.html")

    if request.method == "POST":
        medicine_name = request.form["name"]
        quantity = request.form["qty"]
        rate = request.form["rate"]

        medicine = Medicine.query.filter_by(id=id).first()
        if medicine:
            return render_template("medicine.html", msg="Medicine already registered")
        else:
            new_medicine = Medicine(medicine_name=medicine_name,quantity=quantity,rate=rate)
            db.session.add(new_medicine)
            db.session.commit()
            return render_template("medicine.html", medicine=medicine_name)

@app.route('/getAllMedicines',methods=['GET'])
def medicines_list():
    if request.method == 'GET':
        medicines = Medicine.query.all()
        medicines_list=[]
        for medicine in medicines:
            dict={}
            dict['id']= medicine.id
            dict['name'] = medicine.medicine_name
            dict['qty'] = medicine.quantity
            dict['rate'] = medicine.rate
            medicines_list.append(dict)
        return render_template("medicineList.html",medicine = medicines_list)

@app.route('/getMedicine',methods=['GET'])
def medicine_details():
    if request.method == 'GET':
        return render_template("medicineById.html")

@app.route('/getMedicineById', methods=['GET','POST'])
def medicine_by_Id():
    if request.method == 'POST':
        id = request.form['id']
        medicine = Medicine.query.filter_by(id=id).first()
        if medicine:
            medicine_data = {'id': medicine.id, 'name': medicine.medicine_name,
                             'qty': medicine.quantity, 'rate': medicine.rate}

        if medicine_data:
            return render_template("medicineById.html",data=medicine_data)
        else:
            return render_template("medicineById.html", msg="Medicine not Found")

@app.route('/updateMedicine', methods=['POST'])
def medicine_update():
    if request.method == 'POST':
        id = request.form['id']
        print('id', id)
        medicine = Medicine.query.filter_by(id=id).first()
        print('medicine', medicine)
        if medicine:
            medicine_data = {'id': medicine.id, 'name': medicine.medicine_name,
                             'qty': medicine.quantity, 'rate': medicine.rate}
        print(medicine_data)
        if medicine_data:
            return render_template("medicineById.html", update_msg =medicine_data)
        else:
            return render_template("medicineById.html", msg="Medicine not Found")

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        print("inside update")
        id = request.form['id']
        medicine_name = request.form['name']
        quantity = request.form['qty']
        rate=request.form['rate']

        update_medicine = Medicine(id=id,medicine_name=medicine_name, quantity=quantity, rate=rate)
        medicine_data = {'id': update_medicine.id, 'medicine_name': update_medicine.medicine_name,
                           'quantity': update_medicine.quantity, 'rate': update_medicine.rate}
        Medicine.query.filter_by(id=id).update(medicine_data)
        db.session.commit()
        return render_template("medicineById.html", update=medicine_data)

@app.route('/deleteMedicine', methods=['GET','POST'])
def medicine_delete():
    if request.method == 'POST':
        id = request.form["id"]
        medicine = Medicine.query.filter_by(id=id).first()
        medicine_name=medicine.medicine_name

        if medicine:
            Medicine.query.filter_by(id=id).delete()
            db.session.commit()
            return render_template("medicineById.html", msg = medicine_name+" deleted successfully")
        else:
            return render_template("medicineById.html", msg = "Medicine not found")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)
