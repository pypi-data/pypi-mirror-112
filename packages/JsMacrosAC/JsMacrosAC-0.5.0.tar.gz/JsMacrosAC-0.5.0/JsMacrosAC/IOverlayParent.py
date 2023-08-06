from .OverlayContainer import *
from .IContainerParent import *

class IOverlayParent(none, IContainerParent):



    def closeOverlay(self, overlay: OverlayContainer, ) -> None:
        pass

    def setFocused(self, focused: Element, ) -> None:
        pass

    def getChildOverlay(self, ) -> OverlayContainer:
        pass


    pass
