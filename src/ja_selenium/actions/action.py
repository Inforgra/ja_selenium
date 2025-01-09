class Action:

    def __init__(self):
        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def get_driver(self):
        return self.controller.get_driver()

    def get_state(self):
        return self.controller.get_state()

    def run(self):
        pass
