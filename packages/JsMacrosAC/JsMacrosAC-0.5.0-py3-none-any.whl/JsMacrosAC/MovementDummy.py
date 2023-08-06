from .PlayerInput import *

class MovementDummy(LivingEntity, ):



    def __init__(player: self, ):
        pass


    def getCoordsHistory(self, ) -> list:
        pass

    def getInputs(self, ) -> list:
        pass

    def applyInput(self, input: PlayerInput, ) -> Vec3d:
        pass

    def method_26318(self, movementInput: Vec3d, f: float, ) -> Vec3d:
        pass

    def canMoveVoluntarily(self, ) -> bool:
        pass

    def setSprinting(self, sprinting: bool, ) -> None:
        pass

    def getMainHandStack(self, ) -> ItemStack:
        pass

    def getArmorItems(self, ) -> Iterable:
        pass

    def getEquippedStack(self, slot: EquipmentSlot, ) -> ItemStack:
        pass

    def equipStack(self, slot: EquipmentSlot, stack: ItemStack, ) -> None:
        pass

    def getMainArm(self, ) -> Arm:
        pass

    def clone(self, ) -> self:
        pass


    pass
