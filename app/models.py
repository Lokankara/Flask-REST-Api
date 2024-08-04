from flask_sqlalchemy import SQLAlchemy
import uuid
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

db = SQLAlchemy()

class TestRecord(db.Model):
    __tablename__ = 'allure_tekg'

    uuid = db.Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    historyid = db.Column(db.String)
    fullname = db.Column(db.String)
    links = db.Column(db.JSON)
    labels = db.Column(db.JSON)
    name = db.Column(db.String)
    status = db.Column(db.String)
    statusdetails = db.Column(db.JSON)
    stage = db.Column(db.String)
    attachments = db.Column(db.JSON)
    parameters = db.Column(db.JSON)
    start = db.Column(db.DateTime)
    stop = db.Column(db.DateTime)
    steps = db.relationship('TestStep', backref='test_record', lazy=True)

class TestStep(db.Model):
    __tablename__ = 'test_steps'

    id = db.Column(db.Integer, primary_key=True)
    step_name = db.Column(db.String)
    step_description = db.Column(db.String)
    test_record_uuid = db.Column(db.UUID(as_uuid=True), db.ForeignKey('allure_tekg.uuid'))

