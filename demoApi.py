from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_restful import reqparse
from data import testData

app = Flask(__name__)
api = Api(app)

def findEmployee(lastName):
    lowercaseLastName = lastName.lower()
    matchingEmployees = []
    for e in testData:
        if (e['LastName'].lower().startswith(lowercaseLastName)):
            matchingEmployees.append(e)
    return matchingEmployees

class Employees(Resource):
    def get(self):
        return jsonify(testData)

class EmployeesByLastName(Resource):
    def get(self, lastName):
        employees = findEmployee(lastName)
        if (len(employees) == 0):
            jsonify('{error: "Not found"'), 404
        else:
            return jsonify(employees)

api.add_resource(Employees, '/api/v1/employees')
api.add_resource(EmployeesByLastName, '/api/v1/employees/<string:lastName>')  

if __name__ == '__main__':
    app.run(debug=True)