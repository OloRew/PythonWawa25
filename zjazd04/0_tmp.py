a = input('Podaj liczbe:  ')
b = int(input('Podaj liczbe:  '))

try:
    wynik = a / b
except ZeroDivisionError:
    print('Nie mogę podzielić przez zero')
    print('przyjmuje wynik = 1')
    wynik = 1
except TypeError:
    wynik = int(a) / int(b)
    print('niepoprawny typ - zrzucam do int')

print(wynik)

