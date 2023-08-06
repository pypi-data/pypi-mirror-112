from .collector import Collector


class Builder:
    def __init__(self, formatter=lambda p: f"%({p})s"):
        self._formatter = formatter

    def __call__(self, fragment):
        if isinstance(fragment, str):
            return fragment, dict()
        collector = Collector(self._formatter)
        return fragment(collector), collector.get_params()
