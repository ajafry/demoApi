from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_restful import reqparse
from data import testData
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger(__name__)
app = Flask(__name__)
api = Api(app)

logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey=659960ad-5acf-477b-80b4-d1f0436a3783')
)

tracer = Tracer(
    exporter=AzureExporter(
        connection_string='InstrumentationKey=659960ad-5acf-477b-80b4-d1f0436a3783'),
    sampler=ProbabilitySampler(1.0),
)

def findEmployee(lastName):
    print("### Entered findEmployee(lastName)")
    lowercaseLastName = lastName.lower()
    matchingEmployees = []
    for e in testData:
        if (e['LastName'].lower().startswith(lowercaseLastName)):
            matchingEmployees.append(e)
    logger.info(f'[findEmployee] found {len(matchingEmployees)} records')
    with tracer.span(name="test") as span:
        print(f'[Employees] returning all data, {len(testData)} records')
    return matchingEmployees

class Employees(Resource):
    print("### Entered Employees(lastName)")
    def get(self):
        logger.info(f'[Employees] returning all data, {len(testData)} records')
        with tracer.span(name="test") as span:
            print(f'[Employees] returning all data, {len(testData)} records')
        return jsonify(testData)

class EmployeesByLastName(Resource):
    print("### Entered EmployeesByLastName(lastName)")
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
