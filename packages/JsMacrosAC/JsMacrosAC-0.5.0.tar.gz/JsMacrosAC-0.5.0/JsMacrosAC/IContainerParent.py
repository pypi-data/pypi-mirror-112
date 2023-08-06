from .OverlayContainer import *
from .IOverlayParent import *

class IContainerParent(none, ):



    def addDrawableChild(self, drawableElement: T, ) -> T:
        pass

    def remove(self, button: Element, ) -> None:
        pass

    def openOverlay(self, overlay: OverlayContainer, ) -> None:
        pass

    def openOverlay(self, overlay: OverlayContainer, disableButtons: bool, ) -> None:
        pass

    def getFirstOverlayParent(self, ) -> IOverlayParent:
        pass


    pass
