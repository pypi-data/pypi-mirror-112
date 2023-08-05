from Freya_alerce.core.commands.base_api import BaseAPI


class AddResource(BaseAPI):
    """
    Add resource to FreyaAPI, need call inside FreyaAPI.

    Parameters
    ----------
    name : (string) 
        name catalogue in Freya what adds resource in FreyaAPI.
    """
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        super().create_new_resource()