import importlib


def model_str(instance, attr) -> str:
    """
    The field to display for an object's __str__. If the field doesn't exist then an
    alternative will be displayed.
    :param instance:    Instance object
    :param attr:        Field name to get data from if it exists
    :return:            str
    """
    return hasattr(instance, attr) and getattr(instance, attr) \
           or f'<{instance.__class__.__name__}: {instance.id}>'


def modstr(instance, attr) -> str:
    """Alias for model_str()"""
    return model_str(instance, attr)


def classgrabber(dotpath: str):
    """
    Returns the class from a dot path that leads to the class to be imported.
    The class would be ready for use.
    Example:
        Settings = classgrabber('app.folder.file.Settings')
        # Settings class now ready for use
        myobj = Settings()
    :param dotpath:   A dot path
    :return:            class
    """
    x = dotpath.split('.')
    path = '.'.join(x[0:-1])
    models = importlib.import_module(path)
    return getattr(models, x[-1])