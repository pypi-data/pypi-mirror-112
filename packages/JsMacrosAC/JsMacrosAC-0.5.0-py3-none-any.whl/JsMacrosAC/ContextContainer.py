from .ScriptContext import *

class ContextContainer(Object, ):



    def __init__(ctx: ScriptContext, ):
        pass


    def isLocked(self, ) -> bool:
        pass

    def setLockThread(self, lockThread: Thread, ) -> None:
        pass

    def getCtx(self, ) -> ScriptContext:
        pass

    def getLockThread(self, ) -> Thread:
        pass

    def awaitLock(self, then: Runnable, ) -> None:
        pass

    def releaseLock(self, ) -> None:
        pass

    def toString(self, ) -> str:
        pass


    pass
