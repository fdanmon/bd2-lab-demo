from flask import Flask, render_template, request, make_response, redirect, url_for
from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import re

# Mine
from controllers import *
from models import *

id_regex = re.compile("^[1-9]+[0-9]*$")

app = Flask(__name__)

Base = declarative_base()
engine = create_engine("mysql+mysqlconnector://root:bd2_labs_pass@127.0.0.1:3306/bd2_labs")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    return jsonify({
        'message': 'Hello world!'
    })

@app.route('/persons/info/')
@app.route('/persons/info/all/')
def get_persons():
    try:
        persons = session.query(person.Person).all()
        if persons:
            res = []
            for p in persons:
                new = personhandler.PersonHandler.parse(p)
                res.append(new)
            return jsonify(res)
        else:
            return jsonify({'message': 'There are no results.'})
    except Exception as e:
        return jsonify({'error': e})

@app.route('/persons/info/<id>/')
def get_person(id=id):
    if id_regex.match(id):
        try:
            p = session.query(person.Person).filter_by(id=id).first()
            if p:
                return jsonify(personhandler.PersonHandler.parse(p))
            else:
                return jsonify({'message': 'There are no results.'})
        except Exception as e:
            return jsonify({'error': e})
    else:
        return jsonify({'message': 'Value is incorrect!'})

@app.route('/persons/skills/')
@app.route('/persons/skills/all/')
def get_all_person_skills():
    try:
        cursor = conn.cursor()
        query = ('SELECT * FROM person_skills JOIN persons ON persons.id = person_skills.person_id JOIN skills ON skills.id = person_skills.skill_id JOIN categories ON categories.id = skills.category_id')
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        if results and len(results) > 0:
            res_json = []
            for r in results:
                el = PersonHandler.parse_skill(r)
                res_json.append(el)
            return jsonify(res_json)
        else:
            return jsonify({'message': 'There are no results.'})
    except mysql.connector.Error as e:
        if cursor:
            cursor.close()
        return e

@app.route('/persons/skills/<id>/')
def get_person_skills(id=id):
    if id_regex.match(id):
        try:
            cursor = conn.cursor()
            query = ('SELECT * FROM person_skills JOIN persons ON persons.id = person_skills.person_id JOIN skills ON skills.id = person_skills.skill_id JOIN categories ON categories.id = skills.category_id WHERE person_skills.person_id = %(id)s')
            cursor.execute(query, {'id': id})
            results = cursor.fetchall()
            cursor.close()
            if results and len(results) > 0:
                res_json = []
                for r in results:
                    el = PersonHandler.parse_skill(r)
                    res_json.append(el)
                return jsonify(res_json)
            else:
                return jsonify({'message': 'There are no results.'})
        except mysql.connector.Error as e:
            if cursor:
                cursor.close()
            return e
    else:
        return jsonify({'message': 'Value is incorrect!'})

@app.route('/persons/rating/<id>/')
def get_rating_from_person(id=id):
    if id_regex.match(id):
        try:
            cursor = conn.cursor()
            query = ('SELECT persons.*, FORMAT(AVG(person_skills.rating), 2) FROM person_skills JOIN persons ON persons.id = person_skills.person_id WHERE person_skills.person_id = %(id)s GROUP BY person_skills.person_id')
            cursor.execute(query, {'id': id})
            r = cursor.fetchone()
            cursor.close()
            if r:
                el = PersonHandler.parse_average_rating(r)
                return jsonify(el)
            else:
                return jsonify({'message': 'There are no results.'})
        except mysql.connector.Error as e:
            if cursor:
                cursor.close()
            return e
    else:
        return jsonify({'message': 'Value is incorrect!'})

@app.route('/jobs/top-appliancer/<id>/')
def get_top_appliancer(id):
    try:
        top = session.execute('CALL getTopAppliancer(:id)', {'id': id})
        if top:
            print(top)
            '''
            return jsonify({
                'name': top.name,
                'rating': top.avg_rating
            })
            '''
        else:
            return jsonify({'message': 'There is no results'})
    except Exception as e:
        return jsonify({'error': e})

@app.route('/jobs/')
@app.route('/jobs/all/')
def get_jobs():
    try:
        jobs = session.query(job.Job).all()
        if jobs:
            res = []
            for j in jobs:
                new = jobhandler.JobHandler.parse(j)
                res.append(new) 
            return jsonify(res)
        else:
            return jsonify({'message': 'There are no results.'})
    except Exception as e:
        return jsonify({'error': e})

@app.route('/skills/')
@app.route('/skills/all/')
def get_skills():
    try:
        skills = session.query(skill.Skill).all()
        if skills:
            res = []
            for s in skills:
                new = skillhandler.SkillHandler.parse_info(s)
                res.append(new) 
            return jsonify(res)
        else:
            return jsonify({'message': 'There are no results.'})
    except Exception as e:
        return jsonify({'error': e})

@app.route('/jobs/create/')
def create_job():
    try:
        cats = session.query(category.Category).all()
        comp = session.query(company.Company).all()
        if cats and comp:
            categories = []
            for c in cats:
                new = categoryhandler.CategoryHandler.parse(c)
                categories.append(new)

            companies = []
            for e in comp:
                n = companyhandler.CompanyHandler.parse_info(e)
                companies.append(n)
            
            return render_template('jobs/create.html', categories=categories,companies=companies)
        else:
            return jsonify({'message': 'There are no categories'})
    except Exception as e:
        return jsonify({'error': e})

@app.route('/jobs/store', methods=['POST'])
def store_job():
    if request.method == 'POST':
        try:
            new_job = job.Job(
                title=request.form['title'],
                description=request.form['description'],
                vacancies=request.form['vacancies'],
                category_id=request.form['category_id'],
                company_id=request.form['company_id'],
                status=1
            )
            session.add(new_job)
            session.commit()
            return redirect(url_for('get_jobs'))
        except Exception as e:
            return jsonify({'error': e})
    else:
        return jsonify({'message': 'Method not supported!'})
