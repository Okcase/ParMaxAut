import copy


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

    def fillDict(self, taskList, dictionary):  # Remplit le dictionnaire avec la liste des tâches
        for i in range(len(taskList)):
            dictionary[taskList[i].name] = list()

    def getDependencies(self, task):  # Retourne la liste des dépendances d'une tâche
        return self.dictionary[task.name]

    def bernstein(self, task1, task2, dictionary):  # Evaluation des conditions de Bernstein
        for i in task1.writes:
            for j in task2.reads:
                if i == j:
                    dictionary[task2.name].append(task1.name)
        for i in task1.reads:
            for j in task2.writes:
                if i == j:
                    dictionary[task1.name].append(task2.name)
        for i in task1.writes:
            for j in task2.writes:
                if i == j:
                    pass
                    # dictionary[task1.name].append(task2.name)
                    # dictionary[task2.name].append(task1.name)

    def dependencies(self, dictionary):  # Cherche toutes les dépendances entre les tâches
        for i in range(0, len(self.taskList) - 1):
            for j in range(1, len(self.taskList)):
                self.bernstein(self.taskList[i], self.taskList[j], dictionary)

    def run(self):
        self.dependencies(self.dictionary)
        dico = copy.deepcopy(self.dictionary)


X = None
Y = None
Z = None


def runT1():
    global X
    X = 1


def runT2():
    global Y
    Y = 2


def runTsomme():
    global X, Y, Z
    Z = X + Y


t1 = Task("T1", [""], ["X"], runT1)
"""t1.name = "T1"
t1.writes = ["X"]
t1.run = runT1"""

t2 = Task("T2", [""], ["Y"], runT2)
"""t2.name = "T2"
t2.writes = ["Y"]
t2.run = runT2"""

tSomme = Task("somme", ["X", "Y"], ["Z"], runTsomme)
"""tSomme.name = "somme"
tSomme.reads = ["X", "Y"]
tSomme.writes = ["Z"]
tSomme.run = runTsomme"""

"""t1.run()
t2.run()
tSomme.run()
print(X)
print(Y)
print(Z)"""

s1 = TaskSystem([t1, t2, tSomme], {"T1": [], "T2": ["T1"], "somme": ["T1", "T2"]})
# s1.dependencies(s1.taskList, s1.dictionary)
print(s1.dictionary)
