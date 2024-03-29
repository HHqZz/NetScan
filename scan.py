import os
import socket    
import multiprocessing
import subprocess
import os


def pinger(job_q, results_q):
   
    DEVNULL = open(os.devnull, 'w')
    while True:

        ip = job_q.get()

        if ip is None:
            break

        try:
            subprocess.check_call(['ping', '-c1', ip],
                                  stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass


def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def map_network(pool_size=255):
    ip_list = list()
    ip_failed = list()
    ip_parts = get_my_ip().split('.')
    base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()
    pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)]
    for p in pool:
        p.start()
    for i in range(1, 255):
        jobs.put(base_ip + '{0}'.format(i))
    for p in pool:
        jobs.put(None)
    for p in pool:
        p.join()
   
    print('\n ----------------------------RESULTS-------------------------------')
    while not results.empty():
        ip = results.get()
        ip_list.append(ip)
	try:
		print(socket.gethostbyaddr(ip))
    
	except:
		ip_failed.append(ip)

    print('\n ---------------------------UNKNOWN IP--------------------------------')   
    for i in ip_failed:
	print(i)
    return ip_list


def main():
	print('Scanning...')
	lst = map_network()

if __name__ == '__main__':
	main()			

