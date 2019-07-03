# 1. Записати в стрічку філософію Пайтона
#     a. Знайти в заданій стрічці кількість входжень слів (better, never, is)
#     b. Вивести весь текст у верхньому регістрі (всі великі літери)
#     c. Замінити всі входження символу i на &
#
# 2. Задано чотирицифрове натуральне число.
#     a. Знайти добуток цифр цього числа.
#     b. Записати число в реверсному порядку.
#     c. Посортувати цифри, що входять в дане число
#
# 3. Поміняти між собою значення двох змінних, не використовуючи третьої змінної.

pep20 = '''Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!'''

print('1. Записати в стрічку філософію Пайтона' '\n',
      '1.a -- Знайти в заданій стрічці кількість входжень слів (better, never, is)')
count_better = pep20.count('better')
print("Кількість входжень 'better' -- ", count_better)

count_never = pep20.count('never')
print("Кількість входжень 'never' -- ", count_never)

count_is = pep20.count('is')
print("Кількість входжень 'is' -- ", count_is, '\n')

print('1.b -- Вивести весь текст у верхньому регістрі (всі великі літери)')
uppercase = pep20.upper()
print(uppercase, '\n')

print('1.c -- Замінити всі входження символу i на &')
replace = pep20.replace('i', '&')
print(replace, '\n')

print('2. Задано чотирицифрове натуральне число.', '\n' '2.a -- Знайти добуток цифр цього числа.')
number = 1638
x1 = number // 1000
x2 = number // 100 % 10
x3 = number // 10 % 10
x4 = number % 10
amount = x1 * x2 * x3 * x4
print(amount, '\n')

print('2.b. -- Записати число в реверсному порядку.')
print(x4, x3, x2, x1, '\n')

print('2.c. -- Посортувати цифри, що входять в дане число.')
sort = "".join(sorted(str(number)))
print(sort, '\n')

print('3. Поміняти між собою значення двох змінних, не використовуючи третьої змінної.')
a = 0
b = 1
print('a =', a, '|', 'b =', b)
a, b = b, a
print('a =', a, '|', 'b =', b)
