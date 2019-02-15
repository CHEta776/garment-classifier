import pandas as pd
import requests
import os
from queue import Queue
from time import time
from threading import Thread
from PIL import Image
from io import BytesIO


class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            url, filename = self.queue.get()
            response = requests.get(url)

            if response.status_code == 200:
                img = Image.open(BytesIO(response.content)).convert('RGB')
                img.thumbnail((400, 400), Image.ANTIALIAS)
                img.save(filename)
            else:
                print('Error with: {}'.format(url))

            self.queue.task_done()


def download_urls(base_folder='Images', threads=10):

    print('=====================================================================================================')
    print('                                   DOWNLOAD STARTED                                                  ')
    print('=====================================================================================================')
    ts = time()

    base_folder = os.path.join(base_folder, 'Images')

    print('Image destination folder: {}'.format(base_folder))

    # Prepare output folder
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    # Create a queue to communicate with the worker threads
    queue = Queue()

    # Read data
    data = pd.read_csv('Data/data.csv').url

    # Create  worker threads
    print('Creating {} threads'.format(threads))
    for x in range(threads):
        worker = DownloadWorker(queue)

        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()

    print('Total URLs: {}'.format(len(data)))

    # Put the tasks into the queue as a tuple
    for i, url in enumerate(data[:1000]):
        queue.put((url, '{}/{}.png'.format(base_folder, i)))

    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()
    print('Took {}'.format(time() - ts))

