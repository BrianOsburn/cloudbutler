from jarvis_run import db

"""
Creates  the tables for the database
"""


#  Standard columns in each table
class Base(db.Model):
    __abstract__ = True

    record_number = db.Column(db.Integer, primary_key=True, autoincrement="auto", unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Users(Base):
    __tablename__ = 'users'

    slack_id = db.Column(db.String, nullable=False)
    slack_name = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)


class TicketQueue(Base):
    __tablename__ = 'ticketqueue'

    case_number = db.Column(db.String, nullable=False)
    req_uid = db.Column(db.String, nullable=False)
    req_uname = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    priority = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    casetype = db.Column(db.String)

    def __repr__(self):
        return "<TicketQueue(record_number='%s', date_created='%s', date_modified='%s', case_number='%s', " \
               "req_uid='%s', req_uname='%s', status='%s', priority='%s', description='%s', casetype='%s')>" % \
               (self.record_number, self.date_created, self.date_modified, self.case_number, self.req_uid,
                self.req_uname, self.status, self.priority, self.description, self.casetype)


class TicketDetails(Base):
    __tablename__ = 'ticketdetails'

    case_number = db.Column(db.String, nullable=False)
    event = db.Column(db.String, nullable=False)
    update_uid = db.Column(db.String, nullable=False)
    update_uname = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<TicketDetails(record_number='%s', date_created='%s', date_modified='%s', case_number='%s', " \
               "event='%s', update_uid='%s', update_uname='%s')>" % \
               (self.record_number, self.date_created, self.date_modified, self.case_number, self.event,
                self.update_uid, self.update_uname)














