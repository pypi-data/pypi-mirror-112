from Freya_alerce.core.commands.base_api import BaseAPI


class NewAPI(BaseAPI):
    """
    Created new FreyaAPI.
    """
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        super().create_new_api()