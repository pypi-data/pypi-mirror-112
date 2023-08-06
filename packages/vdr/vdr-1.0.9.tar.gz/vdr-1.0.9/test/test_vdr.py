import vdr

VDR = vdr.Vdr()
VDR.add_connection("localhost", 12345, "ecdis")
VDR.add_connection("localhost", 12346, "radar")
VDR.add_connection("localhost", 12347, "nmea")

ECDIS = vdr.ReceivingFrame(VDR, "ecdis")
RADAR = vdr.ReceivingFrame(VDR, "radar")
NMEA = vdr.ReceivingNmea(VDR, "nmea")

ECDIS.start()
RADAR.start()
NMEA.start()
