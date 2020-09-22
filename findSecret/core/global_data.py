class GlobalData:
    def __init__(self):
        self.event_loop = None
        self.ws_connections = {}


g = GlobalData()
