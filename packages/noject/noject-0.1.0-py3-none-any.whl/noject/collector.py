class Collector:
    def __init__(self, formatter):
        self._formatter = formatter
        self._counter = 0
        self._params = dict()

    def get_params(self):
        return self._params
        
    def __call__(self, value):
        if callable(value):
            return value(self)
        param = f"param_{self._counter}"
        self._params[param] = value
        self._counter += 1
        return self._formatter(param)
