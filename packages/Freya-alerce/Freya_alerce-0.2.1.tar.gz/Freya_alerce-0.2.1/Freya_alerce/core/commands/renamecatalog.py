from Freya_alerce.core.commands.base_freya import Base

class RenameCatalog(Base):
    """
    Rename catalog inside Freya.

    Parameters
    ----------
    old_name : (string) 
        name catalog inside Freya.
    new_name : (string) 
        new name for catalog inside Freya.
    """
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        super().rename_catalog()