import shelve


def load_workspace(db_path, external_namespace=None, allow_callables=False):
    """
    Load a saved workspace either by returning a dict or by inserting all variables directly into the enclosing \
    namespace.

    :param db_path: Path to the database file produced by WorkspaceSaver. Don't trust databases you didn't create!
    :type db_path: str
    :param external_namespace: A namespace. If globals() is used, the variables are inserted directly into the \
    enclosing namespace. Any other dict (including those returned by locals() and vars()) will be updated in place, \
    which will NOT change any namespace. If no argument is given, return a dict of the variables.
    :type external_namespace: dict or None
    :param allow_callables: Whether to allow callables (class and function definitions) to be loaded. Not recommended.
    :type allow_callables: bool
    :return: None if external_globals was specified, or a dictionary of the contents of the saved workspace.
    :rtype: None or dict
    """

    d = dict()

    with shelve.open(db_path) as db:
        if allow_callables:
            d.update(db)
        else:
            d.update({key: value for key, value in db.items() if not hasattr(value, '__call__')})

    if external_namespace:
        external_namespace.update(d)
    else:
        return d


class WorkspaceSaver:
    """
    Class which is able to save all variables in the given namespace. Only variables defined after the WorkspaceSaver \
    is instantiated will be saved (so that imports etc. are not saved).
    """
    def __init__(self, db_path, external_globals):
        """

        :param db_path: Path to the database file. Does not need to exist yet.
        :type db_path: str
        :param external_globals: A namespace (e.g. as created by globals()). locals() and vars() will not work because \
        they return copies of the namespace.
        :type external_globals: dict
        """
        self.db_path = db_path
        self.ignore = set(external_globals)
        self.ignore.add('db')
        self.external_namespace = external_globals

    def save(self, allow_callables=False):
        """
        Save any variables defined after the WorkspaceSaver was instantiated.

        :param allow_callables: Whether to allow callables (class and function definitions) to be saved.
        :type allow_callables: bool
        """
        globals_copy = dict(self.external_namespace)
        with shelve.open(self.db_path) as db:
            db.clear()
            for key, value in globals_copy.items():
                if key in self.ignore or value == self:
                    continue
                if not allow_callables and hasattr(value, '__call__'):
                    continue
                db[key] = value

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()
