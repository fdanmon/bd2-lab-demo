from flask import Flask
from flask import jsonify
import mysql.connector
import re
from controllers.personhandler import PersonHandler
from controllers.jobhandler import JobHandler

id_regex = re.compile("^[1-9]+[0-9]*$")

app = Flask(__name__)
conn = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='bd2_labs',
    user='root',
    password='bd2_labs_pass'
)

@app.route('/')
def index():
    return jsonify({
        'message': 'Hello world!'
    })

@app.route('/persons/info/')
@app.route('/persons/info/all/')
def get_persons():
    try:
        cursor = conn.cursor()
        query = ('SELECT * FROM persons')
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        if results and len(results) > 0:
            res_json = []
            for r in results:
                el = PersonHandler.parse_info(r)
                res_json.append(el)
            return jsonify(res_json)
        else:
            return jsonify({'message': 'There are no results.'})
    except mysql.connector.Error as e:
        if cursor:
            cursor.close()
        return e

@app.route('/persons/info/<id>/')
def get_person(id=id):
    if id_regex.match(id):
        try:
            cursor = conn.cursor()
            query = ('SELECT * FROM persons WHERE id = %(id)s')
            cursor.execute(query, {'id': id})
            result = cursor.fetchone()
            cursor.close()
            if result:
                el = PersonHandler.parse_info(result)
                return jsonify(el)
            else:
                return jsonify({'message': 'There are no results.'})
        except mysql.connector.Error as e:
            if cursor:
                cursor.close()
            return e
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

@app.route('/jobs/')
@app.route('/jobs/all/')
def get_jobs():
    try:
        cursor = conn.cursor()
        query = ('SELECT * FROM jobs JOIN categories ON jobs.category_id = categories.id JOIN companies ON jobs.company_id = companies.id')
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        if results and len(results) > 0:
            res_json = []
            for r in results:
                d = JobHandler.parse_job_info(r)
                res_json.append(d)
            return jsonify(res_json)
        else:

            return jsonify({'message': 'There are no results'})
    except mysql.connector.Error as e:
        if cursor:
            cursor.close()
        return e