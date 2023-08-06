from .BaseHelper import *
from .NBTNumberHelper import *
from .NBTCompoundHelper import *
from .NBTListHelper import *

class NBTElementHelper(BaseHelper, ):



    def getType(self, ) -> int:
        pass

    def isNull(self, ) -> bool:
        pass

    def isNumber(self, ) -> bool:
        pass

    def isString(self, ) -> bool:
        pass

    def isList(self, ) -> bool:
        pass

    def isCompound(self, ) -> bool:
        pass

    def asString(self, ) -> str:
        pass

    def asNumberHelper(self, ) -> NBTNumberHelper:
        pass

    def asListHelper(self, ) -> NBTListHelper:
        pass

    def asCompoundHelper(self, ) -> NBTCompoundHelper:
        pass

    def toString(self, ) -> str:
        pass

    def resolve(self, element: NbtElement, ) -> self:
        pass


    pass
