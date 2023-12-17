import machine
import time
import struct
sda = machine.Pin(0)
scl = machine.Pin(1)

i2c = machine.I2C(0, sda=sda, scl=scl, freq=1000)
temp_sense = 0x3a

def i2c_read(i2c, addr, reg, count=1, unpack_format='H'):
    addr_msb = reg >> 8 & 0x00FF
    addr_lsb = reg & 0x00FF

    i2c.writeto(addr, bytes([addr_msb, addr_lsb]), False)
    read = i2c.readfrom(addr, count*2)

    if unpack_format is None:
        return bytes(list(read))
    results = struct.unpack(">{}{}".format(count, unpack_format), bytes(list(read)))
    if count == 1:
        return results[0]
    return results

def i2c_write(i2c, addr, reg, data):
    cmd = []
    reg_msb = reg >> 8
    cmd.append(reg & 0x00FF)

    if type(data) is list:
        for d in data:
            cmd.append((d>>8) & 0x00FF)
            cmd.append(d & 0x00FF)
    else:
        cmd.append((data>>8) & 0x00FF)
        cmd.append(data & 0x00FF)
    # print(reg_msb, cmd)
    i2c.writeto(addr, reg_msb, bytearray(cmd))


    if (addr & 0xFF00) == 0x2400: # Wait after EEWRITE!
        time.sleep(0.010) # 10ms

    return 0


