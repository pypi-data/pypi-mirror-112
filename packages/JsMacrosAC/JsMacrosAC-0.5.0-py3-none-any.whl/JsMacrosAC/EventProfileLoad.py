from .BaseProfile import *
from .BaseEvent import *

class EventProfileLoad(Object, BaseEvent):

    profileName: str = None


    def __init__(profile: BaseProfile, profileName: str, ):
        pass


    def toString(self, ) -> str:
        pass


    pass
