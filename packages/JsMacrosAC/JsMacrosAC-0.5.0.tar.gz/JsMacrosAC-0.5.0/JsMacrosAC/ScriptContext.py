from .BaseEvent import *

class ScriptContext(Object, ):

    startTime: long = None


    def __init__(event: BaseEvent, ):
        pass


    def getContext(self, ) -> WeakReference:
        pass

    def getMainThread(self, ) -> WeakReference:
        pass

    def setMainThread(self, t: Thread, ) -> None:
        pass

    def getTriggeringEvent(self, ) -> BaseEvent:
        pass

    def setContext(self, context: T, ) -> None:
        pass

    def isContextClosed(self, ) -> bool:
        pass

    def closeContext(self, ) -> None:
        pass


    pass
