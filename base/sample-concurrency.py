# import threading
# '''
# 	state




# '''
# import multiprocessing

# def implementation_3():
#     process_1 = multiprocessing.Process(target=countdown)
#     process_2 = multiprocessing.Process(target=countdown)
#     process_1.start()
#     process_2.start()
#     process_1.join()
#     process_2.join()


# if __name__ == '__main__':
#     # freeze_support()
#     implementation_1()
#     implementation_2()
#     implementation_3()
from multiprocessing import Process, Manager
from time import sleep

def dothing(L, i):  # the managed list `L` passed explicitly.
    L[i]= i
    sleep(4)

if __name__ == "__main__":
    with Manager() as manager:
        L = manager.list(range(50))  # <-- can be shared between processes.
        processes = []
        for i in range(50):
            p = Process(target=dothing, args=(L,i))  # Passing the list
            p.start()
            processes.append(p)
        for p in processes:
            p.join()
        print(L)
