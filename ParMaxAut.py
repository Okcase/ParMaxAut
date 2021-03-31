
class Task:
    name = ""  # Nom de la tâche, unique.
    reads = []  # Domaine de lecture de la tâche
    writes = []  # Domaine d'écriture de la tâche
    run = None  # Fonction pour le comportement de la tâche


class TaskSystem:
    taskList = list()  # Liste des tâches
    dictionary = dict()  # Dictionnaire des tâches avec leurs dépendances

    def fillDict(self, taskList, dictionary):
        for i in range(len(taskList)):
            dictionary[taskList[i].name] = list()

    def getDependencies(self, task, dictionary):  # Retourne la liste des dépendances d'une tâche
        return dictionary[task.name]

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
                    dictionary[task1.name].append(task2.name)
                    dictionary[task2.name].append(task1.name)

    def dependencies(self, taskList, dictionary):  # Cherche toutes les dépendances entre les tâches
        for i in range(0, len(taskList) - 1):
            for j in range(1, len(taskList)):
                self.bernstein(taskList[i], taskList[j], dictionary)

    def run(self):
        print()


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


t1 = Task()
t1.name = "T1"
t1.writes = ["X"]
t1.run = runT1

t2 = Task()
t2.name = "T2"
t2.writes = ["Y"]
t2.run = runT2

tSomme = Task()
tSomme.name = "somme"
tSomme.reads = ["X", "Y"]
tSomme.writes = ["Z"]
tSomme.run = runTsomme

"""t1.run()
t2.run()
tSomme.run()
print(X)
print(Y)
print(Z)"""

s1 = TaskSystem()
s1.taskList = [t1, t2, tSomme]
s1.fillDict(s1.taskList, s1.dictionary)
#s1.dependencies(s1.taskList, s1.dictionary)
print(s1.dictionary)
