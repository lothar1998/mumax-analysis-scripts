import math
import sys
import json


class Amplitude:
    def __init__(self, m0, J0, Hk, omega):
        self.m0 = m0
        self.J0 = J0
        self.Hk = Hk
        self.omega = omega

    def calculate(self):
        nominator = abs(self.m0 * self.J0 * (self.Hk - (self.J0 * math.sqrt(1 - pow(self.m0, 2))) + self.omega))
        d_com1 = pow(pow(self.omega, 2) - pow(self.Hk - (self.J0 * math.sqrt(1 - pow(self.m0, 2))), 2), 2)
        d_com2 = pow(self.m0 * self.J0 * (self.Hk - (self.J0 * math.sqrt(1 - pow(self.m0, 2))) + pow(self.omega, 2)), 2)

        amplitude = nominator / math.sqrt(pow(d_com1, 2) + pow(d_com2, 2))

        return amplitude


if __name__ == "__main__":

    arg = tuple(sys.argv)

    json_values = []

    with open('amplitude_template.json') as json_file:
        data = json.load(json_file)

        for i in data['specification']:
            json_values.append(dict(Name=i['name'], Short=i['short'], Help=i['help'], Type=i['type']))

        if '--' + json_values[4]['Name'] in arg or '-' + json_values[4]['Short'] in arg:
            print(data['name'])
            print(data['description'])
            print()
            for i in json_values:
                print(i['Name'] + '\t\t(-' + i['Short'] + ') - ' + i['Help'])
            exit()

    m0 = 0
    J0 = 0
    Hk = 0
    omega = 0

    if '-' + json_values[0]['Short'] in arg:
        m0 = float(arg[arg.index('-' + json_values[0]['Short']) + 1])
    elif '--' + json_values[0]['Name'] in arg:
        m0 = float(arg[arg.index('--' + json_values[0]['Name']) + 1])

    if '-' + json_values[1]['Short'] in arg:
        J0 = float(arg[arg.index('-' + json_values[1]['Short']) + 1])
    elif '--' + json_values[1]['Name'] in arg:
        J0 = float(arg[arg.index('--' + json_values[1]['Name']) + 1])

    if '-' + json_values[2]['Short'] in arg:
        Hk = float(arg[arg.index('-' + json_values[2]['Short']) + 1])
    elif '--' + json_values[2]['Name'] in arg:
        Hk = float(arg[arg.index('--' + json_values[2]['Name']) + 1])

    if '-' + json_values[3]['Short'] in arg:
        omega = float(arg[arg.index('-' + json_values[3]['Short']) + 1])
    elif '--' + json_values[3]['Name'] in arg:
        omega = float(arg[arg.index('--' + json_values[3]['Name']) + 1])

    amp = Amplitude(m0, J0, Hk, omega)

    print(amp.calculate())
