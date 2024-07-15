from time import sleep
import threading

def fun1(number):
    for num in number:
        sleep(0.5)
        print('Fun 1 : ', num)
def fun2(number):
    for num in number:
        sleep(0.5)
        print('Fun 2 : ', num)


# Multi Threading
lst = [1,2,3,4,5,6,7,8,9]

t1 = threading.Thread(target=fun1, args=(lst,))
t2 = threading.Thread(target=fun2, args=(lst,))

t1.start()
# t1.join()  this join hold this threding

t2.start()
# t12.join()  this join hold this threding

t1.join()
t2.join()