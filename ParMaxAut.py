import copy
from threading import Thread


class Task:
    def __init__(self, name, reads, writes, run):
        self.name = name  # Nom de la tâche, unique.
        self.reads = reads  # Domaine de lecture de la tâche
        self.writes = writes  # Domaine d'écriture de la tâche
        self.run = run  # Fonction pour le comportement de la tâche
        self.isRunning = False
        self.done = False

    def getTaskFromName(self, name):
        if self.name == name:
            return self
        else:
            return None

    def getInfoFromTask(self):
        return self.name, self.reads, self.writes


class TaskSystem:
    def __init__(self, taskList, dictionary):
        self.taskList = taskList  # Liste des tâches
        self.dictionary = dictionary  # Dictionnaire des tâches avec leurs dépendances

    """def fillDict(self, taskList, dictionary):  # Remplit le dictionnaire avec la liste des tâches
        for i in range(len(taskList)):
            dictionary[taskList[i].name] = list()"""

    def getDependencies(self, task):  # Retourne la liste des dépendances d'une tâche
        return self.dictionary[task.name]

    def bernstein(self, task1, task2):  # Evaluation des conditions de Bernstein
        for i in task1.writes:
            for j in task2.reads:
                if i == j:
                    #dictionary[task2.name].append(task1.name)
                    return True
        for i in task1.reads:
            for j in task2.writes:
                if i == j:
                    #dictionary[task1.name].append(task2.name)
                    return True
        for i in task1.writes:
            for j in task2.writes:
                if i == j:
                    return True
        return False
                    # dictionary[task1.name].append(task2.name)
                    # dictionary[task2.name].append(task1.name)

    def dependencies(self):  # Cherche toutes les dépendances entre les tâches
        #print(self.dictionary)
        for i in self.taskList:
            for j in self.dictionary[i.name]:
                for k in self.taskList:
                    if j == k.name:
                        #taskDep = k.getTaskFromName(j)
                        if not self.bernstein(i, k):
                            self.dictionary[i.name].remove(j)
        #print(self.dictionary)

    def run(self):
        self.dependencies()
        taskToDo = list()
        threadList = []
        for task in self.taskList:  # récupération des taches à faire
            if len(self.getDependencies(task)) == 0 and not task.done and not task.isRunning:
                taskToDo += task

        for task in taskToDo:  # Ajout des différents threads à faire, dans une liste
            t = Thread(target=task.run)
            task.isRunning = True
            threadList.append(t)

        for thread in threadList:
            thread.start()

        #
        # Ici, il faut pouvoir détecter lorsque le thread est fini et de mettre la tache en question en done
        #

        for task in self.taskList:
            if not task.done and not task.isRunning:
                self.run()



X = None
Y = None
Z = None
W = None


def runT1():
    global X
    X = 1
    return 1

def runT2():
    global Y
    Y = 2
    return 2

def runTsomme():
    global X, Y, Z
    Z = X + Y
    return 3

def runTmulti():
    global X, Y, W
    W = X * Y


t1 = Task("T1", [""], ["X"], runT1)
t2 = Task("T2", [""], ["Y"], runT2)
tSomme = Task("somme", ["X", "Y"], ["Z"], runTsomme)
tMulti = Task("multi", ["X", "Y"], ["W"], runTmulti)

"""t1.run()
t2.run()
tSomme.run()"""


s1 = TaskSystem([t1, t2, tSomme, tMulti], {"T1": [], "T2": ["T1"], "somme": ["T1", "T2"], "multi": ["T1", "T2"]})
print(s1.dictionary)
s1.run()
print("X =", X)
print("Y =", Y)
print("Z =", Z)
print("W =", W)
print(s1.dictionary)

for i in s1.taskList:
    print(i.done)
