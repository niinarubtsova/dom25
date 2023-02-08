from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from builder import build_query
from models import BatchRequestSchema

main_bp = Blueprint('main', __name__)

#FILE_NAME = 'data/apache_logs.txt'


@main_bp.route("/perform_query", methods=['POST'])
def perform_query():
    # Принять запрос от пользователя
    data = request.json
    # Обработать запрос, валидировать значение
    try:
        validated_data = BatchRequestSchema().load(data)
    except ValidationError as error:
        return jsonify(error.messages), 400
    # Выполнить запрос
    result = None
    for query in validated_data['queries']:
        result = build_query(
            cmd=query['cmd'],
            value=query['value'],
            file_name=validated_data['file_name'],
            data=result,
        )

    return jsonify(result)
