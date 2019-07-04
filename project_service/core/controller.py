import uuid

from flask import request, abort, jsonify
from flask_restful import Resource

from .models import Projects, Data, db
from .utils.schemas import ProjectSchema, DataSchema
from .utils.session import session
from .utils.logger_creator import LoggerCreator

logger = LoggerCreator('controller', 'controller.log', '%(asctime)s - %(levelname)s - %(message)s').logger
project_schema = ProjectSchema()
data_schema = DataSchema()


# /projects
class ProjectsInitializer(Resource):
    def get(self):
        projects = Projects.query.all()
        if not projects:
            return {'message': 'There are no projects'}, 200

        logger.info(f'/projects GET (all_projects_count): {len(projects)}')

        return {'data': project_schema.dump(projects, many=True).data}, 200

    def post(self):
        data = project_schema.load(request.json)[0]
        if not data:
            abort(400)
            return {"message": "No input data provided"}, 400

        logger.info(f'/projects POST (data): {data}')

        project_name = data['name']
        contract_id = data['contract_id']
        new_project = Projects(name=project_name, contract_id=contract_id, status='default')

        logger.debug(f'/projects POST (write_data) {new_project}')

        with session() as db:
            db.add(new_project)

        return {'status': 'ok'}, 201


# /projects/<id>
class ProjectsResources(Resource):
    def get(self, id):
        project = Projects.query.filter_by(id=id).first()
        if not project:
            abort(404)
            return {"message": "No such project"}, 404

        return {
            'name': project.name,
            'contract_id': str(project.contract_id),
            'status': project.name
        }

    # update contract_id
    def put(self, id):
        data = project_schema.load(request.json, partial=('contract_id',))[0]
        if not data:
            abort(400)
            return {"message": "No input data provided"}, 400

        logger.info(f'/projects/<id> PUT (contract_id) {data}')

        contract_id = data['contract_id']

        with session() as db:
            db.query(Projects).filter(Projects.id == id). \
                update({'contract_id': contract_id})

        return {'status': 'updated'}

    def delete(self, id):
        logger.info(f'/projects/<id>/delete DELETE (project_id) {id}')

        with session() as db:
            db.query(Projects).filter(Projects.id == id). \
                delete()

        return {'status': 'deleted successfully'}, 200


# /projects/<id>/status
class StatusUpdater(Resource):
    def put(self, id):
        data = project_schema.load(request.json, partial=('status',))[0]
        if not data:
            abort(400)
            return {"message": "No input data provided"}, 400

        status = data['status']

        logger.info(f'/projects/<id>/status PUT (update_status) {status}')

        with session() as db:
            db.query(Projects).filter(Projects.id == id). \
                update({'status': status})

        return {'status': 'status_updated_successfully'}, 200


# /projects/<id>/data/
class DataHandler(Resource):
    def post(self, id):
        data = data_schema.load(request.json)[0]
        if not data:
            abort(400)
            return {"message": "No input data provided"}, 400

        logger.info(f'/projects/<id>/data POST (calculation data) {data}')

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

        return {'status': 'write_all_data'}, 201

    # delete all data owned by project by project_id
    def delete(self, id):

        with session() as db:
            db.query(Data).filter(Data.project_id == id).\
                delete()

        return {'status': 'deleted_successfully'}, 200


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
            db.query(Projects).filter(Projects.id == id).\
                update({'status': new_status})

        try:
            output_prj = project_schema.dump(_project).data
            output_data = data_schema.dump(_data).data
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


# /api/calc/status/<id>
class ProjectsCalcResult(Resource):
    def put(self, id):
        """
        Method to update project status data which are in calculation progress
        :param id: an id of the project
        """

        # deserialize input json
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400

        new_status = json_data["status"]

        project = Projects.query.filter_by(id=uuid.UUID(id)).first()
        if not project:
            return {"message": "Can't update - no such project"}, 404

        with session() as db:
            db.query(Projects).filter(Projects.id == id). \
                update({'status': new_status})

        return {"message": "Status succefully updated for {}".format(new_status)}, 200
