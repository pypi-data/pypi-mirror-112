from .BossBarHelper import *
from .BaseEvent import *

class EventBossbar(Object, BaseEvent):

    bossBar: BossBarHelper = None
    uuid: str = None
    type: str = None


    def __init__(type: str, uuid: UUID, bossBar: ClientBossBar, ):
        pass


    def toString(self, ) -> str:
        pass


    pass
