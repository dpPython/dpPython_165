import uuid

from flask import request, abort, jsonify
from flask_restful import Resource

from .models import Projects, Data
from .utils.schemas import ProjectSchema, DataSchema, StatusSchema
from .utils.session import session

DATA = 0
ERRORS = 1
project_schema = ProjectSchema()
data_schema = DataSchema()
status_schema = StatusSchema()


# /projects
class ProjectsInitializer(Resource):
    def get(self):
        projects = Projects.query.all()
        return {'data': project_schema.dump(projects, many=True).data}, 200

    def post(self):
        input_request = project_schema.load(request.json)

        data = input_request[DATA]
        errors = input_request[ERRORS]

        if errors:
            abort(404, 'not enough data')

        project_name = data['name']
        contract_id = data['contract_id']
        project = Projects(name=project_name, contract_id=contract_id, status='default')
        print(project.id)

        with session() as db:
            db.add(project)
            project_id = db.query(Projects).filter(Projects.contract_id == contract_id).first()

            return {'status': 'create_successfully', 'id': str(project_id)}, 201


# /projects/<id>
class ProjectsResources(Resource):
    def get(self, id):
        project = Projects.query.filter_by(id=id).first()

        if not project:
            abort(404, "No such project")

        return {
            'name': project.name,
            'contract_id': str(project.contract_id),
            'status': project.name
        }, 200

    # update contract_id
    def put(self, id):
        input_requset = project_schema.load(request.json)

        data = input_requset[DATA]
        errors = input_requset[ERRORS]

        if errors:
            abort(404, 'error')

        contract_id = data['contract_id']
        with session() as db:
            db.query(Projects).filter(Projects.id == id). \
                update({'contract_id': contract_id})

        return {'status': 'updated'}, 200

    def delete(self, id):
        with session() as db:
            db.query(Projects).filter(Projects.id == id). \
                delete()

        return {'status': 'deleted successfully'}, 200


# /projects/<id>/status
class StatusUpdater(Resource):
    def put(self, id):
        request_data = status_schema.load(request.json)

        data = request_data[DATA]
        errors = request_data[ERRORS]

        if errors:
            abort(404, 'invalid status')

        status = data['status']
        with session() as db:
            db.query(Projects).filter(Projects.id == id). \
                update({'status': status})

        return {'status': 'status_updated_successfully'}, 200


# /projects/<id>/data/
class DataHandler(Resource):
    def post(self, id):
        request_data = data_schema.load(request.json)

        data = request_data[DATA]
        errors = request_data[ERRORS]

        if errors:
            abort(404, 'Invalid data')

        with session() as db:
            for data in data['data']:
                project_data = Data(
                    project_id=uuid.UUID(id),
                    field_1=data['field_1'],
                    field_2=data['field_2'],
                    field_3=data['field_3'],
                    field_4=data['field_4'],
                    field_5=data['field_5'],
                    field_6=data['field_6'],
                    field_7=data['field_7'],
                    field_8=data['field_8'],
                    field_9=data['field_9'],
                    field_10=data['field_10']
                )
                db.add(project_data)

        return {'status': 'write_all_data'}, 201

    # delete all data owned by project by project_id
    def delete(self, id):
        with session() as db:
            db.query(Data).filter(Data.project_id == id). \
                delete()

        return {'status': 'deleted_successfully'}, 200


# /projects/<id>/calc
class ProjectsCalc(Resource):

    def get(self, id):

        """
        Method to fetch data of the particular project for calculation
        :param id: an id of the project
        """
        project = Projects.query.filter_by(id=uuid.UUID(id)).first()
        if not project:
            abort(404)
            return {"message": "There is no such project"}, 404

        id = str(project.id)
        data = Data.query.filter_by(id=uuid.UUID(id))
        if not data:
            abort(400)
            return {"message": "No input data provided"}, 400
        if not bool(data):
            abort(400)
            return {"message": "Empty data"}, 400

        new_status = "calculation"
        with session() as db:
            db.query(Projects).filter(Projects.id == id). \
                update({'status': new_status})

        try:
            output_prj = project_schema.dump(project).data
            output_data = data_schema.dump(data).data
        except KeyError:
            abort(400)
            return {"message": "Something is wrong"}, 400
        return jsonify({"project": output_prj, "data": output_data}), 200

    def post(self, id):
        """
        Method to retrieve  calculated data of the particular project
        :param id: an id of the project
        """

        # obtain certain project
        project = Projects.query.filter_by(id=uuid.UUID(id)).first()
        if not project:
            abort(404)
            return {"message": "There is no such project"}, 404

        # deserialize input json
        entry_data = request.get_json()
        if not entry_data:
            return {"message": "No input data provided"}, 400
        result = entry_data["result"]
        return {"result": result}, 200
