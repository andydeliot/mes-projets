from threading import Thread


class Threader(Thread):
    def __init__(self, code):
        """ code à paralleliser.
            start() pour démarrer.
            join() pour attendre la fin d'un Thread.
        """
        Thread.__init__(self)
        self.code = code

    def run(self):
        self.code()


if __name__ == "__main__":

    import random
    import sys
    import time

    def mon_code(lettre):
        i = 0
        while i < 20:
            sys.stdout.write(lettre)
            sys.stdout.flush()
            attente = 0.2
            attente += random.randint(1, 60) / 100
            time.sleep(attente)
            i += 1

    a = Threader(lambda: mon_code("1"))
    b = Threader(lambda: mon_code("2"))

    a.start()
    b.start()
    
    a.join()
    b.join()

    print("Terminé")
    
