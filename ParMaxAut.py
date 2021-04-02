import copy
import threading


class Task:
    def __init__(self, name, reads, writes, run):
        self.name = name  # Nom de la tâche, unique.
        self.reads = reads  # Domaine de lecture de la tâche
        self.writes = writes  # Domaine d'écriture de la tâche
        self.run = run  # Fonction pour le comportement de la tâche
        self.done = False

    def getTaskFromName(self, name):
        if self.name == name:
            return self
        else:
            return None

    def getInfoFromTask(self):
        return self.name, self.reads, self.writes

    def removeTask(self):
        del(self)


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

    def getKey(self, val):
        for key, value in self.dictionary.items():
            for i in value:
                if val == i:
                    return key
        return None


    def run(self):
        self.dependencies()
        for i in self.taskList:
            if len(self.getDependencies(i)) == 0 and not i.done:
                i.run()
                i.done = True
                while self.getKey(i.name) is not None:
                    key = self.getKey(i.name)
                    self.dictionary[key].remove(i.name)

        for i in self.taskList:
            if not i.done:
                self.run()


        #dico = copy.deepcopy(self.dictionary)


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
