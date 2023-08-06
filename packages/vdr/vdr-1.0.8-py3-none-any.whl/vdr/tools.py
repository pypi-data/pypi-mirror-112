from .sentences import *


def update(filename):
    new_number = str(int(filename) + 1)
    while len(new_number) < 6:
        new_number = "0" + new_number
    return new_number


def propulsion(sentence, file):
    id_gt = 0
    id_motor = 0
    id_backup = 0

    for i in sentence:

        if 'gas_turbine' in i:
            file.write(sentence[0] + " " + GTP(id_gt, sentence[sentence.index(i) + 1],
                                               sentence[sentence.index(i) + 2],
                                               sentence[sentence.index(i) + 3],
                                               sentence[sentence.index(i) + 4],
                                               sentence[sentence.index(i) + 5],
                                               sentence[sentence.index(i) + 6]))
            id_gt += 1
        elif 'motor' in i:
            file.write(sentence[0] + " " + EEP(id_motor,
                                               sentence[sentence.index(i) + 1],
                                               sentence[sentence.index(i) + 2],
                                               sentence[sentence.index(i) + 3],
                                               sentence[sentence.index(i) + 4],
                                               sentence[sentence.index(i) + 5]))
            id_motor += 1
        elif 'backup' in i:
            file.write(sentence[0] + " " + BEP(id_backup, sentence[sentence.index(i) + 1],
                                               sentence[sentence.index(i) + 2],
                                               sentence[sentence.index(i) + 3],
                                               sentence[sentence.index(i) + 4],
                                               sentence[sentence.index(i) + 5],
                                               sentence[sentence.index(i) + 6]))
            id_backup += 1


def safety(sentence, file):
    id_door = 0
    id_ballast = 0
    id_alarm = 0

    for i in sentence:

        if 'door' in i:
            file.write(sentence[0] + " " + SDS(id_door, sentence[sentence.index(i) + 1]))
            id_door += 1
        elif 'ballast' in i:
            file.write(sentence[0] + " " + SBS(id_ballast,
                                               sentence[sentence.index(i) + 1],
                                               sentence[sentence.index(i) + 2],
                                               sentence[sentence.index(i) + 3]))
            id_ballast += 1
        elif 'alarm' in i:
            file.write(sentence[0] + " " + SAS(id_alarm, sentence[sentence.index(i) + 1]))
            id_alarm += 1


def power(sentence, file):
    id_alternator = 0
    id_battery = 0

    for i in sentence:

        if 'alternator' in i:
            file.write(sentence[0] + " " + DAP(id_alternator, sentence[sentence.index(i) + 1],
                                               sentence[sentence.index(i) + 2],
                                               sentence[sentence.index(i) + 3],
                                               sentence[sentence.index(i) + 4],
                                               sentence[sentence.index(i) + 5],
                                               sentence[sentence.index(i) + 6]))
            id_alternator += 1
        elif 'battery' in i:
            file.write(sentence[0] + " " + PBP(id_battery,
                                               sentence[sentence.index(i) + 1],
                                               sentence[sentence.index(i) + 2],
                                               sentence[sentence.index(i) + 3]))
            id_battery += 1


def utilities(sentence, file):
    id_tank = 0
    id_compressor = 0
    id_cooler = 0

    for i in sentence:

        if 'tank' in i:
            file.write(sentence[0] + " " + TAP(id_tank, sentence[sentence.index(i) + 1],
                                               sentence[sentence.index(i) + 2],
                                               sentence[sentence.index(i) + 3],
                                               sentence[sentence.index(i) + 4],
                                               sentence[sentence.index(i) + 5],
                                               sentence[sentence.index(i) + 6],
                                               sentence[sentence.index(i) + 7]))
            id_tank += 1
        elif 'compressor' in i:
            file.write(sentence[0] + " " + COM(id_compressor,
                                               sentence[sentence.index(i) + 1],
                                               sentence[sentence.index(i) + 2],
                                               sentence[sentence.index(i) + 3]))
            id_compressor += 1
        elif 'cooler' in i:
            file.write(sentence[0] + " " + COO(id_cooler, sentence[sentence.index(i) + 1],
                                               sentence[sentence.index(i) + 2],
                                               sentence[sentence.index(i) + 3]))
            id_cooler += 1
