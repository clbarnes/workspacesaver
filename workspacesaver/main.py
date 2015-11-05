import shelve


def retrieve_workspace(db_path, external_globals):
    with shelve.open(db_path) as db:
        external_globals.update(db)


class WorkspaceSaver:
    def __init__(self, db_path, external_globals, allow_callables=False):
        self.db_path = db_path
        self.allow_callables = allow_callables
        self.ignore = set(external_globals)
        self.ignore.add('db')

    def save(self, external_globals):
        global_copy = dict(external_globals)
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
