import datetime

def datetime_serializer(obj):
    """Used for serializing objects with datetime types."""
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError(f"Type not serializable: {type(obj)}")
