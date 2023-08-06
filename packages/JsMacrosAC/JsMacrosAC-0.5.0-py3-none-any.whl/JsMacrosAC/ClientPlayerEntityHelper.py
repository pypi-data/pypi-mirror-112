from .PlayerEntityHelper import *
from .EntityHelper import *

class ClientPlayerEntityHelper(PlayerEntityHelper, ):



    def __init__(e: T, ):
        pass


    def lookAt(self, yaw: float, pitch: float, ) -> self:
        pass

    def lookAt(self, x: float, y: float, z: float, ) -> self:
        pass

    def attack(self, entity: EntityHelper, ) -> None:
        pass

    def attack(self, x: int, y: int, z: int, direction: int, ) -> None:
        pass

    def interact(self, entity: EntityHelper, offHand: bool, ) -> None:
        pass

    def interact(self, offHand: bool, ) -> None:
        pass

    def interact(self, x: int, y: int, z: int, direction: int, offHand: bool, ) -> None:
        pass

    def interact(self, ) -> None:
        pass

    def attack(self, ) -> None:
        pass

    def getFoodLevel(self, ) -> int:
        pass

    def toString(self, ) -> str:
        pass


    pass
