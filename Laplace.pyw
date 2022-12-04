import sympy
from sympy import *


def laplace_transform_derivatives(e):
    """
    Evalua las transformadas de Laplace de derivadas de funciones sin evaluar.
    """
    if isinstance(e, sympy.LaplaceTransform):
        if isinstance(e.args[0], sympy.Derivative):
            d, t, s = e.args
            n = len(d.args) - 1
            return ((s**n) * sympy.LaplaceTransform(d.args[0], t, s) -
                    sum([s**(n-i) * sympy.diff(d.args[0], t, i-1).subs(t, 0)
                         for i in range(1, n+1)]))

    if isinstance(e, (sympy.Add, sympy.Mul)):
        t = type(e)
        return t(*[laplace_transform_derivatives(arg) for arg in e.args])

    return e


def ecuaciones_dif_laplace(A, B, C,c1,c2):
    # Ejemplo de transformada de Laplace
    # Defino las incognitas
    t = sympy.symbols("t", positive=True)
    y = sympy.Function("y")

    # Defino la ecuación
    edo = A*y(t).diff(t, t) + B*y(t).diff(t) + C*y(t)

    print("=============== PLANTEO DE ECUACION ===============\n")
    pprint(sympy.Eq(edo, 0))
    print("\n")

    # simbolos adicionales.
    s, Y = sympy.symbols("s, Y", real=True)
    

    # Calculo la transformada de Laplace ñ
    L_edo = sympy.laplace_transform(edo, t, s)
    sympy.Eq(L_edo, 0)

    # Aplicamos la nueva funcion para evaluar las transformadas de Laplace
    # de derivadas

    L_edo_2 = laplace_transform_derivatives(L_edo)
    sympy.Eq(L_edo_2, 0)

    # reemplazamos la transfomada de Laplace de y(t) por la incognita Y
    # para facilitar la lectura de la ecuación.
    L_edo_3 = L_edo_2.subs(sympy.laplace_transform(y(t), t, s), Y)
    sympy.Eq(L_edo_3, 0)

    # Definimos las condiciones iniciales
    ics = {y(0): c1, y(t).diff(t).subs(t, 0): c2}
    ics

    # Aplicamos las condiciones iniciales
    L_edo_4 = L_edo_3.subs(ics)
    print("=============== DESARROLLO DE ECUACION Y APLICACION DE CONDICIONES INICALES ===============\n")
    pprint(L_edo_4)
    print("\n")

    print("=============== APLICACION DE TRANSFORMADA DE LAPLACE ===============\n")
    Y_sol = sympy.solve(L_edo_4, Y)
    pprint(Y_sol)
    print("\n")


    print("============= CALCULANDO INVERSA DE LA TRANSFORMADA DE LAPLACE ========\n")

    y_sol = sympy.inverse_laplace_transform(Y_sol[0], s, t)
    print("Expresion en una sola linea:\n")
    pprint(str(y_sol))
    print("\n")
    print("Expresion algebraica:\n")
    pprint(y_sol)
    print("\n")



seguir = True
while (seguir == True):
    try:
        print("===========================================\n")
        print("Bienvenido al solucionador de Ecuaciones Diferenciales utilizando la Transformada de Laplace\n")
        print("La ecuacion a resolver tendra la forma:\n")
        print("Ay'' + By' + Cy = 0\n")
        print("Con A, B y C siendo numeros reales que ingresa el usuario\n")
        A = int(input("Por favor, ingrese A\n"))
        B = int(input("Por favor, ingrese B\n"))
        C = int(input("Por favor, ingrese C\n"))
        print("Ademas se necesitaran las condiciones inicales de y(0) Y /y'(0)\n")
        cond1 = int(input("Por favor, ingrese la condicion de y(0)= "))
        cond2 = int(input("Por favor, ingrese la condicion de y'(0)= "))

        ecuaciones_dif_laplace(A, B, C,cond1,cond2)
        print("Desea realizar otra ecuacion?\n")
        print("Ingrese 1 para SI")
        dec = int(input())
        if dec != 1:
            seguir = 0
            print("Gracias por usar el solucionador de Ecuaciones Diferenciales")
    except ValueError:
        print("============= ERROR ==========\n")
        print("Por favor ingrese numeros validos\n")
