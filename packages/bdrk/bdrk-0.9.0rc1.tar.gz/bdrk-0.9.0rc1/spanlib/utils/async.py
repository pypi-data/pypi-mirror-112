class DeferredInit(type):
    def __new__(cls, name, bases, attrs):
        attrs["_restricted_fields"] = [attrs.get("has_many")]
        return type.__new__(cls, name, bases, attrs)

    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(DeferredInit, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
