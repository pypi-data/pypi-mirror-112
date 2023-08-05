from Freya_alerce.core.commands.base_freya import Base

class DeleteCatalog(Base):
    """
    Delete catalog inside Freya

    Parameters
    ----------
    name : (string) 
        name of catalog to delete inside Freya.
    """
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        super().delete_catalog()