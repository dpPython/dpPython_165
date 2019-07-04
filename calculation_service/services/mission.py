from celery import Celery
from decimal import Decimal

from services import data_api
from services.models import Calculation
from .config import db

celery = Celery('tasks', broker='amqp://guest@localhost:5672')


@celery.task
def calculate_by_rules(project_id):
    calculation = Calculation()
    project_info = data_api.AccessToProjects.get(project_id)[0]
    data = project_info.get("data")
    contract = project_info.get("contract_id")
    rules = data_api.AccessToContracts.get(contract)[0]
    operands = []
    operator = rules.get('operator')
    for key in rules:
        name_field = rules.get(key)
        if name_field in data:
            operands.append(Decimal(data.get(name_field)))

    calculate = Decimal(eval(str(operands[0]) + operator + str(operands[1]) + "*" + str(rules.get('coefficient'))))
    db.session.add(calculation)
    db.session.commit()
    data_api.AccessToProjects.put(project_id, 'completed')
    return calculate
