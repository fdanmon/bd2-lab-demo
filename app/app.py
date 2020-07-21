from flask import Flask, render_template, request, make_response, redirect, url_for
from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
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
    return render_template('index.html')

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
            return render_template('persons/index.html', persons=res)
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
                pers = personhandler.PersonHandler.parse(p)
                return render_template('persons/detail.html', p=pers)
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
        sql = text("SELECT * FROM person_skills JOIN persons ON persons.id = person_skills.person_id JOIN skills ON skills.id = person_skills.skill_id JOIN categories ON categories.id = skills.category_id")
        results = engine.execute(sql).fetchall()
        if results and len(results) > 0:
            res_json = []
            for r in results:
                el = personhandler.PersonHandler.parse_skill(r)
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
            sql = text("SELECT person_skills.person_id, skills.id, skills.title, person_skills.rating, categories.id, categories.name, persons.name FROM person_skills JOIN persons ON persons.id = person_skills.person_id JOIN skills ON skills.id = person_skills.skill_id JOIN categories ON skills.category_id = categories.id WHERE person_skills.person_id = {}".format(id))
            rows = engine.execute(sql).fetchall()
            if rows:
                sks = []
                for r in rows:
                    el = personhandler.PersonHandler.parse_skill(r)
                    sks.append(el)
                res = {
                    'person': {
                        'id': rows[0][0],
                        'name': rows[0][6]
                    },
                    'skills': sks
                }
                return render_template('persons/skills.html', person_skills=res)
                return jsonify(res)
            else:
                return jsonify({'message': 'There are no results.'})
        except Exception as e:
            return e
    else:
        return jsonify({'message': 'Value is incorrect!'})

@app.route('/persons/rating/<id>/')
def get_rating_from_person(id=id):
    if id_regex.match(id):
        try:
            sql = text("SELECT persons.*, FORMAT(AVG(person_skills.rating), 2) FROM person_skills JOIN persons ON persons.id = person_skills.person_id WHERE person_skills.person_id = {} GROUP BY person_skills.person_id".format(id))
            r = engine.execute(sql).fetchone()
            if r:
                el = personhandler.PersonHandler.parse_average_rating(r)
                return jsonify(el)
            else:
                return jsonify({'message': 'There are no results.'})
        except Exception as e:
            return jsonify({'error': e})
    else:
        return jsonify({'message': 'Value is incorrect!'})

@app.route('/jobs/top-appliancer/<id>/')
def get_top_appliancer(id):
    if id_regex.match(id):
        try:
            sql = text("CALL getTopAppliancer({})".format(id))
            rows = engine.execute(sql).fetchall()
            if rows:
                res = []
                for r in rows:
                    n = {
                        'name': r[0],
                        'rating': r[1]
                    }
                    res.append(n)
                
                return jsonify(res)
            else:
                return jsonify({'message': 'There is no results'})
        except Exception as e:
            return jsonify({'error': e})
    else:
        return jsonify({'error': 'ID value is not correct.'})

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
            return render_template('jobs/index.html',jobs=res)
        else:
            return jsonify({'message': 'There are no results.'})
    except Exception as e:
        return jsonify({'error': e})

@app.route('/jobs/appliances/<id>')
def job_appliances(id):
    try:
        if id_regex.match(id):
            sql = text('SELECT persons.id, persons.name, jobs.id, jobs.title, appliance_date, persons.rating FROM job_appliances JOIN jobs ON job_appliances.job_id = jobs.id JOIN persons ON job_appliances.person_id = persons.id WHERE job_appliances.job_id = {}'.format(id))
            rows = engine.execute(sql).fetchall()
            if rows:
                if len(rows)>0:
                    apps = []
                    for r in rows:
                        new = jobhandler.JobHandler.parse_job_appliances(r)
                        apps.append(new)
                    res = {
                        'job': {
                            'id': rows[0][2],
                            'name': rows[0][3],
                        },
                        'appliancers': apps
                    }
                    #return jsonify(res)
                    return render_template('jobs/appliances.html', job_appliances=res)
                else:
                    res = {
                        'job': {
                            'id': rows[0][2],
                            'name': rows[0][3],
                        },
                        'appliancers': []
                    }
                    return render_template('jobs/appliances.html', job_appliances=res)
            else:
                sql = text('SELECT * FROM jobs  WHERE jobs.id = {}'.format(id))
                row = engine.execute(sql).fetchone()
                res = {
                    'job': {
                        'id': row[0],
                        'name': row[1],
                    },
                    'appliancers': []
                }
                return render_template('jobs/appliances.html', job_appliances=res)
        else:
            return jsonify({'message': 'ID value is not correct'})
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

@app.route('/jobs/store/', methods=['POST'])
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
