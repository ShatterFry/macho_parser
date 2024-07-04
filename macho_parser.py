import argparse
import os
from enum import Enum

mach_header_bytes_num = 32
MH_MAGIC_64 = "feedfacf"

MH_EXECUTE = "02"
MH_DYLIB = "06"

LC_SEGMENT = "01"
LC_SEGMENT_64 = "19"

CSMAGIC_CODEDIRECTORY = "fade0c02"

class BinaryType(Enum):
    EXECUTABLE = 1,
    DYLIB = 2

class LoadCommandInfo:
    def __init__(self, file_handle) -> None:
        self._cmd = file_handle.read(4).hex().rstrip("0")
        self._cmdsize_hex = file_handle.read(4).hex().rstrip("0")
        self._cmdsize_decimal = int(self._cmdsize_hex, 16)
        self._remaining_bytes = file_handle.read(self._cmdsize_decimal - 8)


class segment_command_64(LoadCommandInfo):
    def __init__(self, file_handle) -> None:
        super().__init__(file_handle)
        if self._cmd != LC_SEGMENT_64:
            # {self._remaining_bytes}
            raise Exception(f"Unexpected cmd type: {self._cmd} {self._cmdsize_decimal} \n")
        
        self._segname = self._remaining_bytes[:16]
        print("segname len: ", len(self._segname))
        self._segname = self._segname.decode().rstrip("\x00")

        self.vmaddr = self._remaining_bytes[16:24].hex()
        self.vmsize = self._remaining_bytes[24:32].hex()
        self.fileoff = self._remaining_bytes[32:40].hex()
        self.filesize = self._remaining_bytes[40:48].hex()

        self.maxprot = self._remaining_bytes[48:52].hex()
        self.initprot = self._remaining_bytes[52:56].hex()
        self._nsects_hex = self._remaining_bytes[56:60].hex()
        self._nsects_int = int(self._nsects_hex, 16)
        print(f"Number of sections in segment: {self._nsects_int}")
        self.flags = self._remaining_bytes[60:64].hex()


def print_command_info(file_handle):
        print("Printing command info")
        load_command = segment_command_64(file_handle)
        print(f"cmd: {load_command._cmd} cmdsize: {load_command._cmdsize_decimal}")
        print(f"Remaining bytes:\n{load_command._remaining_bytes}")
        return load_command


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
            
        if filetype == MH_EXECUTE:
            binary_type = BinaryType.EXECUTABLE
        elif filetype == MH_DYLIB:
            binary_type = BinaryType.DYLIB
        else:
            raise Exception(f"Unknown file type {filetype}")

        ncmds_bytes = file_handle.read(4)
        print("ncmds bytes", ncmds_bytes)
        ncmds_str = ncmds_bytes.hex().rstrip("0")
        print("ncmds hex str", ncmds_str)
        #ncmds_int = int(f"0x{ncmds_str}", 0)
        ncmds_int = int(ncmds_str, 16)
        print("ncmds (decimal): ", ncmds_int)

        sizeofcmds_hex = file_handle.read(4).hex().rstrip("0")
        print("sizeofcmds_hex: ", sizeofcmds_hex)

        sizeofcmds_decimal = int(sizeofcmds_hex, 16)
        print(sizeofcmds_decimal)

        flags = file_handle.read(4).hex()
        print(flags)

        reserved = file_handle.read(4).hex()
        print(reserved)

        load_commands_begin_offset = file_handle.tell()
        print("Load commands begin offset", load_commands_begin_offset)
        if load_commands_begin_offset != mach_header_bytes_num:
            raise Exception()
        
        last_command_start = load_commands_begin_offset

        # Load commands
        pagezero = None
        if binary_type == BinaryType.EXECUTABLE:
            pagezero = print_command_info(file_handle)
        # sectname __text
        # segname __TEXT
        segment_64 = print_command_info(file_handle)
        print_command_info(file_handle)


if __name__ == "__main__":
    main()