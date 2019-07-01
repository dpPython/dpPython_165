import uuid

from flask import request
from flask_restful import Resource

from .models import Projects, Data
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

        logger.info(f'/projects GET (all_projects_count): {len(projects)}')

        return {'data': project_schema.dump(projects, many=True).data}

    def post(self):
        data = project_schema.load(request.json)[0]

        logger.info(f'/projects POST (data): {data}')

        project_name = data['name']
        contract_id = data['contract_id']
        new_project = Projects(name=project_name, contract_id=contract_id, status='default')

        logger.debug(f'/projects POST (write_data) {new_project}')

        with session() as db:
            db.add(new_project)

        return {'status': 'ok'}

    # def delete(self) :


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
        data = project_schema.load(request.json, partial=('contract_id',))[0]

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

        return {'status': 'deleted successfully'}


# /projects/<id>/status
class StatusUpdater(Resource):
    def put(self, id):
        data = project_schema.load(request.json, partial=('status',))[0]
        status = data['status']

        logger.info(f'/projects/<id>/status PUT (update_status) {status}')

        with session() as db:
            db.query(Projects).filter(Projects.id == id). \
                update({'status': status})

        return {'status': 'status_updated_successfully'}


# /projects/<id>/data/
class DataHandler(Resource):
    def post(self, id):
        data = data_schema.load(request.json)[0]

        logger.info(f'/projects/<id>/data POST (calculation data) {data}')

        with session() as db:
            for data in data['data']:
                data_about_room = Data(
                    project_id=uuid.UUID(id),
                    address=data['address'],
                    city=data['city'],
                    square=data['square'],
                    living_square=data['living_square'],
                    currency_value=data['price']['currency_value'],
                    currency=data['price']['currency'],
                    published_date=data['published_date'],
                    rooms=data['rooms'],
                    toilets=data['toilets']
                )
                db.add(data_about_room)

        return {'status': 'write_all_data'}

    # delete all data owned by project by project_id
    def delete(self, id):

        with session() as db:
            db.query(Data).filter(Data.project_id == id).\
                delete()

        return {'status': 'delete_successfully'}
