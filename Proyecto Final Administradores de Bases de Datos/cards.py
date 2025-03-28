def isValidCard(card):
    # Eliminar los espacios en caso de que haya
    card = card.replace(" ", "")
    
    # Verificar que el número de tarjeta sea numérico y tenga una longitud válida
    if not card.isdigit() or len(card) < 13 or len(card) > 19:
        return False
    
    # Aplicar el algoritmo de Luhn
    total = 0
    reversed_digits = card[::-1]
    
    for i, digit in enumerate(reversed_digits):
        n = int(digit)
        if i % 2 == 1:  # Si es un dígito en una posición impar (contando desde 0)
            n = n * 2
            if n > 9:
                n -= 9
        total += n
    
    # Si el total es múltiplo de 10, la tarjeta es válida
    return total % 10 == 0

def typeCard(numero):
    if not isValidCard(numero):
        return None
    
    numero = str(numero)
    
    # Verificar la longitud de la tarjeta
    longitud = len(numero)
    
    # Visa (empieza con 4, 13 o 16 dígitos)
    if numero[0] == '4' and (longitud == 13 or longitud == 16):
        return "visa"
    
    # MasterCard (empieza con 5 o 2, 16 dígitos)
    elif (numero[0] == '5' or numero[0] == '2') and longitud == 16:
        # Mejorar: Para MasterCard, considerar también los rangos 51-55 y 2221-2720
        if (numero[:2] in ['51', '52', '53', '54', '55']) or (2221 <= int(numero[:4]) <= 2720):
            return "mastercard"
    
    # American Express (empieza con 34 o 37, 15 dígitos)
    elif (numero[:2] == '34' or numero[:2] == '37') and longitud == 15:
        return "americanexpress"
    
    # Discover (empieza con 6, 16 dígitos)
    elif numero[0] == '6' and longitud == 16:
        return "discover"
    
    # Diners Club (empieza con 30, 36, 38 o 39, 14 dígitos)
    elif numero[:2] in ['30', '36', '38', '39'] and longitud == 14:
        return "dinersclub"
    
    # Si no es ninguna de las anteriores
    return None

# Ejemplo de uso
numero = input("Introduce el número de tarjeta de crédito para verificar: ")
tipo_tarjeta = typeCard(numero)

if isValidCard(numero):
    print("La tarjeta es válida.")
else:
    print("La tarjeta no es válida.")
print(f"El tipo de tarjeta es: {tipo_tarjeta}")
