from sys import argv

(StartMask, AMask, BMask, XMask,
    YMask, ZMask, UpMask, DownMask) = (1 << x for x in range(8))

infile = argv[1]
outfile = argv[2]

blank = "".join(chr(x) for x in (0, 0, 0, 0, 128, 128, 128, 128))

with open(outfile, "w") as f:
    data = open(infile, "r").read()

    f.write(data[0:0x100])                   # header
    f.write(data[0x100:0x100 + 123 * 0x20])  # first 123 frames: "ready, go"

    for frame in range(123, (len(data) - 0x100) // 0x20 + 1):
        f.write(data[0x100 + 0x20 * frame:0x100 + 0x20 * (frame + 1)])
        for input in (StartMask, XMask|DownMask, XMask|DownMask, XMask|DownMask, XMask|DownMask, StartMask):
            f.write(chr(input))
            f.write(blank[1:])
            for port in range(2, 4 + 1):
                f.write(blank)
