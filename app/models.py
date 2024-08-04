from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class TestRecord(db.Model):
    __tablename__ = 'allure_tekg'

    uuid = db.Column(db.String, primary_key=True)
    historyid = db.Column(db.String)
    fullname = db.Column(db.String)
    labels = db.Column(db.JSON)
    name = db.Column(db.String)
    status = db.Column(db.String)
    statusdetails = db.Column(db.JSON)
    stage = db.Column(db.String)
    description = db.Column(db.String)
    steps = db.Column(db.JSON)
    attachments = db.Column(db.JSON)
    parameters = db.Column(db.JSON)
    start = db.Column(db.BigInteger)
    stop = db.Column(db.BigInteger)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'historyId': self.historyid,
            'fullName': self.fullname,
            'labels': self.labels,
            'name': self.name,
            'status': self.status,
            'statusDetails': self.statusdetails,
            'stage': self.stage,
            'description': self.description,
            'steps': self.steps,
            'attachments': self.attachments,
            'parameters': self.parameters,
            'start': self.start,
            'stop': self.stop,
        }
