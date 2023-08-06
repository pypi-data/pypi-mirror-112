
def checksum(sentence):
    checksum = 0
    for el in sentence[1:]:
        checksum ^= ord(el)
    return "*" + str(format(checksum, 'x'))


# PROPULSION MANAGEMENT SYSTEM
def GTP(id, load_rate, consumption, power, rpm, nox_emission, temperature):
    """Gas Turbine Parameters"""
    fields = (
        ("Gas turbine ID", id),
        ("Load rate", load_rate),
        ("Consumption", consumption),
        ("Power", power),
        ("RPM", rpm),
        ("NOx emission", nox_emission),
        ("Temperature", temperature)
    )

    sentence = "$PFGTP,"
    for i in fields:
        sentence += str(i[1]) + ","

    return sentence + checksum(sentence) + "\t\n"


def EEP(id, load_rate, consumption, power, rpm, temperature):
    """Electrical Engine Parameters"""
    fields = (
        ("Engine ID", id),
        ("Load rate", load_rate),
        ("Consumption", consumption),
        ("Power", power),
        ("RPM", rpm),
        ("Temperature", temperature)
    )

    sentence = "$PFEEP,"
    for i in fields:
        sentence += str(i[1]) + ","

    return sentence + checksum(sentence) + "\t\n"


def BEP(id, load_rate, consumption, power, rpm, temperature, angle):
    """Backup Engine Parameters"""
    fields = (
        ("Backup engine ID", id),
        ("Load rate", load_rate),
        ("Consumption", consumption),
        ("Power", power),
        ("RPM", rpm),
        ("Temperature", temperature),
        ("Angle", angle)
    )

    sentence = "$PFBEP,"
    for i in fields:
        sentence += str(i[1]) + ","

    return sentence + checksum(sentence) + "\t\n"


# SAFETY MANAGEMENT SYSTEM
def SDS(id, state):
    """Safety Door System"""
    fields = (
        ("Door ID", id),
        ("Door state", state)
    )

    sentence = "$PFSDS,"
    for i in fields:
        sentence += str(i[1]) + ","

    return sentence + checksum(sentence) + "\t\n"


def SBS(id, capacity, level, quantity):
    """Safety Ballast System"""
    fields = (
        ("Ballast ID", id),
        ("Ballast capacity", capacity),
        ("Ballast level", level),
        ("Ballast quantity", quantity)
    )

    sentence = "$PFSBS,"
    for i in fields:
        sentence += str(i[1]) + ","

    return sentence + checksum(sentence) + "\t\n"


def SAS(id, state):
    """Safety Alarm System"""
    fields = (
        ("Alarm ID", id),
        ("Alarm state", state)
    )
    sentence = "$PFSAS,"
    for i in fields:
        sentence += str(i[1]) + ","
    return sentence + checksum(sentence) + "\t\n"


# POWER MANAGEMENT SYSTEM
def DAP(id, load_rate, consumption, power, rpm, nox_emission, temperature):
    """Diesel Alternator Parameters"""
    fields = (
        ("Alternator ID", id),
        ("Load rate", load_rate),
        ("Consumption", consumption),
        ("Power", power),
        ("RPM", rpm),
        ("NOx emission", nox_emission),
        ("Temperature", temperature)
    )

    sentence = "$PFDAP,"
    for i in fields:
        sentence += str(i[1]) + ","

    return sentence + checksum(sentence) + "\t\n"


def PBP(id, capacity, level, quantity):
    """Power Bank Parameters"""
    fields = (
        ("Power bank ID", id),
        ("Power bank capacity", capacity),
        ("Power bank level", level),
        ("Power bank quantity", quantity)
    )

    sentence = "$PFPBP,"
    for i in fields:
        sentence += str(i[1]) + ","

    return sentence + checksum(sentence) + "\t\n"


# UTILITIES MANAGEMENT SYSTEM
def TAP(id, type, capacity, level, quantity, autonomy, pump_state, valve_state):
    """Tank Parameters"""
    fields = (
        ("Tank ID", id),
        ("Tank type", type),
        ("Tank capacity", capacity),
        ("Tank level", level),
        ("Tank quantity", quantity),
        ("Tank autonomy", autonomy),
        ("Tank pump state", pump_state),
        ("Tank valve state", valve_state)
    )

    sentence = "$PFTAP,"
    for i in fields:
        sentence += str(i[1]) + ","

    return sentence + checksum(sentence) + "\t\n"


def COM(id, state, capacity, pressure):
    """Compressor Parameters"""
    fields = (
        ("Compressor ID", id),
        ("Compressor state", state),
        ("Compressor capacity", capacity),
        ("Compressor pressure", pressure)
    )

    sentence = "$PFCOM,"
    for i in fields:
        sentence += str(i[1]) + ","

    return sentence + checksum(sentence) + "\t\n"


def COO(id, state, temperature, humidity):
    """Cooler Parameters"""
    fields = (
        ("Cooler ID", id),
        ("Cooler state", state),
        ("Cooler temperature", temperature),
        ("Cooler humidity", humidity)
    )

    sentence = "$PFCOO,"
    for i in fields:
        sentence += str(i[1]) + ","

    return sentence + checksum(sentence) + "\t\n"
