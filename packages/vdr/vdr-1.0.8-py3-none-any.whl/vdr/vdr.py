# https://www.sciencedirect.com/science/article/pii/S1742287613000510
# https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjViPqBjrDxAhUGjhQKHe0SCN0QFjAAegQIAxAD&url=https%3A%2F%2Fwww.iacs.org.uk%2Fdownload%2F1871&usg=AOvVaw2AFrLs9fUAaCMTTwdPvqJq
import errno
import os
import socket
import threading
import time
from pathlib import Path
import configparser
from .tools import *
import logging


# List of creation time of files/frames
frame_creation_times = []
nmea_creation_times = []

# Parser of configuration file
config = configparser.ConfigParser()
config.read('config.ini')
record_duration = config['record']['duration']                          # Record duration from config file

# Logger declaration
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s')
logging.getLogger().setLevel(logging.INFO)                              # TODO: configuration of logging level


class Vdr:
    """
    A class used to represent the VDR (Voyage Data Recorder).
    """

    config = configparser.ConfigParser()
    config.read('config.ini')

    def __init__(self, path="."):
        """
        :param path: Path where the VDR data will be stored.
        """
        # Check if the final character is a "/" to avoid pathname error
        if path[-1] == "/":
            self.path = path + "data"
        else:
            self.path = path + "/data"

        # Filename initialisation
        self.frame_filename = "000000"
        self.nmea_filename = "000000"
        self.voice_filename = "000000"

        self.connections = {}
        self.start_time = time.time()
        # End time is calculated to predict when we will need to process file removing
        self.end_time = self.start_time + int(config['record']['duration'])

        logging.info('Start time is %f', self.start_time)

        # Create tree structure of VDR if it is not already exists
        if not os.path.exists(path + "/data"):
            os.makedirs(path + "/data")
        if not os.path.exists(path + "/data/frame"):
            os.makedirs(path + "/data/frame")
        if not os.path.exists(path + "/data/nmea"):
            os.makedirs(path + "/data/nmea")
        if not os.path.exists(path + "/data/voice"):
            os.makedirs(path + "/data/voice")

    def add_connection(self, ip, port, key):
        """
        Adding connection to the VDR by listening on a specified socket.

        :param ip: Interface to listening on.
        :type ip: string
        :param port: Port to listening on.
        :type port: int
        :param key: Name of the connection (important to interact with it).
        :type key: string
        """

        # Socket declaration
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((ip, port))

        # Adding connection to the list
        self.connections[key] = sock


class ReceivingFrame(threading.Thread):

    def __init__(self, vdr, key):
        threading.Thread.__init__(self)
        self.vdr = vdr
        self.key = key

    def run(self):

        while True:
            data = self.vdr.connections[self.key].recvfrom(1024)                        # Receiving data from the specified connection
            path = self.vdr.path + "/frame/" + self.vdr.frame_filename + ".bmp"         # Path of the picture file that will be received
            path_gz = path + ".gz"                                                      # Path with .gz compress extension

            # Testing if the file not already exists or is not currently processed
            while os.path.exists(path) or os.path.exists(path_gz):
                logging.debug("Filename %s already exists", self.vdr.frame_filename)    # DEBUG
                self.vdr.frame_filename = update(self.vdr.frame_filename)               # If it exists filename is updated
                path = self.vdr.path + "/frame/" + self.vdr.frame_filename + ".bmp"     # Updating path
                path_gz = path + ".gz"                                                  # Updating path_gz

            # Start to receive a picture when we receive "start"
            if data[0] == b'start':
                f = open(path_gz, 'wb')                                                 # Opening file to store compressed received data
                data = self.vdr.connections[self.key].recvfrom(8192)                    # Receiving data from specified connection

                # While we receive data of a picture
                while data:
                    # If we receive "stop" the picture reception is ended
                    if data[0] == b'stop':
                        logging.info("Picture %s received from %s", self.vdr.frame_filename, self.key)          # INFO
                        f.close()                                                                               # Close the file
                        os.system("gunzip " + path_gz)                                                          # Extract the compress file .gz
                        frame_creation_times.append((self.vdr.frame_filename, os.path.getmtime(path)))          # Adding filename and creation timestamp to the list
                        current_time = time.time()                                                              # Current time

                        # Processing of removing oldest files
                        if current_time > self.vdr.end_time:
                            for i in frame_creation_times:                                                      # Reading timestamp of the list
                                if i[1] < current_time - int(config['record']['duration']):                     # Check if it is not too older
                                    os.remove(self.vdr.path + "/frame/" + i[0] + ".bmp")                        # Removing older file
                                    logging.debug("Removing too old file %s", self.vdr.frame_filename)          # DEBUG
                                    frame_creation_times.pop(0)                                                 # Removing it from the list
                                else:
                                    break                                                                       # Exit the loop if a file is not to older
                        break                                                                                   # Exit the loop that receive data
                    # Else we continue to receive data picture and store it
                    else:
                        f.write(data[0])                                        # Write data into file
                        data = self.vdr.connections[self.key].recvfrom(8192)    # Receiving data


class ReceivingNmea(threading.Thread):

    def __init__(self, vdr, key):
        threading.Thread.__init__(self)
        self.key = key
        self.vdr = vdr

    def run(self):

        while True:
            data = self.vdr.connections[self.key].recvfrom(1024)
            logging.debug("%s receiving: %s", self.key, data[0])
            logging.info("Data received from %s", self.key)
            path = self.vdr.path + "/nmea/" + self.vdr.nmea_filename
            file = open(path, "a")
            file_size = Path(path).stat().st_size
            if file_size > int(self.vdr.config['nmea']['size']):
                file.close()
                nmea_creation_times.append((self.vdr.nmea_filename, os.path.getmtime(self.vdr.path + "/nmea/" + self.vdr.nmea_filename)))
                current_time = time.time()

                if current_time > self.vdr.end_time:
                    for i in nmea_creation_times:
                        if i[1] < current_time - int(config['record']['duration']):
                            os.remove(self.vdr.path + "/nmea/" + i[0])
                            nmea_creation_times.pop(0)
                        else:
                            break

                self.vdr.nmea_filename = update(self.vdr.nmea_filename)
                file = open(path, "a")

            split_data = bytes.decode(data[0]).split(',')

            try:
                if split_data[0] == "$":
                    file.write(','.join(split_data))
                elif split_data[1] == "propulsion_management_system":
                    propulsion(split_data, file)
                elif split_data[1] == "safety_management_system":
                    safety(split_data, file)
                elif split_data[1] == "power_management_system":
                    power(split_data, file)
                elif split_data[1] == "utilities_management_system":
                    utilities(split_data, file)

            except IndexError:
                logging.error(errno)
