import time


class Consola:

    def escribir(self, values):
        print(values)

    def recibir(self, textoarecibir):
        s = input(textoarecibir)
        return s


class Numeros:
    def sumar(self, *values):
        s = 0
        for argumento in values:
            s = s + argumento
        return s

    def restar(self, *values):
        s = 0
        for argumento in values:
            s = -argumento - s
        return s

    def multiplicar(self, *values):
        s = 1
        for argumento in values:
            s = s * argumento
        return s

    def dividir(self, arg1, arg2):
        s = arg1 / arg2

        return s


class Extras:

    def tiempo(self, *customtime):
        if not customtime:
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        else:
            return time.strftime(customtime[0], time.localtime())


consola = Consola()
numeros = Numeros()
extras = Extras()
