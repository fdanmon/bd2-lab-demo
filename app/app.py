from flask import Flask
from flask import jsonify
import mysql.connector
import re

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

@app.route('/persons')
@app.route('/persons/all')
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
                el = {
                    'id': r[0],
                    'name': r[1],
                    'document_number': r[2],
                    'sex': r[3],
                    'birth_date': r[4],
                    'phone': r[5],
                    'rating': r[6]
                }
                res_json.append(el)
            return jsonify(res_json)
        else:
            return jsonify({'message': 'There are no results.'})
    except mysql.connector.Error as e:
        if cursor:
            cursor.close()
        return e

@app.route('/persons/get-skills/<id>')
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
                    el = {
                        'id': r[0],
                        'rating': r[3],
                        'person': {
                            'id': r[4],
                            'name': r[5],
                            'document_number': r[6],
                            'sex': r[7],
                            'birth_date': r[8],
                            'phone': r[9]
                        },
                        'skill': {
                            'id': r[11],
                            'title': r[13],
                            'category': {
                                'id': r[14],
                                'name': r[15]
                            }
                        }
                    }
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

@app.route('/persons/get-rating/<id>')
def get_rating_from_person(id=id):
    if id_regex.match(id):
        try:
            cursor = conn.cursor()
            query = ('SELECT persons.*, FORMAT(AVG(person_skills.rating), 2) FROM person_skills JOIN persons ON persons.id = person_skills.person_id WHERE person_skills.person_id = %(id)s GROUP BY person_skills.person_id')
            cursor.execute(query, {'id': id})
            r = cursor.fetchone()
            cursor.close()
            if r:
                el = {
                    'average_rating': r[7],
                    'person': {
                        'id': r[0],
                        'name': r[1],
                        'document_number': r[2],
                        'sex': r[3],
                        'birth_date': r[4],
                        'phone': r[5]
                    }
                }

                return jsonify(el)
            else:
                return jsonify({'message': 'There are no results.'})
        except mysql.connector.Error as e:
            if cursor:
                cursor.close()
            return e
    else:
        return jsonify({'message': 'Value is incorrect!'})

@app.route('/jobs')
@app.route('/jobs/all')
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
                d = {
                    'id': r[0],
                    'title': r[1],
                    'description': r[2],
                    'vacancies': r[3],
                    'category': {
                        'id': r[8],
                        'title': r[9]
                    },
                    'company': {
                        'id': r[10],
                        'name': r[12],
                        'document_number': r[13],
                        'rating': r[14],
                        'phone': r[15]
                    },
                    'expiration_date': r[6],
                    'status': r[7]
                }
                res_json.append(d)

            return jsonify(res_json)
        else:

            return jsonify({'message': 'There are no results'})
    except mysql.connector.Error as e:
        if cursor:
            cursor.close()
        return e