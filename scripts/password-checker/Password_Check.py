import re
import argparse

## Aqui van las reglas de política


MIN_LENGTH  = 8
STRONGTH_LENGTH = 12
REQUIRE_UPPER = True
REQUIRE_LOWER = True
REQUIRE_DIGIT = True
REQUIRE_SPECIAL = True

SPECIAL_CHARS = r'!@#$%^&*(),.?:{}|<>\[\]\\_\-;`~+='


## A continuaci´on, se listan en un diciconario las contraseñas comunes que NO
## Ddeben de usarse

COMMON_PWSD = [
    "password", "123", "123456", "password123", "admin", "letmein", "qwerty", 
    "abc123", "monkey", "123456789", "welcome", "login", "pass", "master", "hello", 
    "hola", "root"
]






## Aqui viene la funcion principal del códgio, toda la lógica


def analyze_password ( password: str)-> dict:
    ## Va a analizar una contraseña y va a devolver un dict con lo siguiente:
    ## SCORE, LEVEL, PASSED O FAILED

    passed = []
    failed = []
    score = 0


    ## Ahora, esto es la Longituf minima que deberia de tener
    if len(password) >= MIN_LENGTH:
        passed.append(f"Longitud minima ({MIN_LENGTH} CHARS)")
        score += 20
    else:
        failed.append (f"Longitud minima: se necesita de al menos {MIN_LENGTH} y (tiene {len(password)})")

    ## Ahora si la longitud es fuerte
    if len(password) >= STRONGTH_LENGTH:
        passed.append(f"Longitud fuerte ({STRONGTH_LENGTH} +chars)")
        score += 10

    ## Si tiene mayusculas
    if REQUIRE_UPPER:
        if re.search(r'[A-Z]', password):
            passed.append("Contiene mayusculas")
            score += 20
        else:
            failed.append("Fatan al menos una mayuscula en la contraseña")

    ## Si tiene minusculas
    if REQUIRE_LOWER:
        if re.search(r'[a-z]', password):
            passed.append("Contiene minúsculas")
            score += 15
        else:
            failed.append("Faltan al menos una minsucula en la contraseña")
    
    ## Si tiene numeros
    if REQUIRE_DIGIT:
        if re.search(r'\d', password):
            passed.append("Contiene números")
            score += 15
        else:
            failed.append("Falta al menos un numero en la contraseña")


    ## Si tiene aracteres especiales
    if REQUIRE_SPECIAL:
        if re.search(r'[!@#$%^&*(),.?:{}|<>\[\]\\_\-;`~+=]', password):
            passed.append("Contiene caracetres especiales")
            score += 20
        else:
            failed.append(f"Falta al menos un caracter especial en la contraseña")

    ## DEscartar que se sea una de las comunes ya mencionadas arriba
    if password.lower() in COMMON_PWSD:
        failed.append("Es una de las contraseñas que estan marcadas como comunes")
        score = min(score, 10 )
    else:
        passed.append("NO está en la lista prohibida")

    



    ## Determina el nivel de la pswd

    if score >= 80:
        level = "FUERTE"
    elif score >= 50:
        level = "MEDIO"
    else:
        level = "DEBIL"


    return {
        "password" : password,
        "score" : score, 
        "level" : level,
        "passed" : passed,
        "failed" : failed
    }









##AHora, en esta parte se mostraran los resultados en la pantalla del user

def print_result(result:dict, show_password:bool = True):
    """Imprime el resultado"""
    print("\n" + "=" * 50)

    if show_password:
        print(f"Contraseña: {result['password']}")


    print(f"  Puntaje    : {result['score']}/100")
    print(f"  Nivel      : {result['level']}")


    if result["passed"]:
        print("\n  Cumple:")
        for item in result["passed"]:
            print(f"     - {item}")

    if result["failed"]:
        print("\n  No cumple:")
        for item in result["failed"]:
            print(f"     - {item}")

    print("=" * 50)







## Entrada

def main ():
    parser = argparse.ArgumentParser(
        description="PASSWORD POLICY CHECKER "
    )
    parser.add_argument(
        "-p", "--password",
        help="Analiza una contraseña directamente"
    )
    

    args = parser.parse_args()

    # Si no pasaste nada → modo interactivo
    if not args.password:
        print("\n[Password Policy Checker]")
        pwd = input("Ingresa una contraseña para analizar: ")
        result = analyze_password(pwd)
        print_result(result)
        return

    # Si pasaste -p → analiza esa contraseña
    result = analyze_password(args.password)
    print_result(result)


if __name__ == "__main__":
    main()