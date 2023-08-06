from .ICategoryTreeParent import *
from .Button import *
from .Scrollbar import *
from .MultiElementContainer import *

class CategoryTreeContainer(MultiElementContainer, ICategoryTreeParent):

    category: str = None
    scroll: Scrollbar = None
    children: list = None
    expandBtn: Button = None
    showBtn: Button = None
    isHead: bool = None
    topScroll: int = None
    btnHeight: int = None


    def __init__(x: int, y: int, width: int, height: int, textRenderer: TextRenderer, parent: ICategoryTreeParent, ):
        pass


    def addCategory(self, category: str, ) -> self:
        pass

    def selectCategory(self, category: str, ) -> None:
        pass

    def updateOffsets(self, ) -> None:
        pass

    def init(self, ) -> None:
        pass

    def onScrollbar(self, page: float, ) -> None:
        pass

    def render(self, matrices: MatrixStack, mouseX: int, mouseY: int, delta: float, ) -> None:
        pass


    pass
