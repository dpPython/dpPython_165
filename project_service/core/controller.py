from flask import jsonify, request
from flask_restful import Resource
import uuid

from .utils.schemas import ProjectSchema, DataSchema
from .models import Projects, Data, db
from .utils.session import session

project_schema = ProjectSchema()
data_schema = DataSchema()


# /api/projects
class ProjectsInitializer(Resource):
    def get(self):
        projects = Projects.query.all()
        return jsonify({'data': project_schema.dump(projects, many=True).data})

    def post(self):
        data = project_schema.load(request.json)[0]

        project_name = data['name']
        contract_id = data['contract_id']
        new_project = Projects(name=project_name, contract_id=contract_id, status='waiting_for_data')

        with session() as db:
            db.add(new_project)

        return jsonify({'status': 'ok'})


# /api/projects/<id>
class ProjectsResources(Resource):
    def get(self, id):
        project = Projects.query.filter_by(id=id).first()
        return jsonify(dict(id=id, name=project.name, contract_id=project.contract_id, status=project.name))

    # update contract_id
    def put(self, id):
        data = project_schema.load(request.json, partial=('contract_id',))[0]

        contract_id = data['contract_id']
        project = Projects.query.filter_by(id=id).first()
        project.contract_id = contract_id
        db.session.commit()

        return jsonify({'status': 'updated'})


# /api/projects/status/<id>
class StatusUpdater(Resource):
    def put(self, id):
        data = project_schema.load(request.json, partial=('status',))[0]

        new_status = data['status']
        project = Projects.query.filter_by(id=id).first()
        project.status = new_status
        db.session.commit()

        return jsonify({'status': 'updated'})


# /api/projects/data/<id>
class DataHandler(Resource):
    def post(self, id):
        data = data_schema.load(request.json)[0]

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
            db.session.add(data_about_room)
        db.session.commit()

        return jsonify({'status': 'write_all'})
