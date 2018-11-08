import threading
import multiprocessing

def implementation_3():
    process_1 = multiprocessing.Process(target=countdown)
    process_2 = multiprocessing.Process(target=countdown)
    process_1.start()
    process_2.start()
    process_1.join()
    process_2.join()


if __name__ == '__main__':
    # freeze_support()
    implementation_1()
    implementation_2()
    implementation_3()
