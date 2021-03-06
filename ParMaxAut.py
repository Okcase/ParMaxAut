
class Task:
    def __init__(self, name, reads, writes, run):
        self.name = name  # Nom de la tâche, unique.
        self.reads = reads  # Domaine de lecture de la tâche
        self.writes = writes  # Domaine d'écriture de la tâche
        self.run = run  # Fonction pour le comportement de la tâche


class TaskSystem:
    def __init__(self, taskList, dictionary):
        self.taskList = taskList  # Liste des tâches
        self.dictionary = dictionary  # Dictionnaire des tâches avec leurs dépendances
        self.voisins = dict()  # Dictionnaire de la matrice d'adjacence
        self.chemins = dict()  # Dictionnaire de la matrice des chemins

    def fillDict(self, dictionary):  # Remplit le dictionnaire avec la liste des tâches
        for i in range(len(self.taskList)):
            dictionary[self.taskList[i].name] = list()

    def getDependencies(self, task):  # Retourne la liste des dépendances d'une tâche
        if task not in self.dictionary:
            return None
        return self.dictionary[task.name]

    def bernstein(self, task1, task2):  # Evaluation des conditions de Bernstein
        for i in task1.writes:
            for j in task2.reads:
                if i == j:
                    return True
        for i in task1.reads:
            for j in task2.writes:
                if i == j:
                    return True
        for i in task1.writes:
            for j in task2.writes:
                if i == j:
                    return True
        return False

    def dependencies(self, dictionary):  # Cherche les interférences entre chaque tâche adjacente
        for i in self.taskList:
            tmp = self.getDependencies(i)
            if tmp is None:
                break
            else:
                for j in tmp:
                    for k in self.taskList:
                        if j == k.name:
                            if not self.bernstein(i, k):
                                dictionary[i.name].remove(j)

    def matriceVoisins(self):
        self.fillDict(self.voisins)
        for i in self.taskList:
            for j in self.dictionary:
                if i.name in self.dictionary[j]:
                    if j not in self.voisins[i.name]:
                        self.voisins[i.name].append(j)

    def matriceChemins(self):
        tmp = []
        for i in self.taskList:
            self.chemins[i.name] = self.getAdjacent(i.name, tmp)
            tmp = []

    def getAdjacent(self, task, tmp):
        for i in self.dictionary:
            if task in self.dictionary[i]:
                if i not in tmp:
                    self.getAdjacent(i, tmp)
                    tmp.append(i)
        return tmp

    def launchTask(self, liste):
        for i in self.taskList:
            if i not in liste:
                if self.getDependencies(i) is None:
                    i.run()
                    liste.append(i)
                    self.removeDependencie(i)
                    self.launchTask(liste)

    def removeDependencie(self, task):
        for i in self.dictionary:
            if self.dictionary[i] is None:
                break
            else:
                for j in self.dictionary[i]:
                    if task.name == j:
                        self.dictionary[i].remove(j)

    def run(self):
        self.matriceChemins()
        self.matriceVoisins()
        self.dependencies(self.chemins)
        self.dependencies(self.dictionary)
        done = []
        self.launchTask(done)


M1, M2, M3, M4, M5 = None, None, None, None, None


def runT1():
    global M1, M2, M3
    M1 = 1
    M2 = 2
    M3 = M1 + M2


def runT2():
    global M1, M4
    M4 = M1


def runT3():
    global M3, M4, M1
    M1 = M3 + M4


def runT4():
    global M3, M4, M5
    M5 = M3 + M4


def runT5():
    global M4, M2
    M2 = M4


def runT6():
    global M5
    M5 = M5


def runT7():
    global M1, M2, M4
    M4 = M1 + M2 + M4


def runT8():
    global M1, M3, M5
    M5 = M1 + M3


T1 = Task("T1", ["M1", "M2"], ["M3"], runT1)
T2 = Task("T2", ["M1"], ["M4"], runT2)
T3 = Task("T3", ["M3", "M4"], ["M1"], runT3)
T4 = Task("T4", ["M3", "M4"], ["M5"], runT4)
T5 = Task("T5", ["M4"], ["M2"], runT5)
T6 = Task("T6", ["M5"], ["M5"], runT6)
T7 = Task("T7", ["M1", "M2", "M4"], ["M4"], runT7)
T8 = Task("T8", ["M1", "M3"], ["M5"], runT8)

taches = [T1, T2, T3, T4, T5, T6, T7, T8]
dico = {"T8": ["T7"], "T7": ["T6", "T5"], "T5": ["T4", "T3"], "T6": ["T4"], "T3": ["T2"], "T4": ["T2"], "T2": ["T1"]}

system = TaskSystem(taches, dico)

system.run()

"""for a in system.chemins.items():
    print(a)

for b in system.voisins.items():
    print(b)"""

for c in system.dictionary.items():
    print(c)
