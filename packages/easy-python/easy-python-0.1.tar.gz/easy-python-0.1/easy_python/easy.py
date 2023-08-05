import time


class Consola:

    def escribir(self, values):
        print(values)

    def recibir(self, textoarecibir):
        s = input(textoarecibir)
        return s




class Extras:

    def tiempo(self, *customtime):
        if not customtime:
            return print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        else:
            return print(time.strftime(customtime[0], time.localtime()))

consola = Consola()
#numeros = Numeros()
extras = Extras()


# class Numeros:

#     def sumar(self, *values):
#         s = 0
#         for argumento in values:
#             s = s + argumento
#         return s
#     def restar(self,*values):

#         s = 0
#         for argumento in values:
#             s = s - -argumento
#         return s
#     def multiplicar(self, Ignorar=False, *values):
#         if not Ignorar:
#             if len(values) <= 1:
#                 return "Minimo debes multiplicar 2 numeros, si quieres desactivar esta alerta, pon al principio de la funcion True"
#         s = 1
#         for argumento in values:
#             s = s * argumento
#         return s

#     def dividir(self, arg1, arg2):
#         s = arg1 / arg2
#         return s