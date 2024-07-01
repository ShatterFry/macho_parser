import argparse
import os

MH_MAGIC_64 = "feedfacf"

MH_EXECUTE = "02000000"
MH_DYLIB = "06000000"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("binary")
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

        filetype = file_handle.read(4).hex()
        print("File type: ", filetype)
        if filetype != MH_DYLIB and filetype != MH_EXECUTE:
            raise Exception("Unknown file type")

        ncmds = file_handle.read(4).hex()
        print(ncmds)

        sizeofcmds = file_handle.read(4).hex()
        print(sizeofcmds)

        flags = file_handle.read(4).hex()
        print(flags)

        reserved = file_handle.read(4).hex()
        print(reserved)


if __name__ == "__main__":
    main()