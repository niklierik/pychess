from actors.actor import Actor


class Scene:
    def __init__(self) -> None:
        self._actors: list[Actor] = []

    def init(self):
        for actor in self.actors:
            actor.init()

    @property
    def actors(self):
        return self._actors

    def loop(self):
        ...

    def render(self):
        ...
        
    def on_mouse_button_down(self, pos: tuple[int, int], button: int):
        ...
        

    def on_mouse_button_up(self,):
        ...

    def dispose(self):
        for actor in self.actors:
            actor.dispose()
