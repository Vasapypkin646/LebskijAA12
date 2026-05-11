# bad_code.py
def f(x,y):
    # Сложение чисел
    z=x+y
    return z

def calc(a,b,c):
    # Какая-то сложная логика
    res1=a*b
    res2=res1+c
    res3=res2/2
    # TODO: Добавить обработку
    return res3

# Глобальная переменная
g=100

def process(lst):
    # Обработка списка
    res=[]
    for i in range(len(lst)):
        if lst[i]%2==0:
            res.append(lst[i]*2)
        else:
            res.append(lst[i]*3)
    return res

def get_user(id):
    # Получение пользователя (заглушка)
    if id==1:
        return "Alice"
    elif id==2:
        return "Bob"
    else:
        return None