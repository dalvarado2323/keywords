import random

def gernerar_contrasena(longitud):
    caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*_+"
    contrasena = ""
    for i in range(longitud):
        contrasena += random.choice(caracteres)
    return contrasena

longitud = int(input("Ingresa la longitud de la contraseña: "))

nueva_contrasena = gernerar_contrasena(longitud)
print("Tu nueva contraseña es:", nueva_contrasena)

