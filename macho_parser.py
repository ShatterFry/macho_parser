import argparse
import os

MH_MAGIC_64 = "feedfacf"

MH_EXECUTE = "02"
MH_DYLIB = "06"

LC_SEGMENT = "01"
LC_SEGMENT_64 = "19"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("binary", help="Mach object binary file path (executable/.dylib)")
    args = parser.parse_args()

    binary_path = args.binary

    if not os.path.exists(args.binary):
        raise Exception("Input binary path does not exist!")

    with open(binary_path, "rb") as file_handle:
        # header 32 bytes, 8 fields
        magic = file_handle.read(4)
        magic = magic[::-1].hex()
        print("Magic: ", magic)
        if magic != MH_MAGIC_64:
            raise Exception("Invalid header magic!")
        
        cputype = file_handle.read(4).hex()
        print(cputype)

        cpusubtype = file_handle.read(4).hex()
        print(cpusubtype)

        filetype = file_handle.read(4).hex().rstrip("0")
        print("File type: ", filetype)
        if filetype != MH_DYLIB and filetype != MH_EXECUTE:
            raise Exception("Unknown file type")

        ncmds_bytes = file_handle.read(4)
        print("ncmds bytes", ncmds_bytes)
        ncmds_str = ncmds_bytes.hex().rstrip("0")
        print("ncmds hex str", ncmds_str)
        #ncmds_int = int(f"0x{ncmds_str}", 0)
        ncmds_int = int(ncmds_str, 16)
        print("ncmds (decimal): ", ncmds_int)

        sizeofcmds = file_handle.read(4).hex().rstrip("0")
        print("sizeofcmds: ", sizeofcmds)

        flags = file_handle.read(4).hex()
        print(flags)

        reserved = file_handle.read(4).hex()
        print(reserved)

        # Load commands
        cmd = file_handle.read(4).hex().rstrip("0")
        cmdsize = file_handle.read(4).hex().rstrip("0")
        segname = file_handle.read(16).decode().rstrip("\x00")
        print(cmd, cmdsize, segname)
        if cmd != LC_SEGMENT_64:
            raise Exception()

if __name__ == "__main__":
    main()