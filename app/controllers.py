from flask import Blueprint, jsonify, request, send_from_directory, render_template

from logger import logger
from models import db, TestRecord, TestStep
from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/results', methods=['GET'])
def get_all_jsons():
    records = TestRecord.query.all()
    return jsonify([record.to_dict() for record in records])


@main.route('/result', methods=['POST'])
def create_record():
    try:
        data = request.get_json()

        start_time = datetime.fromtimestamp(data.get('start') / 1000.0) if 'start' in data else None
        stop_time = datetime.fromtimestamp(data.get('stop') / 1000.0) if 'stop' in data else None

        new_record = TestRecord(
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
            step_obj = TestStep(
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
        return jsonify({"message": "Error creating record"}), 500


@main.route('/result/<uuid>', methods=['GET'])
def get_record(uuid):
    record = TestRecord.query.get_or_404(uuid)
    return jsonify(record.to_dict())


@main.route('/result/<uuid>', methods=['PUT'])
def update_record(uuid):
    data = request.json
    record = TestRecord.query.get_or_404(uuid)
    for key, value in data.items():
        setattr(record, key, value)
    db.session.commit()
    return jsonify({"message": "Record updated"})


@main.route('/result/<uuid>', methods=['DELETE'])
def delete_record(uuid):
    try:
        record = TestRecord.query.filter_by(uuid=uuid).first()
        if record is None:
            return jsonify({"message": "Record not found"}), 404
        db.session.delete(record)
        db.session.commit()
        return jsonify({"message": "Record deleted"}), 200
    except Exception as e:
        logger.error(f"Error deleting record: {e}")
        return jsonify({"message": "Internal server error"}), 500


@main.route('/attachments/<filename>')
def serve_image(filename):
    return send_from_directory('images', filename)


@main.route('/')
def serve_page():
    return render_template('index.html')
