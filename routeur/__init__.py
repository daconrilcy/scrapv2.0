import time
from controller import Controller
from events import Events
from interface import Fenetredefault
from routeur.routes import routes


class Router:
    controller = None
    interface = None
    event = None
    actionEnCours = None
    routes = None

    def __init__(self, event: Events, controller: Controller, interface: Fenetredefault):
        self.event = event
        self.controller = controller
        self.interface = interface
        self.routes = routes

    def actions(self):
        gostop = "start"
        while gostop != "stop":
            time.sleep(2)
            i = len(self.event.actions)
            if i > 0:
                act = self.event.actions[i - 1]
                if act['actionToDo'] == "quit":
                    gostop = "stop"
                else:
                    if self.routes[act['actionToDo']]:
                        if act['status'] == "start":
                            route = self.routes[act['actionToDo']]
                            moduleName = route['module']
                            actionToDo = route['action']
                            args = act['argus']
                            print('reoute :' + self.routes[act['actionToDo']]['action'])
                            module = self.__getattribute__(moduleName)
                            fn = module.__getattribute__(actionToDo)
                            if args:
                                fn(args)
                            else:
                                fn()
                            self.event.actions[i - 1]['status'] = "En cours"
