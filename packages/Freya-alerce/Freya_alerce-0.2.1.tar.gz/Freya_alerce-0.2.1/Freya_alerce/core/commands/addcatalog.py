from Freya_alerce.core.commands.base_freya import Base


class AddCatalog(Base):
    """
    Add new catalogue inside Freya.

    Parameters
    ----------
    name : (string) 
        name with add catalogue inside Freya.
    source : (string) 
        origin source catalogue [api,db].
    """
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        super().create_module_catalog()