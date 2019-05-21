import sys
import json


class Run:
    def __init__(self, script_json, file_name):

        self.localization = file_name[0:file_name.rfind("/")+1]

        self.script_json = script_json

        self.file_name = file_name[file_name.rfind("/")+1:file_name.rfind(".")]
        self.file_extension = file_name[file_name.rfind("."):]

        self.script = list()
        self.file = list()

        temp_h = open(self.script_json)
        json_temp = json.load(temp_h)
        temp = json_temp['name']
        self.script_name = temp[0:temp.rfind(".")]
        self.script_extension = temp[temp.rfind("."):]
        temp = json_temp['specification']
        self.script = temp.split("\n")
        temp_h.close()

        temp_h = open(self.file_name + self.file_extension)
        self.file = list(temp_h.read().split("\n"))
        temp_h.close()

        print(self.script_name + self.script_extension)
        print(self.file_name + self.file_extension)

    def change(self, line, new_line, start_value, stop_value, step_value):
        k = 0
        for i in range(start_value, stop_value, step_value):

            new_script = open(self.localization + self.script_name + "_" + self.file_name + "_" + str(k) + self.script_extension, "w")
            temp = self.script.copy()
            temp[temp.index("#SBATCH -J")] = "#SBATCH -J " + self.file_name + "_" + str(k)
            temp[temp.index("#SBATCH --output=\"_output.txt\"")] = "#SBATCH --output=" + "\"" + self.file_name + "_" + str(k) + "_" + "output.txt" + "\""
            temp[temp.index("#SBATCH --error=\"_error.txt\"")] = "#SBATCH --error=" + "\"" + self.file_name + "_" + str(k) + "_" + "error.txt" + "\""
            temp[temp.index("mumax3")] = "mumax3" + " " + self.file_name + "_" + str(k) + self.file_extension
            for j in temp:
                new_script.write(j + "\n")
            new_script.close()

            new_file = open(self.localization + self.file_name + "_" + str(k) + self.file_extension, "w")
            temp = self.file.copy()
            temp[temp.index(line)] = new_line.replace('*', str(i))
            for j in temp:
                new_file.write(j + "\n")
            new_file.close()

            k += 1


if __name__ == "__main__":

    arg = tuple(sys.argv)
    print(arg)
    json_values = []

    with open('run_template.json') as json_file:
        data = json.load(json_file)

        for i in data['specification']:
            json_values.append(dict(Name = i['name'], Short = i['short'], Help = i['help'], Type = i['type']))

        if '--' + json_values[0]['Name'] in arg or '-' + json_values[0]['Short'] in arg:
            print(data['name'])
            print(data['description'])
            print()
            for i in json_values:
                print(i['Name'] + '\t\t(-' + i['Short'] + ') - ' + i['Help'])
            exit()

    filename = ""
    line = ""
    into = ""
    start_value = None
    stop_value = None
    step_value = None

    if '-' + json_values[1]['Short'] in arg:
        filename = arg[arg.index('-' + json_values[1]['Short']) + 1]
    elif '--' + json_values[1]['Name'] in arg:
        filename = arg[arg.index('--' + json_values[1]['Name']) + 1]

    if '-' + json_values[2]['Short'] in arg:
        line = arg[arg.index('-' + json_values[2]['Short']) + 1]
    elif '--' + json_values[2]['Name'] in arg:
        line = arg[arg.index('--' + json_values[2]['Name']) + 1]

    if '-' + json_values[3]['Short'] in arg:
        into = arg[arg.index('-' + json_values[3]['Short']) + 1]
    elif '--' + json_values[3]['Name'] in arg:
        into = arg[arg.index('--' + json_values[3]['Name']) + 1]

    if '-' + json_values[4]['Short'] in arg:
        start_value = int(arg[arg.index('-' + json_values[4]['Short']) + 1])
    elif '--' + json_values[4]['Name'] in arg:
        start_value = int(arg[arg.index('--' + json_values[4]['Name']) + 1])

    if '-' + json_values[5]['Short'] in arg:
        stop_value = int(arg[arg.index('-' + json_values[5]['Short']) + 1])
    elif '--' + json_values[5]['Name'] in arg:
        stop_value = int(arg[arg.index('--' + json_values[5]['Name']) + 1])

    if '-' + json_values[6]['Short'] in arg:
        step_value = int(arg[arg.index('-' + json_values[6]['Short']) + 1])
    elif '--' + json_values[6]['Name'] in arg:
        step_value = int(arg[arg.index('--' + json_values[6]['Name']) + 1])

    run = Run("sbatch_script_template.json", filename)

    if stop_value is None or step_value is None:
        step_value = start_value
        stop_value = start_value * 2

    run.change(line, into, start_value, stop_value, step_value)

