import threading
import time
import os, subprocess
import argparse
import platform
import multiprocessing

SINGLE_THREAD = 0
MULTI_THREAD = 1


def wget(name, link):

    if platform.system() == 'Windows':
        cmd = f'powershell -c "Invoke-WebRequest -Uri "{link}" -OutFile "{link.split("/")[-1]}" 2>&1'
    else:
        cmd = f'wget {link} > /dev/null 2>&1 &'

    # os.system(cmd)
    subprocess.call(cmd, shell=True)
    print(name, '->', 'done')


if __name__ == "__main__":

    # get argument
    parser = argparse.ArgumentParser()
    parser.add_argument('--thread_mode', type=int)
    mode = parser.parse_args().thread_mode

    links = ['http://www.ubicomp.org/ubicomp2003/adjunct_proceedings/proceedings.pdf',
            'https://www.hq.nasa.gov/alsj/a17/A17_FlightPlan.pdf',
            'https://ars.els-cdn.com/content/image/1-s2.0-S0140673617321293-mmc1.pdf',
            'http://www.visitgreece.gr/deployedFiles/StaticFiles/maps/Peloponnese_map.pdf']

    start = time.time()

    if mode == SINGLE_THREAD:
        print('Mode: Single Threaded')
        for i, l in enumerate(links):
            wget('file' + str(i + 1), l)
    elif mode == MULTI_THREAD:

        print('Mode: Multi Threaded')
        cpu = multiprocessing.cpu_count()  # get the number fo CPUs

        for x in range(0, len(links), cpu):
            threads = []

            # create and run threads
            for i, l in enumerate(links[x:x+cpu]):
                threads.append(threading.Thread(target=wget, args=('file' + str(links.index(l) + 1), l)))
                threads[-1].start()

            # wait for threads to finish
            for t in threads:
                t.join()
    else:
        print('No such argument! Please use --thread_mode=0 or --thread_mode=1')

    print(f'Time {time.time() - start} seconds')