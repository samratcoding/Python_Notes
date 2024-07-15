from time import sleep
import multiprocessing

def fun1(number):
    for num in number:
        sleep(0.2)
        print('Fun 1 : ', num)
def fun2(number):
    for num in number:
        sleep(0.2)
        print('Fun 2 : ', num)


# Multi Processing
if __name__ == '__main__':
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    p1 = multiprocessing.Process(target=fun1, args=(lst,))
    p2 = multiprocessing.Process(target=fun2, args=(lst,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()



