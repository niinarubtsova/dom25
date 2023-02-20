from typing import Tuple, Union, Dict

from flask import Blueprint, jsonify, request, Response
from marshmallow import ValidationError

from builder import build_query
from models import BatchRequestSchema

main_bp = Blueprint('main', __name__)

#FILE_NAME = 'data/apache_logs.txt'


@main_bp.route("/perform_query", methods=['POST'])
def perform_query() -> Union[Response, Tuple[Response, int]]:
    # Принять запрос от пользователя
    data: Dict[str, Union[list[dict], str]] = request.json
    # Обработать запрос, лидировать значение
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


@main_bp.route('/ping', methods=['GET'])
def ping():
    return 'pong'
