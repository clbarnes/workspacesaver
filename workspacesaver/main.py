import shelve


def retrieve_workspace(db_path, external_globals, allow_callables=False):
    with shelve.open(db_path) as db:
        if allow_callables:
            external_globals.update(db)
        else:
            external_globals.update({key: value for key, value in db.items() if not hasattr(value, '__call__')})


class WorkspaceSaver:
    def __init__(self, db_path, external_globals, allow_callables=False):
        self.db_path = db_path
        self.allow_callables = allow_callables
        self.ignore = set(external_globals)
        self.ignore.add('db')
        self.external_globals = external_globals

    def save(self):
        global_copy = dict(self.external_globals)
        with shelve.open(self.db_path) as db:
            for key, value in global_copy.items():
                if key in self.ignore or value == self:
                    continue
                if not self.allow_callables and hasattr(value, '__call__'):
                    continue
                db[key] = value

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()
