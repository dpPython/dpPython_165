import uuid

from flask import request, abort, jsonify
from flask_restful import Resource

from .models import Projects, Data
from .utils.schemas import ProjectSchema, DataSchema
from .utils.session import session

DATA = 0
project_schema = ProjectSchema()
data_schema = DataSchema()


# /projects
class ProjectsInitializer(Resource):
    def get(self):
        projects = Projects.query.all()
        return {'data': project_schema.dump(projects, many=True).data}

    def post(self):
        data = project_schema.load(request.json)[DATA]

        project_name = data['name']
        contract_id = data['contract_id']
        project = Projects(name=project_name, contract_id=contract_id, status='default')

        with session() as db:
            db.add(project)

        return {'id': project.id}


# /projects/<id>
class ProjectsResources(Resource):
    def get(self, id):
        project = Projects.query.filter_by(id=id).first()

        return {
            'name': project.name,
            'contract_id': str(project.contract_id),
            'status': project.name
        }

    # update contract_id
    def put(self, id):
        data = project_schema.load(request.json, partial=('contract_id',))[DATA]

        contract_id = data['contract_id']
        with session() as db:
            db.query(Projects).filter(Projects.id == id). \
                update({'contract_id': contract_id})

        return {'status': 'updated'}

    def delete(self, id):
        with session() as db:
            db.query(Projects).filter(Projects.id == id). \
                delete()

        return {'status': 'deleted successfully'}


# /projects/<id>/status
class StatusUpdater(Resource):
    def put(self, id):
        data = project_schema.load(request.json, partial=('status',))[DATA]
        status = data['status']

        with session() as db:
            db.query(Projects).filter(Projects.id == id). \
                update({'status': status})

        return {'status': 'status_updated_successfully'}


# /projects/<id>/data/
class DataHandler(Resource):
    def post(self, id):
        data = data_schema.load(request.json)[DATA]

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
                    field_10=data['field_10'],
                    field_11=data['field_11'],
                    field_12=data['field_12'],
                    field_13=data['field_13'],
                    field_14=data['field_14'],
                    field_15=data['field_15'],
                    field_16=data['field_16'],
                    field_17=data['field_17'],
                    field_18=data['field_18'],
                    field_19=data['field_19'],
                    field_20=data['field_20']
                )
                db.add(project_data)

        return {'status': 'write_data'}

    # delete all data owned by project by project_id
    def delete(self, id):
        with session() as db:
            db.query(Data).filter(Data.project_id == id). \
                delete()

        return {'status': 'deleted_successfully'}


# /projects/<id>/calc
class ProjectsCalc(Resource):

    def get(self, id):

        """
        Method to fetch data of the particular project for calculation
        :param id: an id of the project
        """
        _project = Projects.query.filter_by(id=uuid.UUID(id)).first()
        if not _project:
            abort(404)
            return {"message": "There is no such project"}, 404

        _id = str(_project.id)
        _data = Data.query.filter_by(id=uuid.UUID(_id))
        if not _data:
            abort(400)
            return {"message": "No input data provided"}, 400
        if not bool(_data):
            abort(400)
            return {"message": "Empty data"}, 400

        new_status = "calculation"
        with session() as db:
            db.query(Projects).filter(Projects.id == id). \
                update({'status': new_status})

        try:
            output_prj = project_schema.dump(_project).data
            output_data = data_schema.dump(_data).data
        except:
            abort(400)
            return {"message": "Something is wrong"}, 400
        return jsonify({"project": output_prj, "data": output_data}), 200

    def post(self, id):
        """
        Method to retrieve  calculated data of the particular project
        :param id: an id of the project
        """

        # obtain certain project
        _project = Projects.query.filter_by(id=uuid.UUID(id)).first()
        if not _project:
            abort(404)
            return {"message": "There is no such project"}, 404

        # deserialize input json
        entry_data = request.get_json()
        if not entry_data:
            return {"message": "No input data provided"}, 400
        result = entry_data["result"]
        return {"result": result}, 200
