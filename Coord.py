class Coord():
    dimensions = 'xyzt'

    def __init__(self, *args, **kwargs):
        self.value = args

    def __repr__(self):
        return f'coord: {self.value}'

    def __iter__(self):
        return iter(self.value)

    def __set__(self, __, value):
        self.value = value

    def __getitem__(self, key):
        return self.value[key]
    
    def __setitem__(self, key, value):
        self.value = self.value[:key] + (value,) + self.value[key + 1:]

    def __getattr__(self, name):
        if name in self.dimensions:
            i = self.dimensions.index(name)
            return self.value[i]
        else:
            raise ValueError
        
    def __setattr__(self, __name: str, __value):
        if __name == 'value':
            super().__setattr__(__name, __value)
        elif __name in self.dimensions:
            i = self.dimensions.index(__name)
            self.value = self.value[:i] + (__value,) + self.value[i + 1:]
        else:
            raise ValueError

    def __iadd__(self, other):
        return Coord(*(a + b for a, b in zip(self.value, other)))

    def __isub__(self, other):
        return Coord(*(a - b for a, b in zip(self.value, other)))

    def __add__(self, other):
        return Coord(*(a + b for a, b in zip(self.value, other)))