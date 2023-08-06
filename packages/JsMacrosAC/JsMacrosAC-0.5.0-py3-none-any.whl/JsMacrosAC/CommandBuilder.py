from .MethodWrapper import *

class CommandBuilder(Object, ):



    def __init__(name: str, ):
        pass


    def literalArg(self, name: str, ) -> self:
        pass

    def angleArg(self, name: str, ) -> self:
        pass

    def blockArg(self, name: str, ) -> self:
        pass

    def booleanArg(self, name: str, ) -> self:
        pass

    def colorArg(self, name: str, ) -> self:
        pass

    def doubleArg(self, name: str, ) -> self:
        pass

    def doubleArg(self, name: str, min: float, max: float, ) -> self:
        pass

    def floatRangeArg(self, name: str, ) -> self:
        pass

    def longArg(self, name: str, ) -> self:
        pass

    def longArg(self, name: str, min: long, max: long, ) -> self:
        pass

    def identifierArg(self, name: str, ) -> self:
        pass

    def intArg(self, name: str, ) -> self:
        pass

    def intArg(self, name: str, min: int, max: int, ) -> self:
        pass

    def intRangeArg(self, name: str, ) -> self:
        pass

    def itemArg(self, name: str, ) -> self:
        pass

    def nbtArg(self, name: str, ) -> self:
        pass

    def greedyStringArg(self, name: str, ) -> self:
        pass

    def quotedStringArg(self, name: str, ) -> self:
        pass

    def wordArg(self, name: str, ) -> self:
        pass

    def textArgType(self, name: str, ) -> self:
        pass

    def uuidArgType(self, name: str, ) -> self:
        pass

    def regexArgType(self, name: str, regex: str, flags: str, ) -> self:
        pass

    def executes(self, callback: MethodWrapper, ) -> self:
        pass

    def or(self, ) -> self:
        pass

    def or(self, argumentLevel: int, ) -> self:
        pass

    def register(self, ) -> None:
        pass


    pass
