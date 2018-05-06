# import matplotlib.pyplot as plt
# p = int(input('Введите p: '))
# k = int(input('Введите k: '))
# def f(a, b ):
#     current = 0
#     x = []
#     fx = []
#     for _ in range(a ** b):
#         x.append(current)
#         current = (current - 1) % a**b
#         # current = (2 * current ** 2 + 3 * current + 5) % a**b
#         fx.append(current)
#     return [x, fx]
# r = f(p,k)
# print(r)
# plt.plot(r[0],r[1],'ro')
# plt.show()

x = 2
y = eval('[x + 2]')
print(x + y)
