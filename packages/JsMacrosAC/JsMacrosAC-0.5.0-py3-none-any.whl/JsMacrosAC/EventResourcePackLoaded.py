from .BaseEvent import *

class EventResourcePackLoaded(Object, BaseEvent):

    isGameStart: bool = None
    loadedPacks: list = None


    def __init__(isGameStart: bool, ):
        pass


    def toString(self, ) -> str:
        pass


    pass
