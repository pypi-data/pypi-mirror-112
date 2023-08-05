from Freya_alerce.core.commands.base_freya import Base


class AddCatalogLocal(Base):
    """
    Add new catalogue in local folder.

    Parameters
    ----------
    name : (string) 
        name with add catalogue in local folder.
    source : (string) 
        origin source catalogue [api,db].
    """
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        super().create_module_catalog_local()