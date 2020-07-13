class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


class Person(AttrDict):
    def __init__(self, name, prefs=[], married_to=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.original_prefs = prefs
        self.prefs = prefs
        self.married_to = married_to

    def __hash__(self):
        return self.name

    def __repr__(self):
        return str(self.name)

    def __eq__(self, other):
        return self.__str__() == str(other)

    def retrieve_most_preferred(self):
        if self.prefs:
            return self.prefs.pop(0)

    def get_more_preferred(self, obj):
        return self.original_prefs[:self.original_prefs.index(obj)]


class Man(Person):
    pass


class Woman(Person):
    def accepts(self, candidate):
        return self.prefs.index(candidate) < self.prefs.index(self.married_to)
