import asyncio
import aioping
import ipaddress
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

# Using argparse for getting variables from command line.
parser = argparse.ArgumentParser(description="IP Lookup on given network")

parser.add_argument('network', type=str, help="IP Network with netmask")
parser.add_argument('--concurrent', type=int,required=True, help="The number of concurrent hosts that are pinged at the same time")
parser.add_argument('--timeout', type=int,default=5, help="Timeout for one host (by default 5s.)")

args = parser.parse_args()

# PingDiscover class.
class PingDiscover:
    # Constructor.
    def __init__(self, network, concurrency, timeout=args.timeout):
        try:
            self.concurrency = concurrency
            self.timeout = timeout
            self.ip_adresses_list = ipaddress.ip_network(network)
        # Returning an exception in the case of wrong IP Adress. Inherited from ipaddress package's ValueError exception.
        except Exception as e:
            print("Please provide correct IP Network")
            raise e

    # Async function for sending ping using aioping package.
    async def send_ping(self, ip_addr):
        try:
            delay = await aioping.ping(ip_addr, timeout=args.timeout) * 1000
            print(ip_addr," Ping response in %s ms" % delay)

        # In the case of timeout , it prints result for host.
        except TimeoutError:
            print("Timed out: ", ip_addr)
            await asyncio.sleep(0.00001)
        
        # In the case of Permission error for gateway IP.
        except PermissionError:
            print("Got PermissionError on host: ", ip_addr)

    # Getting divided ip_blocks and making async pings on asyncio event loop. ip_blocks value contains list of IP Adresses (up to X values defined by user on --concurrent argumen)
    def single_task(self, ip_blocks):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.set_debug(1)
        loop.run_until_complete(self.call_async_ping(loop,ip_blocks))
        loop.close()
    # Helper async function for single_task method.
    async def call_async_ping(self, loop,ip_blocks):
        tasks_list = []
        for single_ip in ip_blocks:
            pingi=loop.create_task(self.send_ping(single_ip.exploded))
            tasks_list.append(pingi)
        await asyncio.wait(tasks_list)

    # Main runner method for defining thread pool.
    def runner(self):

        # Number of threads. It will be used on ThreadPoolExecutor and will run single tasks on per each thread
        num_threads = 5
        with ThreadPoolExecutor(num_threads) as executor:
            futures = {}
            start = time.perf_counter()
            
            # All IP Adresses will be splitted in this list like 
            # [[ 192.168.0.1 ... 192.168.0.8], [ 192.168.0.9 ... 192.168.0.17], ...]
            ip_chunks = [list(self.ip_adresses_list)[x:x+self.concurrency] for x in range(0, len(list(self.ip_adresses_list)), self.concurrency)]
            for i in ip_chunks:
                future = executor.submit(self.single_task, i)
                futures[future] = i
            for future in as_completed(futures):
                ret = future.result()

            finish = time.perf_counter()
            print(f'Finished in {round(finish-start, 2)} seconds')

def main():
    pd = PingDiscover(args.network, args.concurrent,timeout=args.timeout)
    pd.runner()

if __name__ == '__main__':
    main()
       