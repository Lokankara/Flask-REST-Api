from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect
from config import Config
import logging

db = SQLAlchemy()
inspector = inspect(create_engine(Config.SQLALCHEMY_DATABASE_URI))
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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


logger.info(inspector.get_table_names())

columns = inspector.get_columns('allure_tekg')
for column in columns:
    logger.info(column)
