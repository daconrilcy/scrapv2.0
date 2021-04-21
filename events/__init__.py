class Events:

    actions = []

    def __init__(self):
        print("init")

    def add(self, fromClass: str, actionToDo: str, argus=None):
        if isinstance(argus, str):
            st = argus
            argus = [st]
        todo = {"fromClass": fromClass, "actionToDo": actionToDo, "argus": argus, "status": "start"}
        self.actions.append(todo)
        self.affichAction(todo['actionToDo'], todo['argus'])
        return True

    def _qualifTodo(self, idTodo: int, status: str):
        if idTodo is None:
            return False
        if idTodo in self.actions.index:
            self.actions[idTodo]["status"] = status
            self.affichAction(status, arg=self.actions[idTodo]["argus"])
            return True

    def affichAction(self, todo, arg):
        argstr = " "
        if arg:
            for a in arg:
                argstr += str(a) + ", "

        print('addaction : ' + todo + argstr)
