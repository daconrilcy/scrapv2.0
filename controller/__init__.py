from events import Events


class Controller:

    eventmanager = None

    def __init__(self, eventmanager: Events):
        self.eventmanager = eventmanager

    def action1(self, value):
        print(value * 2)
        self.eventmanager.add("controller", "render", "page2")

    def importbrand(self, arg: list):
        self.eventmanager.add("controller", "render", "pageimport")
        brandst = ""
        origin = arg[0][0]
        for b in arg[1]:
            brandst += b + ", "
        print("importation de : " + brandst)
