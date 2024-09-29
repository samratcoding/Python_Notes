import threading

def thread_task(name):
    print(f"Task {name} is running")

task = 10
i = 0
max_thread = 5
thread_gather = []
while i < task
    for i in range(max_thread):
        if i < task:
            thread = threading.Thread(target=thread_task, args=(i,))
            thread_gather.append(thread)
            thread_gather.start()
        else:
            print('All Task Appended')
            
for thread in thread_gather:
    thread.join()
