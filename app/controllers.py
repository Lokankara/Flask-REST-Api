from flask import Blueprint, jsonify, request, send_from_directory, render_template, abort

from logger import logger
from models import db, Result, Step, Container
from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/results', methods=['GET'])
def get_all_jsons():
    records = Result.query.all()
    return jsonify([record.to_dict() for record in records])


@main.route('/result', methods=['POST'])
def create_record():
    try:
        data = request.get_json()

        start_time = datetime.fromtimestamp(data.get('start') / 1000.0) if 'start' in data else None
        stop_time = datetime.fromtimestamp(data.get('stop') / 1000.0) if 'stop' in data else None

        new_record = Result(
            uuid=data.get('uuid'),
            historyid=data.get('historyId'),
            fullname=data.get('fullName'),
            labels=data.get('labels'),
            links=data.get('links'),
            name=data.get('name'),
            status=data.get('status'),
            statusdetails=data.get('statusDetails'),
            stage=data.get('stage'),
            start=start_time,
            stop=stop_time
        )

        steps_data = data.get('steps', [])
        for step in steps_data:
            step_obj = Step(
                step_name=step.get('stepName'),
                step_description=step.get('stepDescription'),
                test_record_uuid=new_record.uuid
            )
            new_record.steps.append(step_obj)

        db.session.add(new_record)
        db.session.commit()

        return jsonify({"message": "Record created", "uuid": new_record.uuid}), 201

    except Exception as e:
        logger.error(f"Error creating record: {e}")
        abort(500, description="Internal server error")


@main.route('/result/<uuid>', methods=['GET'])
def get_record(uuid):
    result = Result.query.get(uuid)
    if result:
        return jsonify(result.to_dict())
    else:
        abort(404, description="Result not found")


@main.route('/result/<uuid>', methods=['PUT'])
def update_record(uuid):
    data = request.json
    result = Result.query.get(uuid)
    if result:
        for key, value in data.items():
            setattr(result, key, value)
        db.session.commit()
        return jsonify(result.to_dict())
    else:
        abort(404, description="Result not found")


@main.route('/result/<uuid>', methods=['DELETE'])
def delete_record(uuid):
    try:
        record = Result.query.filter_by(uuid=uuid).first()
        if record is None:
            abort(404, description="Record not found")
        db.session.delete(record)
        db.session.commit()
        return jsonify({"message": "Record deleted"}), 200
    except Exception as e:
        logger.error(f"Error deleting record: {e}")
        abort(500, description="Internal server error")


@main.route('/containers', methods=['GET'])
def get_all_containers():
    containers = Container.query.all()
    return jsonify([container.to_dict() for container in containers])


@main.route('/container/<uuid>', methods=['GET'])
def get_container(uuid: str):

    container = Container.query.get(uuid)
    if container:
        return jsonify(container.to_json())
    else:
        abort(404, description="Container not found")


@main.route('/container', methods=['POST'])
def create_container():
    data = request.json
    container = Container(**data)
    db.session.add(container)
    db.session.commit()
    return jsonify(container.to_dict()), 201


@main.route('/container/<uuid>', methods=['PUT'])
def update_container(uuid: str):
    data = request.json
    container = Container.query.get(uuid)
    if container:
        for key, value in data.items():
            setattr(container, key, value)
        db.session.commit()
        return jsonify(container.to_dict())
    else:
        abort(404, description="Container not found")


@main.route('/containers/<uuid>', methods=['DELETE'])
def delete_container(uuid: str):
    container = Container.query.get(uuid)
    if container:
        db.session.delete(container)
        db.session.commit()
        return '', 204
    else:
        abort(404, description="Container not found")


@main.route('/attachments/<filename>')
def serve_image(filename):
    return send_from_directory('images', filename)


@main.route('/')
def serve_page():
    return render_template('index.html')
