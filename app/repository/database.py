class Database:

    def __init__(self, db):
        self.db = db
        self.db.create_all()
