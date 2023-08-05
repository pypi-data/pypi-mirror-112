
def catalog_decorator(cls):
    cls.fill_catalog()
    return cls
