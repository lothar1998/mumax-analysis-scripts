import numpy as np
import matplotlib.pyplot as mp
import struct
import sys
import json


class SpinWaves:
    def __init__(self, filename):
        self.filename = filename
        self.data = None
        self.info_values = dict()

    def read_file(self):

        with open(self.filename, "rb") as binaryFile:
            line = tuple(binaryFile.readline().decode().split())
            self.info_values.update({line[1]+" "+line[2]: line[3]})

            while True:
                line = binaryFile.readline().decode()
                line_tuple = tuple(line.split(':'))
                key = line_tuple[0].split()[1]
                value = line_tuple[1].split()
                self.info_values.update({key: value})
                if "Begin: Data Binary" in line:
                    break

            datasize = int(self.info_values.get("Begin")[2])

            line = binaryFile.read(datasize)
            if not ((datasize == 4 and struct.unpack('f', line)[0] == 1234567) or (datasize == 8 and struct.unpack('f', line)[0] == 123456789012345)):
                print("read error")
                exit()

            xnodes = int(self.info_values.get("xnodes")[0])
            ynodes = int(self.info_values.get("ynodes")[0])
            znodes = int(self.info_values.get("znodes")[0])

            self.data = np.zeros((xnodes, ynodes, znodes, 3))

            for k in range(znodes):
                for i in range(ynodes):
                    for j in range(xnodes):
                        self.data[j, i, k, 0] = struct.unpack('f', binaryFile.read(4))[0]
                        self.data[j, i, k, 1] = struct.unpack('f', binaryFile.read(4))[0]
                        self.data[j, i, k, 2] = struct.unpack('f', binaryFile.read(4))[0]

    def plot(self, dimension, slice_x, slice_y, slice_z, value_name):

        values = None

        if dimension == 'x':
            if value_name == 'Mx':
                values = self.data[0:, slice_y, slice_z, 0]
            elif value_name == 'My':
                values = self.data[0:, slice_y, slice_z, 1]
            elif value_name == 'Mz':
                values = self.data[0:, slice_y, slice_z, 3]

            mp.xlabel(dimension)
            mp.ylabel(value_name)
            start = float(self.info_values.get("xmin")[0])
            step = float(self.info_values.get("xstepsize")[0])
            stop = float(self.info_values.get("xmax")[0])
            mp.plot(np.arange(start, stop, step), values)

        elif dimension == 'y':
            if value_name == 'Mx':
                values = self.data[slice_x, 0:, slice_z, 0]
            elif value_name == 'My':
                values = self.data[slice_x, 0:, slice_z, 1]
            elif value_name == 'Mz':
                values = self.data[slice_x:, 0:, slice_z, 3]

            mp.xlabel(dimension)
            mp.ylabel(value_name)
            start = float(self.info_values.get("ymin")[0])
            step = float(self.info_values.get("ystepsize")[0])
            stop = float(self.info_values.get("ymax")[0])
            mp.plot(np.arange(start, stop, step), values)

        elif dimension == 'z':
            if value_name == 'Mx':
                values = self.data[slice_x, slice_y, 0:, 0]
            elif value_name == 'My':
                values = self.data[slice_x, slice_y, 0:, 1]
            elif value_name == 'Mz':
                values = self.data[slice_x, slice_y, 0:, 3]

            mp.xlabel(dimension)
            mp.ylabel(value_name)
            start = float(self.info_values.get("zmin")[0])
            step = float(self.info_values.get("zstepsize")[0])
            stop = float(self.info_values.get("zmax")[0])
            mp.plot(np.arange(start, stop, step), values)

        mp.ylim([-1.2, 1.2])
        mp.show()


if __name__ == "__main__":

    arg = tuple(sys.argv)

    json_values = []

    with open('spin_wave_template.json') as json_file:
        data = json.load(json_file)

        for i in data['specification']:
            json_values.append(dict(Name = i['name'], Short = i['short'], Help = i['help'], Type = i['type']))

        if '--' + json_values[6]['Name'] in arg or '-' + json_values[6]['Short'] in arg:
            print(data['name'])
            print(data['description'])
            print()
            for i in json_values:
                print(i['Name'] + '\t\t(-' + i['Short'] + ') - ' + i['Help'])
            exit()

    directory = ""
    slice_x = 0
    slice_y = 0
    slice_z = 0
    direction = 'x'
    value_name = 'Mx'

    if '-' + json_values[0]['Short'] in arg:
        directory = arg[arg.index('-' + json_values[0]['Short']) + 1]
    elif '--' + json_values[0]['Name'] in arg:
        directory = arg[arg.index('--' + json_values[0]['Name']) + 1]

    if '-' + json_values[1]['Short'] in arg:
        value_name = arg[arg.index('-' + json_values[1]['Short']) + 1]
    elif '--' + json_values[1]['Name'] in arg:
        value_name = arg[arg.index('--' + json_values[1]['Name']) + 1]

    if '-' + json_values[2]['Short'] in arg:
        direction = arg[arg.index('-' + json_values[2]['Short']) + 1]
    elif '--' + json_values[2]['Name'] in arg:
        direction = arg[arg.index('--' + json_values[2]['Name']) + 1]

    if '-' + json_values[3]['Short'] in arg:
        slice_x = arg[arg.index('-' + json_values[3]['Short']) + 1]
    elif '--' + json_values[3]['Name'] in arg:
        slice_x = arg[arg.index('--' + json_values[3]['Name']) + 1]

    if '-' + json_values[4]['Short'] in arg:
        slice_y = arg[arg.index('-' + json_values[4]['Short']) + 1]
    elif '--' + json_values[4]['Name'] in arg:
        slice_y = arg[arg.index('--' + json_values[4]['Name']) + 1]

    if '-' + json_values[5]['Short'] in arg:
        slice_z = arg[arg.index('-' + json_values[5]['Short']) + 1]
    elif '--' + json_values[5]['Name'] in arg:
        slice_z = arg[arg.index('--' + json_values[5]['Name']) + 1]

    print(directory, slice_x, slice_y, slice_z, direction, value_name)

    wave = SpinWaves(directory)
    wave.read_file()
    wave.plot(direction, slice_x, slice_y, slice_z, value_name)
