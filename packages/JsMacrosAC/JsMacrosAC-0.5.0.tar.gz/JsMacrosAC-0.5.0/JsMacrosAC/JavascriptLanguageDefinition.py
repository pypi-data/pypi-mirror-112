from .BaseLanguage import *
from .BaseEvent import *
from .JSScriptContext import *
from .BaseWrappedException import *
from .Core import *

class JavascriptLanguageDefinition(BaseLanguage, ):



    def __init__(extension: str, runner: Core, ):
        pass


    def wrapException(self, ex: Throwable, ) -> BaseWrappedException:
        pass

    def createContext(self, event: BaseEvent, ) -> JSScriptContext:
        pass


    pass
