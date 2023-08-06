
class BossBarConsumer(Object, BossBarS2CPacket$Consumer):



    def __init__():
        pass


    def add(self, uuid: UUID, name: str, percent: float, color: Color, style: Style, darkenSky: bool, dragonMusic: bool, thickenFog: bool, ) -> None:
        pass

    def remove(self, uuid: UUID, ) -> None:
        pass

    def updateProgress(self, uuid: UUID, percent: float, ) -> None:
        pass

    def updateName(self, uuid: UUID, name: str, ) -> None:
        pass

    def updateStyle(self, id: UUID, color: Color, style: Style, ) -> None:
        pass

    def updateProperties(self, uuid: UUID, darkenSky: bool, dragonMusic: bool, thickenFog: bool, ) -> None:
        pass


    pass
