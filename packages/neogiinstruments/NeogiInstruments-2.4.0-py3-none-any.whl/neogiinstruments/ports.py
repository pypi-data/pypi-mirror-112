import serial as s
import serial.tools.list_ports as lp


# based on elliptec code
from tabulate import tabulate


def find_ports():
    avail_ports = []
    for port in lp.comports():
        if port.serial_number:
            # print(port.serial_number)
            try:
                p = s.Serial(port.device)
                p.close()
                avail_ports.append(port)
            except (OSError, s.SerialException):
                print('%s unavailable.\n' % port.device)
    # pass
    return avail_ports


def port_table():
    ports = find_ports()
    table = [[port.hwid, port.serial_number, port,port.hwid.split(" ")[1].replace("VID:PID=",""),port.name] for port in ports]
    print(tabulate(table,headers=["hwid(full)","serial_number","port","hwid","tty"]))
