class Env:
    """Environment to track variables."""
    def __init__(self, parent=None):
        self.parent = parent
        self.vars = set()

    def define_var(self, name):
        self.vars.add(name)

    def all_vars(self):
        result = set(self.vars)
        if self.parent:
            result |= self.parent.all_vars()
        return result
