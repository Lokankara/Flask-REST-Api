from flask import Blueprint, jsonify, request, send_from_directory, render_template
from app.models import db, TestRecord

main = Blueprint('main', __name__)


@main.route('/jsons', methods=['GET'])
def get_all_jsons():
    records = TestRecord.query.all()
    return jsonify([record.to_dict() for record in records])


@main.route('/json', methods=['POST'])
def create_record():
    data = request.json
    new_record = TestRecord(**data)
    db.session.add(new_record)
    db.session.commit()
    return jsonify({"message": "Record created", "uuid": new_record.uuid}), 201


@main.route('/json/<uuid>', methods=['GET'])
def get_record(uuid):
    record = TestRecord.query.get_or_404(uuid)
    return jsonify(record.as_dict())


@main.route('/json/<uuid>', methods=['PUT'])
def update_record(uuid):
    data = request.json
    record = TestRecord.query.get_or_404(uuid)
    for key, value in data.items():
        setattr(record, key, value)
    db.session.commit()
    return jsonify({"message": "Record updated"})


@main.route('/json/<uuid>', methods=['DELETE'])
def delete_record(uuid):
    record = TestRecord.query.get_or_404(uuid)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Record deleted"})


@main.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory('images', filename)


@main.route('/')
def serve_page():
    return render_template('index.html')
