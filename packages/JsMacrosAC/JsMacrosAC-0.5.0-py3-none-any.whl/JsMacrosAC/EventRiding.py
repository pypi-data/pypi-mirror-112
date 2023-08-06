from .BaseEvent import *
from .EntityHelper import *

class EventRiding(Object, BaseEvent):

    state: bool = None
    entity: EntityHelper = None


    def __init__(state: bool, entity: Entity, ):
        pass


    def toString(self, ) -> str:
        pass


    pass
