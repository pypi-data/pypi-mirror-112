#!/usr/bin/env python3

import binascii
import hashlib
import os
import re
import time

import xmodem


class HardwareAPICLI:
    UNKNOWN = 1
    UBOOT = 2
    LINUX = 3

    def __init__(self, serial_device, username=None, password=None, logfile=None):
        self._serial = serial_device
        self._state = HardwareAPICLI.UNKNOWN
        self._timeout = 10
        if logfile:
            if hasattr(logfile, "write"):
                self._logfile = logfile
            else:
                self._logfile = open(logfile, "wb")
        else:
            self._logfile = None
        self._username = username
        self._password = password

    def _log(self, data):
        if self._logfile:
            self._logfile.write(data)

    @property
    def state(self):
        return self._state

    def _putc(self, data, timeout=1):
        """xmodem putc implementation - not logged"""
        self._serial.write(data)

    def _getc(self, size, timeout=1):
        """xmodem getc implementation - not logged"""
        self._serial.timeout = timeout
        data = self._serial.read(size)
        return data

    def readline(self, targets=[]):
        """Reads the outstanding line of data.
        Returns the line read, and an index into targets of which re matched (or -1 if none)"""

        self._serial.timeout = 1
        data = b""
        index = -1
        while True:
            new_data = self._serial.read(1)
            if not new_data:
                break
            # print("new data", new_data)
            data = data + new_data
            line = data.decode("cp437")  # .strip("\r\n")
            for i in range(len(targets)):
                # print("checking \n'{};\n against {}".format(line, targets[i]))
                if re.search(targets[i], line.lstrip()):
                    index = i
            if new_data == b"\n" or index != -1:
                break

        self._log(data)

        return (data.decode("cp437"), index)

    def write(self, data: str):
        if type(data) == str:
            data = data.encode("cp437")
        self._log(data)
        self._serial.write(data)

    def slow_write(self, data: str):
        if type(data) == str:
            data = data.encode("cp437")
        self._log(data)
        for r in data:
            self._serial.write(bytearray([r]))
            time.sleep(0.005)

    def absorb_outstanding(self, timeout=0.1):
        end = time.time() + timeout
        self._serial.timeout = 0.1
        saw_data = False
        while time.time() <= end or saw_data:
            time.sleep(0.1)
            data = self._serial.read(100)
            self._log(data)
            saw_data = True if data else False

    def wait_for(self, targets, timeout=None, send_ctrl_c=False, line_callback=None):
        if type(targets) == str:
            targets = [targets]
        if not timeout:
            timeout = self._timeout
        start = time.time()
        response = []
        found = -1
        while found == -1:
            if time.time() - start > timeout:
                raise TimeoutError("Timeout waiting for {}".format(", ".join(targets)))
            if send_ctrl_c:
                self.write(b"\x03")
            (line, found) = self.readline(targets)
            if not line:
                continue
            line = line.strip("\r\n")
            response.append(line)
            if line_callback:
                if line_callback(line):
                    return response
        return (response, found)

    def wait_for_prompt(
        self, timeout=None, send_ctrl_c=False, line_callback=None, expect_crash=False
    ):
        prompts = [
            "^.*[a-z]+@[a-z]+:~# .*",  # Linux
            "^# .*",  # Linux
            "^=> .*",  # U-Boot
            "^U-Boot> .*",  # U-Boot
            "^u-boot=> ", # U-Boot
        ]
        states = [
            HardwareAPICLI.LINUX,
            HardwareAPICLI.LINUX,
            HardwareAPICLI.UBOOT,
            HardwareAPICLI.UBOOT,
            HardwareAPICLI.UBOOT,
        ]

        def login_callback(line):
            # TODO: Add more strings here that indicate either a U-Boot or Linux crash
            crash_strings = [
                "Unable to handle kernel paging request at virtual address",
                "Unable to handle kernel NULL pointer dereference",
                "gpmi-nand: DMA timeout, last DMA",
            ]
            if self._username is not None and re.match(".* login:", line):
                self.write(self._username + "\n")
            elif self._password is not None and re.match(".*Password:", line):
                self.write(self._password + "\n")
            if line_callback:
                return line_callback(line)
            if not expect_crash:
                for p in crash_strings:
                    if p in line:
                        # Grab all of the incoming serial data for the next
                        # 10 seconds so we can log it, then die
                        self.absorb_outstanding(timeout=10)
                        raise Exception("Crash: {}".format(line))
            return False

        (response, index) = self.wait_for(
            prompts, timeout=timeout, send_ctrl_c=send_ctrl_c, line_callback=login_callback
        )

        self._state = states[index]

        self.absorb_outstanding()

        return response

    def run_command(self, command, timeout=None):
        self.absorb_outstanding()
        command = command.strip()

        # Linux has proper buffering, so we can run commands faster
        if self.state == HardwareAPICLI.LINUX:
            self.write(command + "\n")
        else:
            self.slow_write(command + "\n")
        response = self.wait_for_prompt(timeout=timeout)
        if len(response) > 1:
            if response[0] != command:
                raise Exception(
                    "Expected command '{}' to echo back, got '{}'".format(command, response[0])
                )
            # The first line is the command itself, the last is the prompt
            response = response[1:-1]
        # Strip off any trailing empty lines
        retval = []
        for i, line in reversed(list(enumerate(response))):
            if len(line) == 0 and len(retval) == 0:
                continue
            retval.insert(0, line)

        return retval

    def uboot_list_commands(self):
        raw_commands = self.run_command("help")
        commands = []
        for c in raw_commands:
            commands.append(c.split("-")[0].strip())
        return commands

    def uboot_has_command(self, name):
        return name in self.uboot_list_commands()

    def uboot_tftp_file(self, filename, load_address=None, host_ip=None):
        command = "tftpboot "
        if load_address is not None:
            command = command + "0x%x " % (load_address)
        else:
            command = command + "$loadaddr "
        if host_ip is not None:
            command = command + "{}:".format(host_ip)
        command = command + filename
        return self.run_command(command)

    def uboot_nfs_file(self, filename, load_address=None, host_ip=None):
        command = "nfs "
        if load_address is not None:
            command = command + "0x%x " % (load_address)

        if host_ip is not None:
            command = command + "{}:".format(host_ip)

        command = command + filename
        return self.run_command(command, timeout=60)

    def uboot_bootz(self, kernel_address=None, initrd_address=None, dtb_address=None, timeout=None):
        command = "bootz "
        if kernel_address is not None:
            command = command + "0x%x " % (kernel_address)
        else:
            command = command + "$loadaddr "
        if initrd_address is not None:
            command = command + "0x%x " % (initrd_address)
        else:
            command = command + "- "
        if dtb_address is not None:
            command = command + "0x%x " % (dtb_address)

        return self.run_command(command, timeout=timeout)

    def uboot_setenv(self, variable, value):
        command = "setenv {} '{}'".format(variable, value)
        return self.run_command(command)

    def uboot_getenv(self, variable):
        val = self.run_command("printenv {}".format(variable))
        if len(val) != 1:
            raise Exception("Invalid variable (more than 1 line)")
        val = val[0]
        if not val.startswith(variable + "="):
            raise Exception("Invalid printenv response")
        return val[len(variable) + 1 :]

    def uboot_get_crc(self, start, length):
        """Retrieve the CRC32 of a given area of memory"""
        # Response of the form 'crc32 for 12000000 ... 120cffff ==> 1175b4fc'
        resp = self.run_command("crc 0x%x 0x%x" % (start, length))[-1]
        return int(resp.split(" ")[-1], 16)

    def _file_crc(self, filename):
        with open(filename, "rb") as stream:
            return binascii.crc32(stream.read()) & 0xFFFFFFFF

    def uboot_loadmem(self, filename, load_address, callback=None):
        """Load a given local file into the given address via individual memory
        byte writes (VERY SLOW)"""
        start = time.time()
        offset = 0
        size = 0

        with open(filename, "rb") as stream:
            size = os.path.getsize(filename)
            while True:
                byte = stream.read(1)
                if byte == b"":
                    break
                self.run_command("mw.b 0x%8.8x 0x%2.2x" % (load_address + offset, ord(byte)))
                offset = offset + 1
                if callback:
                    callback(offset, size)
        duration = time.time() - start
        if not duration:
            duration = 1
        print(
            "{} {:.2f}s to transfer {:.0f}kB: {:.2f}kB/s".format(
                os.path.basename(filename), duration, size / 1024, (size / 1024) / duration
            )
        )

        # Make sure the CRC matches
        crc = self._file_crc(filename)

        unit_crc = self.uboot_get_crc(load_address, size)
        if unit_crc != crc:
            raise Exception("CRC mismatch after download: {:x} != {:x}".format(crc, unit_crc))

    def uboot_loadx(self, filename, load_address, callback=None):
        """Load a given local file into the given address
        callback: Callback function to indicate progress. called as callback(position, total_size)"""
        start = time.time()
        size = 0

        def xmodem_callback(total_packets, success_count, error_count):
            # Adjust packet sizes to byte offsets
            pos = min(total_packets * 1024, size)
            callback(pos, size)

        with open(filename, "rb") as stream:
            size = os.path.getsize(filename)
            if callback:
                callback(0, size)
            self.write("loadx 0x%x\n" % (load_address))
            self.wait_for("## Ready for binary.* bps\.\.\.")
            modem = xmodem.XMODEM(self._getc, self._putc, mode="xmodem1k")
            if not modem.send(stream, callback=xmodem_callback if callback else None):
                raise Exception("Failed to send {}".format(filename))
        duration = time.time() - start
        if not duration:
            duration = 1
        print(
            "{} {:.2f}s to transfer {:.0f}kB: {:.2f}kB/s".format(
                os.path.basename(filename), duration, size / 1024, (size / 1024) / duration
            )
        )
        self.wait_for_prompt()

        # Make sure the CRC matches
        crc = self._file_crc(filename)

        unit_crc = self.uboot_get_crc(load_address, size)
        if unit_crc != crc:
            raise Exception("CRC mismatch after download: {:x} != {:x}".format(crc, unit_crc))

    def uboot_download_memory(self, start, length):
        """Dump an area of memory, and return it as a raw bytearray"""
        crc = self.uboot_get_crc(start, length)
        result = bytearray()
        chunk_size = 8192
        for i in range(0, length, chunk_size):
            this_len = min(chunk_size, length - len(result))
            this_start = start + len(result)
            data = self.run_command("md.b 0x%x 0x%x" % (this_start, this_len))
            for d in data:
                # Lines look like:
                # 12006050: ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff    ................
                # 01234567890123456789012345678901234567890123456789012345678901234567890123456789
                # Pull out the hex string and convert to a bytearray
                raw_hex = d[10:57].strip().split(" ")
                hex_data = bytearray(map(lambda x: int(x, 16), raw_hex))
                result.extend(hex_data)

        # Check CRC against uboot crc
        read_crc = binascii.crc32(result)
        if read_crc != crc:
            raise Exception("CRC mismatch after memory read: {:x} != {:x}".format(crc, read_crc))
        return result

    def uboot_get_version(self):
        version = self.run_command("version")
        for v in version:
            if v.startswith("U-Boot"):
                pos = v.find(",")
                if pos > 0:
                    return v[0:pos]
                return v
        raise Exception("Unable to determine U-Boot version from {}".format(version))

    def _check_return_code(self):
        self.write("echo ~~~$?~~~\n")
        (response, index) = self.wait_for("^~~~[0-9]+~~~[\r\n]")
        return_code = int(response[-1][3:-3])
        if return_code != 0:
            raise Exception("{} had non-zero result: {}".format(command, response))

    def linux_command(self, command, timeout=None):
        res = self.run_command(command, timeout=timeout)
        # Strip out anything that looks like a kernel message, ie:
        # [   64.011533] random: crng init done
        good = []
        for line in res:
            if not re.match("^\[ *[0-9\.]+\]", line):
                good.append(line)

        self._check_return_code()

        return good

    def linux_send_text_file(self, local_file, remote_file):
        self.absorb_outstanding()
        with open(local_file, "rb") as stream:
            self.write("cat > {}\n".format(remote_file))
            self.write(stream.read())
            self.write("\n")
            self.write("\x04")
        self.absorb_outstanding()
        self._check_return_code()

    def linux_xmodem_upload(self, local_file, remote_file, callback=None):
        """Load a given local file to the given remote file over the serial port
        callback: Callback function to indicate progress. called as callback(position, total_size)"""
        start = time.time()
        size = 0

        def xmodem_callback(total_packets, success_count, error_count):
            # Adjust packet sizes to byte offsets
            pos = min(total_packets * 1024, size)
            callback(pos, size)

        with open(local_file, "rb") as stream:
            size = os.path.getsize(local_file)
            if callback:
                callback(0, size)
            self.write("rx %s\n" % (remote_file))
            self.readline()
            # self.wait_for("C")
            print("starting transfer")
            modem = xmodem.XMODEM(self._getc, self._putc, mode="xmodem1k")
            if not modem.send(stream, callback=xmodem_callback if callback else None):
                raise Exception("Failed to send {}".format(local_file))
        duration = time.time() - start
        if not duration:
            duration = 1
        print(
            "{} {:.2f}s to transfer {:.0f}kB: {:.2f}kB/s".format(
                os.path.basename(local_file), duration, size / 1024, (size / 1024) / duration
            )
        )
        self.wait_for_prompt()

        # Check MD5sum of local against remote
        md5sum = self.linux_command("md5sum {}".format(remote_file))[0].split(" ")[0]

        with open(local_file, "rb") as stream:
            file_hash = hashlib.md5()
            while chunk := stream.read(8192):
                file_hash.update(chunk)
            if file_hash.hexdigest() != md5sum:
                raise Exception("MD5 checksum on {} doesn't match".format(local_file))

    def linux_set_baudrate(self, baudrate):
        self.absorb_outstanding()
        self.slow_write("stty {}\n".format(baudrate))
        self._serial.baudrate = baudrate
        self.wait_for_prompt(send_ctrl_c=True)
        time.sleep(1)
        self.absorb_outstanding()
