def number_generator(x, n):
    print('start progress...')
    if isinstance(x, int):
         return [x*num for num in range(1, n+1)]

print(number_generator(3,5))
