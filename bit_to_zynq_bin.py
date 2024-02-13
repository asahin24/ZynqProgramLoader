#!/usr/bin/env python3
import sys
import os
import struct
import argparse

#https://github.com/Xilinx/bootgen/blob/master/bitutils.h
#https://github.com/Xilinx/bootgen/blob/master/bitutils.cpp

def flip32(data):
    sl = struct.Struct('<I')
    sb = struct.Struct('>I')
    b = memoryview(data)
    d = bytearray(len(data))
    for offset in range(0, len(data), 4):
        sb.pack_into(d, offset, sl.unpack_from(b, offset)[0])
    return d

parser = argparse.ArgumentParser(description='Convert FPGA bit files to raw bin format suitable for flashing')
parser.add_argument('-f', '--flip', dest='flip', action='store_true', default=False, help='Flip 32-bit endianess (needed for Zynq)')
parser.add_argument("bitfile", help="Input bit file name")
parser.add_argument("binfile", help="Output bin file name")
args = parser.parse_args()

short = struct.Struct('>H')
ulong = struct.Struct('>I')

with open(args.bitfile, 'rb') as bitfile:
    l = short.unpack(bitfile.read(2))[0]
    if l != 9:
        raise Exception("Missing <0009> header (0x%x), not a bit file" % l)
    bitfile.read(l)
    l = short.unpack(bitfile.read(2))[0]
    d = bitfile.read(l)
    if d != b'a':
        raise Exception("Missing <a> header, not a bit file")

    l = short.unpack(bitfile.read(2))[0]
    d = bitfile.read(l).decode('ascii')
    print("Design name:", d)

    KEYNAMES = {b'b': "Partname", b'c': "Date", b'd': "Time"}

    while True:
        k = bitfile.read(1)
        if not k:
            raise Exception("unexpected EOF")
        elif k == b'e':
            l = ulong.unpack(bitfile.read(4))[0]
            print("found binary data:", l)
            d = bitfile.read(l)
            if args.flip:
                d = flip32(d)
            with open(args.binfile, 'wb') as binfile:
                binfile.write(d)
            break
        elif k in KEYNAMES:
            l = short.unpack(bitfile.read(2))[0]
            d = bitfile.read(l).decode('ascii')
            print(KEYNAMES[k], d)
        else:
            print("Unexpected key: ", k)
            l = short.unpack(bitfile.read(2))[0]
            d = bitfile.read(l)