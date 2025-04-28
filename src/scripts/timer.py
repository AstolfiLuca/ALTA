import time
import multiprocessing
from functools import wraps
import sys

def realtimer(func):
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        elapsed_value = multiprocessing.Value('d', 0.0)  # 'd' = double
        
        stop_event = multiprocessing.Event()
        
        def update_timer():
            start_time = time.time()
            while not stop_event.is_set():
                with elapsed_value.get_lock():
                    elapsed_value.value = time.time() - start_time
                
                sys.stdout.write('\033[s')
                sys.stdout.write('\033[999;1H')
                sys.stdout.write(f'Tempo: {elapsed_value.value:.2f}s\033[K')
                sys.stdout.write('\033[u')
                sys.stdout.flush()
                time.sleep(0.1)

            sys.stdout.write('\033[s\033[999;1H\033[K\033[u')
            sys.stdout.flush()
        
        timer_process = multiprocessing.Process(target=update_timer)
        timer_process.start()
        
        try:
            func(*args, **kwargs)
        finally:
            stop_event.set()
            timer_process.join()
            print(f"\nTempo totale di esecuzione: {elapsed_value.value:.2f} secondi")
        
    
    return wrapper