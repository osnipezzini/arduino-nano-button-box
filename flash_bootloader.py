#!/usr/bin/env python3
"""
V-USB Bootloader Flasher
Flash compiled bootloader to Arduino boards via ISP programmer
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import Optional, List

# MCU Fuse Configurations for V-USB
MCU_FUSES = {
    "atmega328p": {
        "low": "0xdf",
        "high": "0xda",
        "extended": "0x05",
        "lock": "0x0f",
        "unlock": "0x3f"
    },
    "atmega32u4": {
        "low": "0xdf",
        "high": "0xd9",
        "extended": "0xc3",
        "lock": "0x0f",
        "unlock": "0x3f"
    },
    "attiny85": {
        "low": "0xe1",
        "high": "0xdd",
        "extended": "0xff",
        "lock": "0x0f",
        "unlock": "0x3f"
    }
}

class BootloaderFlasher:
    def __init__(self, programmer: str = "avrisp", port: str = None, baud: int = 19200):
        self.programmer = programmer
        self.port = port
        self.baud = baud
    
    def check_avrdude(self) -> bool:
        """Check if avrdude is installed"""
        if subprocess.run(["which", "avrdude"], capture_output=True).returncode != 0:
            print("❌ avrdude not found!")
            print("\nInstall with:")
            print("  Ubuntu/Debian: sudo apt-get install avrdude")
            print("  macOS: brew install avrdude")
            print("  Windows: Install Arduino IDE or WinAVR")
            return False
        print("✅ avrdude found")
        return True
    
    def detect_ports(self) -> List[str]:
        """Detect available serial ports"""
        ports = []
        try:
            result = subprocess.run(["avrdude", "-c", self.programmer, "-P", "?", "-p", "m328p"],
                                  capture_output=True, text=True)
            # Parse output for available ports
            for line in result.stderr.split('\n'):
                if 'Available' in line or '/dev/' in line or 'COM' in line:
                    ports.append(line.strip())
        except:
            pass
        return ports
    
    def backup_bootloader(self, mcu: str, output_file: str) -> bool:
        """Backup current bootloader before flashing"""
        print(f"\n📦 Backing up current bootloader...")
        
        cmd = [
            "avrdude",
            "-c", self.programmer,
            "-p", mcu,
            "-P", self.port,
            "-b", str(self.baud),
            "-U", f"flash:r:{output_file}:i"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"✅ Bootloader backed up to: {output_file}")
                return True
            else:
                print(f"⚠️  Backup failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Backup error: {e}")
            return False
    
    def flash_bootloader(self, mcu: str, hex_file: str, verify: bool = True) -> bool:
        """Flash bootloader to device"""
        print(f"\n🔥 Flashing bootloader...")
        print(f"   MCU: {mcu}")
        print(f"   File: {hex_file}")
        print(f"   Programmer: {self.programmer}")
        print(f"   Port: {self.port}")
        
        if not Path(hex_file).exists():
            print(f"❌ Hex file not found: {hex_file}")
            return False
        
        cmd = [
            "avrdude",
            "-c", self.programmer,
            "-p", mcu,
            "-P", self.port,
            "-b", str(self.baud),
            "-U", f"flash:w:{hex_file}:i"
        ]
        
        if verify:
            cmd.append("-v")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            print(result.stdout)
            
            if result.returncode == 0:
                print(f"✅ Bootloader flashed successfully!")
                return True
            else:
                print(f"❌ Flash failed!")
                print(f"Error: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("❌ Flash timeout")
            return False
        except Exception as e:
            print(f"❌ Flash error: {e}")
            return False
    
    def set_fuses(self, mcu: str, fuses: dict = None) -> bool:
        """Set MCU fuses for V-USB"""
        if fuses is None:
            if mcu not in MCU_FUSES:
                print(f"❌ Unknown MCU: {mcu}")
                return False
            fuses = MCU_FUSES[mcu]
        
        print(f"\n⚙️  Setting fuses for {mcu}...")
        print(f"   Low:      {fuses['low']}")
        print(f"   High:     {fuses['high']}")
        print(f"   Extended: {fuses['extended']}")
        
        commands = [
            f"lfuse:w:{fuses['low']}:m",
            f"hfuse:w:{fuses['high']}:m",
            f"efuse:w:{fuses['extended']}:m"
        ]
        
        for cmd_str in commands:
            cmd = [
                "avrdude",
                "-c", self.programmer,
                "-p", mcu,
                "-P", self.port,
                "-b", str(self.baud),
                "-U", cmd_str
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode != 0:
                    print(f"❌ Fuse setting failed: {cmd_str}")
                    print(f"Error: {result.stderr}")
                    return False
                print(f"✅ {cmd_str}")
            except Exception as e:
                print(f"❌ Error setting {cmd_str}: {e}")
                return False
        
        print(f"✅ All fuses set successfully!")
        return True
    
    def verify_flash(self, mcu: str, hex_file: str) -> bool:
        """Verify bootloader was flashed correctly"""
        print(f"\n✔️  Verifying bootloader...")
        
        cmd = [
            "avrdude",
            "-c", self.programmer,
            "-p", mcu,
            "-P", self.port,
            "-b", str(self.baud),
            "-U", f"flash:v:{hex_file}:i"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print(f"✅ Verification successful!")
                return True
            else:
                print(f"❌ Verification failed!")
                print(f"Error: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Verification error: {e}")
            return False
    
    def full_flash_sequence(self, mcu: str, hex_file: str, backup: bool = True, 
                           set_fuses: bool = True) -> bool:
        """Execute full flash sequence"""
        print(f"\n{'='*60}")
        print(f"V-USB Bootloader Flash Sequence")
        print(f"{'='*60}")
        
        if backup:
            backup_file = f"bootloader_backup_{mcu}.hex"
            if not self.backup_bootloader(mcu, backup_file):
                print("⚠️  Backup failed, continuing anyway...")
        
        if set_fuses:
            if not self.set_fuses(mcu):
                print("❌ Fuse setting failed, aborting")
                return False
        
        if not self.flash_bootloader(mcu, hex_file):
            return False
        
        if not self.verify_flash(mcu, hex_file):
            print("⚠️  Verification failed, but bootloader may still work")
        
        print(f"\n{'='*60}")
        print(f"✅ Flash sequence completed!")
        print(f"{'='*60}")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="V-USB Bootloader Flasher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Flash bootloader to Arduino Nano via ISP on COM3
  python3 flash_bootloader.py --mcu atmega328p --hex bootloader_nano.hex --port COM3
  
  # Flash with full sequence (backup, fuses, verify)
  python3 flash_bootloader.py --mcu atmega328p --hex bootloader_nano.hex --port /dev/ttyUSB0 --full
  
  # Detect available ports
  python3 flash_bootloader.py --detect-ports
  
  # Backup current bootloader
  python3 flash_bootloader.py --mcu atmega328p --port COM3 --backup bootloader_backup.hex
        """
    )
    
    parser.add_argument("--mcu", choices=MCU_FUSES.keys(),
                       help="Target MCU")
    parser.add_argument("--hex", help="Bootloader hex file to flash")
    parser.add_argument("--port", help="Serial port (COM3, /dev/ttyUSB0, etc)")
    parser.add_argument("--programmer", default="avrisp",
                       help="Programmer type (default: avrisp)")
    parser.add_argument("--baud", type=int, default=19200,
                       help="Baud rate (default: 19200)")
    parser.add_argument("--full", action="store_true",
                       help="Execute full sequence (backup, fuses, flash, verify)")
    parser.add_argument("--backup", metavar="FILE",
                       help="Backup current bootloader to file")
    parser.add_argument("--set-fuses", action="store_true",
                       help="Set MCU fuses for V-USB")
    parser.add_argument("--verify", action="store_true",
                       help="Verify bootloader after flashing")
    parser.add_argument("--detect-ports", action="store_true",
                       help="Detect available serial ports")
    parser.add_argument("--check-deps", action="store_true",
                       help="Check if avrdude is installed")
    
    args = parser.parse_args()
    
    try:
        flasher = BootloaderFlasher(args.programmer, args.port, args.baud)
        
        if args.check_deps:
            if flasher.check_avrdude():
                return 0
            else:
                return 1
        
        if args.detect_ports:
            ports = flasher.detect_ports()
            if ports:
                print("\nDetected ports:")
                for port in ports:
                    print(f"  {port}")
            else:
                print("No ports detected")
            return 0
        
        if args.backup:
            if not args.mcu or not args.port:
                print("❌ Error: --mcu and --port required for backup")
                return 1
            if flasher.backup_bootloader(args.mcu, args.backup):
                return 0
            else:
                return 1
        
        if args.full or args.hex:
            if not args.mcu or not args.port:
                print("❌ Error: --mcu and --port required")
                return 1
            
            if not args.hex and not args.full:
                print("❌ Error: --hex required")
                return 1
            
            if args.full:
                if flasher.full_flash_sequence(args.mcu, args.hex):
                    return 0
                else:
                    return 1
            else:
                if flasher.flash_bootloader(args.mcu, args.hex, verify=args.verify):
                    return 0
                else:
                    return 1
        
        parser.print_help()
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
