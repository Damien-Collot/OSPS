import os

pid = os.fork()

if pid == 0:
    os.environ['HOME'] = "rep1"
    #external_function()
else:
    os.environ['HOME'] = "rep2"
    #external_function()


from multiprocessing import Process

def f():
    os.environ['HOME'] = "rep1"
    #external_function()

if __name__ == '__main__':
    p = Process(target=f)
    p.start()
    os.environ['HOME'] = "rep2"
    #external_function()
    p.join()