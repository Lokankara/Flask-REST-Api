import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

db = SQLAlchemy()


class Result(db.Model):
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
    steps = db.relationship('Step', backref='test_record', lazy=True)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'historyId': self.historyid,
            'fullName': self.fullname,
            'labels': self.labels,
            'links': self.links,
            'name': self.name,
            'status': self.status,
            'statusDetails': self.statusdetails,
            'stage': self.stage,
            'steps': self.steps,
            'attachments': self.attachments,
            'parameters': self.parameters,
            'start': self.start,
            'stop': self.stop,
        }


class Step(db.Model):
    __tablename__ = 'test_steps'

    id = db.Column(db.Integer, primary_key=True)
    step_name = db.Column(db.String)
    step_description = db.Column(db.String)
    test_record_uuid = db.Column(db.UUID(as_uuid=True), db.ForeignKey('allure_tekg.uuid'))


class Container(db.Model):
    __tablename__ = 'containers'
    uuid = db.Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    children = db.Column(db.ARRAY(PG_UUID(as_uuid=True)), nullable=True)
    befores = db.Column(db.ARRAY(db.String), nullable=True)
    afters = db.Column(db.ARRAY(db.String), nullable=True)
    start = db.Column(db.BigInteger, nullable=False)
    stop = db.Column(db.BigInteger, nullable=False)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'children': self.children,
            'befores': self.befores,
            'afters': self.afters,
            'start': self.start,
            'stop': self.stop
        }
