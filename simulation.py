import argparse
import urllib.request
import urllib.error

class Queue:
    """Completed implementation of a queue ADT"""
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class Request:
    """Create request class akin to task class in Chapter 3 reading"""
    def __init__(self, time, process_time):
        self.timestamp = time
        self.process_time = process_time

    def get_stamp(self):
        return self.timestamp

    def get_process_time(self):
        return self.process_time

    def wait_time(self, current_time):
        return current_time - self.timestamp

class Server:
    """Create server class akin to printer class in Chapter 3 reading"""
    def __init__(self):
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self, new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_process_time()


def simulateOneServer(file):
    """prints average wait time for a request"""

    one_server = Server()
    queue = Queue()
    wait_times = []

    """this is the URL we are going to use"""
    url = "https://s3.amazonaws.com/cuny-is211-spring2015/requests.csv"

    """open the URL"""
    response = urllib.request.urlopen(url)

    """Read the response and convert it to string characters if it was in binary"""
    file_content = response.read().decode("utf-8")
    file = file_content.split("\n")

    for row in file:
        request_data = row.split(",")
        timestamp = int(request_data[0])
        process_time = int(request_data[2])
        request = Request(timestamp, process_time)
        queue.enqueue(request)

    while not queue.is_empty():
        if (not one_server.busy()) and (not queue.is_empty()):
            next_request = queue.dequeue()
            wait_times.append(next_request.wait_time(timestamp))
            one_server.start_next(next_request)

        one_server.tick()

    avg_wait_time = sum(wait_times) / len(wait_times)
    print("There is an average wait time of %6.2f seconds" % (avg_wait_time))


def simulateManyServers(file, number_of_servers):
    """prints average wait time for simulation of more than one server"""

    servers = [Server() for i in range(number_of_servers)]
    queue = Queue()
    wait_times = []

    """this is the URL we are going to use"""
    url = "s3.amazonaws.com/cuny-is211-spring2015/requests.csv"

    """open the URL"""
    response = urllib.request.urlopen(url)

    """Read the response and convert it to string characters if it was in binary"""
    file_content = response.read().decode("utf-8")
    file = file_content.split("\n")

    for row in file:
        request_data = row.split(",")
        timestamp = int(request_data[0])
        process_time = int(request_data[2])
        request = Request(timestamp, process_time)
        queue.enqueue(request)

        for one_server in servers:
            if (not one_server.busy()) and (not queue.is_empty()):
                next_request = queue.dequeue()
                wait_times.append(next_request.wait_time(timestamp))
                one_server.start_next(next_request)

            one_server.tick()

    avg_wait_time = sum(wait_times) / len(wait_times)
    print("There is an average wait time of %6.2f seconds" % (avg_wait_time))

def downloadData(url):
    """Downloads the data"""

    """this is the URL we are going to use"""
    # url = "https://s3.amazonaws.com/cuny-is211-spring2015/requests.csv"

    """Open the URL"""
    response = urllib.request.urlopen(url)

    """Read the response and convert it to string characters if it was in binary"""
    file_content = response.read().decode('utf-8').split("\n")
    return file_content


def main(url, number_of_servers):
    print(f"Running main with URL = {url}...")

    """Checking for url"""
    if args.file:
        try:
            request_data = downloadData(args.file)
        except(urllib.error.HTTPError, urllib.error.URLError):
            print("There was an error with provided path")

        if args.servers and args.servers > 1:
            simulateManyServers(request_data, args.servers)
        elif not args.servers or (args.servers and args.servers <= 1):
            simulateOneServer(request_data)

    else:
        print("Enter valid file")


if __name__ == "__main__":
    """Main entry point"""
    """Setting up arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="URL of CSV file with request inputs", type=str)
    parser.add_argument("--servers", help="Number of servers to simulate", type=int)
    args = parser.parse_args()
    main(args.file, args.servers)