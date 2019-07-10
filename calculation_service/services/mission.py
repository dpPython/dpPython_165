from celery import Celery
from decimal import Decimal

from services import data_api
from services.models import Calculation
from .config import db

celery = Celery('mission', broker='amqp://guest:guest@localhost:5672')



@celery.task
def calculate_by_rules(project_id):

    calculation = Calculation()
    project_info = data_api.AccessToProjects.get(project_id)
    data = project_info.get("data")
    contract = project_info.get("contract_id")
    rules = data_api.AccessToContracts.get(contract)
    operands = []
    operator = rules.get('operator')
    for key in rules:
        name_field = rules.get(key)
        if name_field in data:
            operands.append(Decimal(data.get(name_field)))

    expression = str(operands[0]) + operator + str(operands[1]) + "*" + str(rules.get('coefficient'))
    calculate = Decimal(eval(expression))
    db.session.add(calculation)
    db.session.commit()
    data_api.AccessToProjects.put(project_id, 'completed')
    return calculate
