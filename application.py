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
    connection_string='InstrumentationKey=31e9c92e-6f6c-43fe-a167-d34249265162')
)

tracer = Tracer(
    exporter=AzureExporter(
        connection_string='InstrumentationKey=31e9c92e-6f6c-43fe-a167-d34249265162'),
    sampler=ProbabilitySampler(1.0),
)

def findEmployee(lastName):
    lowercaseLastName = lastName.lower()
    matchingEmployees = []
    for e in testData:
        if (e['LastName'].lower().startswith(lowercaseLastName)):
            matchingEmployees.append(e)
    logger.info(f'[findEmployee] found {len(matchingEmployees)} records')
    return matchingEmployees

class Employees(Resource):
    def get(self):
        logger.info(f'[Employees] returning all data, {len(testData)} records')
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