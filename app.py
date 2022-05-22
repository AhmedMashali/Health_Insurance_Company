from flask import Flask, render_template, request
from db import cur, con

c_id=[0]
plan_type=[0]

app = Flask(__name__)

@app.route("/")
#getting the first page of the site
def index():
    return render_template("index.html")


#continue as customer
@app.route("/customer")
def customer():
    #going to customer page to let the user submit his information
    return render_template("customer.html")


#store the inforamtion about the user in the database
@app.route("/register", methods=["POST"])
def register():

    #store infromation of the user in variables
    f_name = request.form.get("f_name")
    l_name = request.form.get("l_name")
    n_id = request.form.get("n_id")
    age = request.form.get("age")
    p_number = request.form.get("p_number")
    city = request.form.get("city")
    street = request.form.get("street")
    gender = request.form.get("gender")

    #retrieve the national_id from the database to check if this national id already exist
    cur.execute(f"SELECT national_id FROM customers WHERE national_id='{n_id}';")
    x = cur.fetchall()

    #if the national_id exist
    if x:
        return render_template("exist.html")
    else:
        #store customer information in the database
        cur.execute("INSERT INTO customers (national_id, f_name, l_name, phone_number, age, city, street, gender)"
                    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s);",
                    (n_id, f_name, l_name, p_number, age, city, street, gender))

        #make changes persistent into the database
        con.commit()

        #remember the PK of the user using the national id because it is going to be used as a foreign key
        cur.execute(f"SELECT customer_id FROM customers WHERE national_id='{n_id}';")
        records = cur.fetchall()
        c_id[0] = records[0][0]

        #going to ask the user for adding dependent
        return render_template("addDep.html")


#taking information about the depndent
@app.route("/dependent")
def dependent():
    #going to dependent page to let the user submit information about the dependent
    return render_template("dependent.html")


#store the information about the dependent into the database
@app.route("/add_dependent", methods=["post"])
def add_dependent():
    #store informations of the dependent in variables
    name = request.form.get("name")
    gender = request.form.get("gender")
    relation = request.form.get("relation")

    #store the dependent in the database with the foreign key of the customer
    cur.execute(f"INSERT INTO dependents(name, gender, relation, customer_id) VALUES('{name}', '{gender}', '{relation}', {c_id[0]});")

    #make changes persistent into the database
    con.commit()

    #getting the number of hospitals of each plan
    cur.execute("SELECT COUNT(h_id) FROM covers WHERE p_t = 1;")
    basic_c = cur.fetchall()

    cur.execute("SELECT COUNT(h_id) FROM covers WHERE p_t = 2;")
    premium_c = cur.fetchall()

    cur.execute("SELECT COUNT(h_id) FROM covers WHERE p_t = 3;")
    gold_c = cur.fetchall()

    #asking the user for adding more dependents
    return render_template("plain.html", basic=basic_c[0][0], premium=premium_c[0][0], gold=gold_c[0][0])

#choosing a plan
@app.route("/plan")
def plan():
    #getting the number of hospitals of each plan
    cur.execute("SELECT COUNT(h_id) FROM covers WHERE p_t = 1;")
    basic_c = cur.fetchall()

    cur.execute("SELECT COUNT(h_id) FROM covers WHERE p_t = 2;")
    premium_c = cur.fetchall()

    cur.execute("SELECT COUNT(h_id) FROM covers WHERE p_t = 3;")
    gold_c = cur.fetchall()

    return render_template("plain.html", basic=basic_c[0][0], premium=premium_c[0][0], gold=gold_c[0][0])


@app.route("/add_plan", methods=["post"])
def add_plan():
    #remember the plan type to use it as foreign key
    plan_type[0] = request.form.get("plan")

    return render_template("beneficiary.html")

#store inforamtion about the plan
@app.route("/beneficiary", methods=["post"])
def beneficiary():
    #store the beneficiary name
    b_name = request.form.get("beneficiary")

    #store information about the plan in the database with two foreign keys: one of the customer and other of the plan
    cur.execute("INSERT INTO plans(beneficiary, customer_id, plan_type)"
                " VALUES(%s, %s, %s);", (b_name, c_id[0], plan_type[0]))

    #make changes persistent into the database
    con.commit()

    #going to the profile page of the user
    return render_template("profile.html")


@app.route("/cust_profile")
def cust_profile():
    return render_template("/profile.html")

@app.route("/dependent2", methods=["post"])
def dependent2():
    return render_template("dependent2.html")

@app.route("/add_dependent2", methods=["post"])
def add_dependent2():
    #store information of the dependent in variables
    name = request.form.get("name")
    gender = request.form.get("gender")
    relation = request.form.get("relation")

    #store the dependent in the database with the foreign key of the customer
    cur.execute(f"INSERT INTO dependents(name, gender, relation, customer_id) VALUES('{name}', '{gender}', '{relation}', {c_id[0]});")

    #make changes persistent into the database
    con.commit()
    return render_template("/profile.html")

@app.route("/purchased_plans")
def purchased_plans():
    cur.execute(f"SELECT plan_type, beneficiary FROM plans WHERE customer_id ={c_id[0]};")
    p = cur.fetchall()
    print("before passing it", p)

    lenn = len(p)

    return render_template("purchased_plan.html", p=p, lenn=lenn)


#viewing hospitals of the purchased plan
@app.route("/viewHospitals", methods=["post"])
def viewHospitals():
    plan_t = request.form.get("plan_t")
    print("plan_t from viewHospitals", plan_t)
    #retrieve hospitals information from the database
    cur.execute(f"SELECT hospital_name, city, street FROM hospitals INNER JOIN covers ON h_id = hospital_id and p_t = {plan_t};")
    hospitals =[]
    city = []
    street= []
    re = cur.fetchall()
    lenn = len(re)
    #storing the retrieved information into lists
    for i in range(lenn):
        hospitals.append(re[i][0])
        city.append((re[i][1]))
        street.append((re[i][2]))

    #passing the hsopitals information to the html page to view it to the user
    return render_template("availablehospitals.html", hospitals=hospitals, city=city, street=street, lenn=lenn)


#taking claim from the user
@app.route("/addClaim", methods=["post"])
def addClaim():
    return render_template("claim.html")


@app.route("/storeClaim", methods=["post"])
def store():
    #store the information of the claim into variables
    national_id = request.form.get("national_id")
    beneficiary = request.form.get("beneficiary")
    hospital = request.form.get("hospital")
    expense_amount = request.form.get("expense_amount")
    expense_details = request.form.get("expense_details")

    #retrieve the PK of the customer using the national id to use it as a foreign key
    cur.execute(f"SELECT customer_id FROM customers where national_id='{national_id}';")
    rec1 = cur.fetchall()
    customer_id = rec1[0][0]

    #retrieve the PK of the plan using the PK of the user and the beneficiary name
    cur.execute(f"SELECT plan_id FROM plans WHERE customer_id = '{customer_id}' and beneficiary = '{beneficiary}';")
    rec2 = cur.fetchall()
    plan_id = rec2[0][0]

    #store information about the claim into the database
    cur.execute(f"INSERT INTO claims(expense_amount, expense_details, resolved, beneficiry, hospital, customer_id, plan_id) VALUES('{expense_amount}', '{expense_details}', 0, '{beneficiary}', '{hospital}',{customer_id} , {plan_id});")

    #make changes persistent into the database
    con.commit()

    return render_template("profile.html")
#end of customer




#continue as admin
@app.route("/admin")
def admin():
    #going to the main page of the admin
    return render_template("admin.html")


#getting informations about new hospital
@app.route("/add_hospital")
def add_hospital():
    return render_template("addhospital.html")

#add new hospital into the database
@app.route("/store_hospital", methods=["post"])
def store_hospital():
    #sotore information of the new hospitals in variables
    hospital_name = request.form.get("hospital_name")
    city = request.form.get("city")
    street = request.form.get("street")

    #store new hospital into the database
    cur.execute(f"INSERT INTO hospitals (hospital_name, city, street) VALUES('{hospital_name}', '{city}', '{street}');")

    #retreive the PK of the hospital to use as a foreign key in cover table
    cur.execute(f"SELECT hospital_id FROM hospitals WHERE hospital_name='{hospital_name}' and city='{city}' and street='{street}';")
    ree=cur.fetchall()
    h_id = ree[0][0]

    #plan type
    basic= request.form.get("basic")
    premium = request.form.get("premium")
    gold = request.form.get("gold")

    #associate the new hospital with a plan type in the database
    if basic:
        cur.execute(f"INSERT INTO covers(p_t, h_id) VALUES({basic}, {h_id});")

    if premium:
        cur.execute(f"INSERT INTO covers(p_t, h_id) VALUES({premium}, {h_id});")

    if gold:
        cur.execute(f"INSERT INTO covers(p_t, h_id) VALUES({gold}, {h_id});")

    #make changes persistent into the database
    con.commit()

    return render_template("admin.html")


#view all claims
@app.route("/view_claims")
def view_claims():
    s = cur.fetchall()
    c_id=[]
    c_r=[]
    lenn =len(s)
    #store claim_id and resolved in lists
    for i in range(lenn):
        c_id.append(s[i][0])
        c_r.append(s[i][1])

    #passing claims to the html page to view it to the admin
    return render_template("allclaims.html", c_id=c_id, c_r=c_r, lenn=lenn)


#to store the claim_id to update unresolved state if admin mark it as resolved
claim_id=[0]


@app.route("/claim_detail", methods=["post"])
def claim_detail():
    #retrieve claim_id and store it
    claim_id[0] = request.form.get("claim_id")

    #retrieve all inforamtion of the claim from the database
    cur.execute(f"SELECT expense_amount, expense_details, resolved, beneficiry, hospital FROM claims WHERE claim_id={claim_id[0]};")
    s = cur.fetchall()

    #passing the information of the claim into the html page to view it to the admin
    return render_template("claimdetails.html", s=s, claim_id=claim_id[0])


#change unresolved claim to resolved
@app.route("/resolve_claim", methods=["post"])
def resolve_claim():
    #change the unresolved claim to resloved in the database
    cur.execute(f"UPDATE claims SET resolved = 1 WHERE claim_id ={claim_id[0]};")

    #make changes persistent into the database
    con.commit()

    #retrieve information of the claim from the database after changing the resolved state
    cur.execute(f"SELECT expense_amount, expense_details, resolved, beneficiry, hospital FROM claims WHERE claim_id={claim_id[0]};")
    s = cur.fetchall()

    #passing information of the claim to the html page after changing resolved state to view it to the admin
    return render_template("claimdetails.html", s=s, claim_id=claim_id[0])


#view resolved claims
@app.route("/view_resolved_claims")
def view_resolved_claims():
    #retrieve all resolved claims from the database
    cur.execute(f"SELECT claim_id, expense_amount, expense_details, beneficiry, hospital FROM claims WHERE resolved = 1;")
    s = cur.fetchall()
    lenn = len(s)

    #passing the resolved claims to the html page to view it to the admin
    return render_template("resolvedclaims.html", s=s, lenn=lenn)


#view all customers to the admin
@app.route("/view_customers")
def view_customers():
    #retrieve all customers from the database
    cur.execute(f"SELECT national_id, f_name, l_name, age, gender, phone_number, city, street FROM customers;")
    s = cur.fetchall()
    lenn = len(s)

    #passing information of the customers to the html page to view it to the admin
    return render_template("viewcustomers.html", s=s, lenn=lenn)
