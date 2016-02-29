#!/usr/bin/env python2

from sys import argv
import struct

(StartMask, AMask, BMask, XMask,
    YMask, ZMask, UpMask, DownMask) = (1 << x for x in range(8))

blank = "".join(chr(x) for x in (0, 0, 0, 0, 0x80, 0x80, 0x80, 0x80))

WAIT_FRAMES = 1165 * 2


def __main__():
    if len(argv[1:]) == 2:
        infile = argv[1]
        outfile = argv[2]
    else:
        print("usage: python2 conv.py infile outfile")
        exit(1)

    with open(outfile, "w") as f:
        data = open(infile, "r").read()

        VIs, inputs, lag = struct.unpack("<3Q", data[0xD:0x25])
        data = data[:0xD] + struct.pack("<2Q", (VIs + lag) * 6, inputs * 6) + data[0x1D:]

        f.write(data[0:0x100])                           # header
        f.write(data[0x100:0x100 + WAIT_FRAMES * 0x20])  # skip to "ready, go"

        for input in (StartMask, UpMask, YMask | DownMask, StartMask):
            f.write(chr(input))
            f.write(blank[1:])
            for port in range(2, 4 + 1):
                f.write(blank)

        for frame in range(WAIT_FRAMES, (len(data) - 0x100) // 0x20 + 1):
            f.write(data[0x100 + 0x20 * frame:0x100 + 0x20 * (frame + 1)])
            for input in (StartMask, XMask | DownMask, XMask | DownMask, XMask | DownMask, XMask | DownMask, StartMask):
                f.write(chr(input))
                f.write(blank[1:])
                for port in range(2, 4 + 1):
                    f.write(blank)

if __name__ == "__main__":
    __main__()
