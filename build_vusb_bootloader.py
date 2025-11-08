#!/usr/bin/env python3
"""
V-USB Bootloader Builder for Arduino Boards
Compiles V-USB firmware with customizable device name and MCU support
"""

import os
import sys
import subprocess
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Optional

# MCU Configurations
MCU_CONFIGS = {
    "nano": {
        "mcu": "atmega328p",
        "f_cpu": "16000000",
        "usb_port": "B",
        "usb_bit_d_plus": "4",
        "usb_bit_d_minus": "3",
        "description": "Arduino Nano (ATmega328P)"
    },
    "micro": {
        "mcu": "atmega32u4",
        "f_cpu": "16000000",
        "usb_port": "D",
        "usb_bit_d_plus": "4",
        "usb_bit_d_minus": "3",
        "description": "Arduino Micro (ATmega32U4)"
    },
    "leonardo": {
        "mcu": "atmega32u4",
        "f_cpu": "16000000",
        "usb_port": "D",
        "usb_bit_d_plus": "4",
        "usb_bit_d_minus": "3",
        "description": "Arduino Leonardo (ATmega32U4)"
    },
    "uno": {
        "mcu": "atmega328p",
        "f_cpu": "16000000",
        "usb_port": "B",
        "usb_bit_d_plus": "4",
        "usb_bit_d_minus": "3",
        "description": "Arduino UNO (ATmega328P)"
    },
    "attiny85": {
        "mcu": "attiny85",
        "f_cpu": "16500000",
        "usb_port": "B",
        "usb_bit_d_plus": "4",
        "usb_bit_d_minus": "3",
        "description": "ATtiny85"
    }
}

class VUSBBootloaderBuilder:
    def __init__(self, vusb_path: str, output_dir: str = "bootloader_builds"):
        self.vusb_path = Path(vusb_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        if not self.vusb_path.exists():
            raise FileNotFoundError(f"V-USB path not found: {vusb_path}")
    
    def check_dependencies(self) -> bool:
        """Check if required tools are installed"""
        required_tools = ["avr-gcc", "avr-objcopy", "make"]
        missing_tools = []
        
        for tool in required_tools:
            if shutil.which(tool) is None:
                missing_tools.append(tool)
        
        if missing_tools:
            print(f"❌ Missing required tools: {', '.join(missing_tools)}")
            print("\nInstall with:")
            print("  Ubuntu/Debian: sudo apt-get install gcc-avr avr-libc avrdude make")
            print("  macOS: brew install avr-gcc avrdude")
            print("  Windows: Install WinAVR or Arduino IDE")
            return False
        
        print("✅ All required tools found")
        return True
    
    def create_usbconfig(self, mcu: str, device_name: str, vendor_id: str = "0x16c0", 
                        product_id: str = "0x05df") -> str:
        """Create customized usbconfig.h"""
        
        if mcu not in MCU_CONFIGS:
            raise ValueError(f"Unknown MCU: {mcu}. Available: {', '.join(MCU_CONFIGS.keys())}")
        
        config = MCU_CONFIGS[mcu]
        
        # Truncate device name to fit USB descriptor (max 32 bytes)
        device_name = device_name[:32]
        device_name_len = len(device_name)
        
        # Create USB descriptor string
        device_descriptor = ", ".join([f"'{c}'" for c in device_name])
        
        usbconfig = f"""/* Name: usbconfig.h
 * Project: V-USB Bootloader for {config['description']}
 * Device Name: {device_name}
 * Auto-generated configuration
 */

#ifndef __usbconfig_h_included__
#define __usbconfig_h_included__

/* USB Vendor and Product ID */
#define USB_CFG_VENDOR_ID       {vendor_id}
#define USB_CFG_DEVICE_ID       {product_id}

/* Device Name String */
#define USB_CFG_DEVICE_NAME     "{device_name}"
#define USB_CFG_DEVICE_NAME_LEN {device_name_len}

/* MCU Configuration */
#define USB_CFG_IOPORTNAME      {config['usb_port']}
#define USB_CFG_DMINUS_BIT      {config['usb_bit_d_minus']}
#define USB_CFG_DPLUS_BIT       {config['usb_bit_d_plus']}

/* USB Speed */
#define USB_CFG_CLOCK_KHZ       (F_CPU/1000)

/* Features */
#define USB_CFG_HAS_INTRIN_ENDPOINT     1
#define USB_CFG_HAS_INTRIN_ENDPOINT3    0
#define USB_CFG_HAS_INTERRUPT_IN        1
#define USB_CFG_HAS_INTERRUPT_IN3       0
#define USB_CFG_SUPPRESS_INTR_CODE      0
#define USB_CFG_INTR_POLL_INTERVAL      10

/* Device Classes */
#define USB_CFG_IS_SELF_POWERED         0
#define USB_CFG_MAX_BUS_POWER           100
#define USB_CFG_IMPLEMENT_FN_WRITE      1
#define USB_CFG_IMPLEMENT_FN_READ       1
#define USB_CFG_IMPLEMENT_FN_WRITEOUT   0

/* Strings */
#define USB_CFG_HAVE_INTRIN_ENDPOINT    1
#define USB_CFG_HAVE_INTRIN_ENDPOINT3   0
#define USB_CFG_HAVE_INTERRUPT_IN       1
#define USB_CFG_HAVE_INTERRUPT_IN3      0

#define USB_CFG_LONG_TRANSFERS          1

#endif
"""
        return usbconfig
    
    def create_makefile(self, mcu: str, device_name: str) -> str:
        """Create customized Makefile for compilation"""
        
        if mcu not in MCU_CONFIGS:
            raise ValueError(f"Unknown MCU: {mcu}")
        
        config = MCU_CONFIGS[mcu]
        
        makefile = f"""# Makefile for V-USB Bootloader
# MCU: {config['description']}
# Device: {device_name}

MCU = {config['mcu']}
F_CPU = {config['f_cpu']}
FORMAT = ihex
TARGET = bootloader

OBJECTS = main.o usbdrv/usbdrv.o usbdrv/usbdrvasm.o oddebug.o

CFLAGS = -g -Os -Wall -Wextra -std=gnu99
CFLAGS += -mmcu=$(MCU) -DF_CPU=$(F_CPU)UL
CFLAGS += -fno-move-loop-invariants -fno-tree-scev-cprop -fno-inline-small-functions
CFLAGS += -fno-split-wide-types -fno-strict-aliasing -fshort-enums
CFLAGS += -Wall -Wstrict-prototypes
CFLAGS += -funsigned-char -funsigned-bitfields -fpack-struct

LDFLAGS = -Wl,--relax,--gc-sections

CC = avr-gcc
OBJCOPY = avr-objcopy
OBJDUMP = avr-objdump
SIZE = avr-size
AR = avr-ar
NM = avr-nm
AVRDUDE = avrdude
REMOVE = rm -f
REMOVEDIR = rm -rf

all: $(TARGET).hex $(TARGET).eep size

%.o: %.c
	$(CC) -c $(CFLAGS) -o $@ $<

%.o: %.S
	$(CC) -c $(CFLAGS) -o $@ $<

$(TARGET).elf: $(OBJECTS)
	$(CC) $(LDFLAGS) -o $@ $^

$(TARGET).hex: $(TARGET).elf
	$(OBJCOPY) -O $(FORMAT) -R .eeprom $< $@

$(TARGET).eep: $(TARGET).elf
	-$(OBJCOPY) -j .eeprom --set-section-flags=.eeprom="alloc,load" \\
	--change-section-lma .eeprom=0 -O $(FORMAT) $< $@

size: $(TARGET).elf
	@$(SIZE) --format=avr --mcu=$(MCU) $(TARGET).elf

clean:
	$(REMOVE) $(TARGET).hex $(TARGET).eep $(TARGET).elf
	$(REMOVE) $(OBJECTS)
	$(REMOVE) $(TARGET).map

.PHONY: all clean size
"""
        return makefile
    
    def build(self, mcu: str, device_name: str, vendor_id: str = "0x16c0", 
              product_id: str = "0x05df") -> Optional[Path]:
        """Build bootloader for specified MCU"""
        
        print(f"\n{'='*60}")
        print(f"Building V-USB Bootloader")
        print(f"{'='*60}")
        print(f"MCU: {MCU_CONFIGS[mcu]['description']}")
        print(f"Device Name: {device_name}")
        print(f"Vendor ID: {vendor_id}")
        print(f"Product ID: {product_id}")
        print(f"{'='*60}\n")
        
        # Create build directory
        build_dir = self.output_dir / f"build_{mcu}_{device_name.replace(' ', '_')}"
        build_dir.mkdir(exist_ok=True)
        
        # Copy V-USB source files
        print("📋 Copying V-USB source files...")
        usbdrv_src = self.vusb_path / "usbdrv"
        usbdrv_dst = build_dir / "usbdrv"
        
        if usbdrv_dst.exists():
            shutil.rmtree(usbdrv_dst)
        shutil.copytree(usbdrv_src, usbdrv_dst)
        
        # Create usbconfig.h
        print("⚙️  Creating usbconfig.h...")
        usbconfig_content = self.create_usbconfig(mcu, device_name, vendor_id, product_id)
        usbconfig_path = build_dir / "usbconfig.h"
        usbconfig_path.write_text(usbconfig_content)
        
        # Create Makefile
        print("📝 Creating Makefile...")
        makefile_content = self.create_makefile(mcu, device_name)
        makefile_path = build_dir / "Makefile"
        makefile_path.write_text(makefile_content)
        
        # Copy main.c and other source files
        print("📋 Copying firmware source...")
        shutil.copy(self.vusb_path / "examples" / "hid-data" / "firmware" / "main.c", 
                   build_dir / "main.c")
        
        # Try to copy oddebug files if they exist
        oddebug_src = self.vusb_path / "examples" / "hid-data" / "firmware" / "oddebug.c"
        if oddebug_src.exists():
            shutil.copy(oddebug_src, build_dir / "oddebug.c")
            shutil.copy(self.vusb_path / "examples" / "hid-data" / "firmware" / "oddebug.h", 
                       build_dir / "oddebug.h")
        else:
            # Create minimal oddebug files
            (build_dir / "oddebug.c").write_text(
                "#include \"oddebug.h\"\nvoid odDebugInit(void) {}\n"
            )
            (build_dir / "oddebug.h").write_text(
                "#ifndef __oddebug_h_included__\n"
                "#define __oddebug_h_included__\n"
                "#define odDebugInit()\n"
                "#define DBG1(x,y,z)\n"
                "#endif\n"
            )
        
        # Compile
        print("🔨 Compiling bootloader...")
        try:
            result = subprocess.run(
                ["make", "clean", "all"],
                cwd=build_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                print(f"❌ Compilation failed!")
                print(f"STDOUT:\n{result.stdout}")
                print(f"STDERR:\n{result.stderr}")
                return None
            
            print(result.stdout)
            
            # Check if hex file was created
            hex_file = build_dir / "bootloader.hex"
            if hex_file.exists():
                print(f"\n✅ Bootloader compiled successfully!")
                print(f"📦 Output: {hex_file}")
                
                # Copy to output directory
                output_hex = self.output_dir / f"bootloader_{mcu}_{device_name.replace(' ', '_')}.hex"
                shutil.copy(hex_file, output_hex)
                print(f"💾 Saved to: {output_hex}")
                
                return output_hex
            else:
                print(f"❌ Hex file not created")
                return None
                
        except subprocess.TimeoutExpired:
            print("❌ Compilation timeout")
            return None
        except Exception as e:
            print(f"❌ Compilation error: {e}")
            return None
    
    def list_mcus(self):
        """List available MCU configurations"""
        print("\nAvailable MCU Configurations:")
        print("-" * 60)
        for key, config in MCU_CONFIGS.items():
            print(f"  {key:12} - {config['description']}")
        print("-" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="V-USB Bootloader Builder for Arduino Boards",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build for Arduino Nano with custom name
  python3 build_vusb_bootloader.py --mcu nano --name "Button Box"
  
  # Build for Arduino Micro
  python3 build_vusb_bootloader.py --mcu micro --name "Game Controller"
  
  # List available MCUs
  python3 build_vusb_bootloader.py --list-mcus
        """
    )
    
    parser.add_argument("--vusb-path", default="v-usb",
                       help="Path to V-USB source (default: v-usb)")
    parser.add_argument("--output-dir", default="bootloader_builds",
                       help="Output directory for compiled bootloaders (default: bootloader_builds)")
    parser.add_argument("--mcu", choices=MCU_CONFIGS.keys(),
                       help="Target MCU (required unless --list-mcus)")
    parser.add_argument("--name", default="Arduino Device",
                       help="USB device name (max 32 chars, default: Arduino Device)")
    parser.add_argument("--vendor-id", default="0x16c0",
                       help="USB Vendor ID (default: 0x16c0 - V-USB shared ID)")
    parser.add_argument("--product-id", default="0x05df",
                       help="USB Product ID (default: 0x05df - V-USB shared ID)")
    parser.add_argument("--list-mcus", action="store_true",
                       help="List available MCU configurations")
    parser.add_argument("--check-deps", action="store_true",
                       help="Check if required dependencies are installed")
    
    args = parser.parse_args()
    
    try:
        builder = VUSBBootloaderBuilder(args.vusb_path, args.output_dir)
        
        if args.list_mcus:
            builder.list_mcus()
            return 0
        
        if args.check_deps:
            if builder.check_dependencies():
                return 0
            else:
                return 1
        
        if not args.mcu:
            parser.print_help()
            print("\n❌ Error: --mcu is required (unless using --list-mcus)")
            return 1
        
        if not builder.check_dependencies():
            return 1
        
        hex_file = builder.build(args.mcu, args.name, args.vendor_id, args.product_id)
        
        if hex_file:
            print(f"\n✅ Build successful!")
            print(f"Next steps:")
            print(f"  1. Use avrdude to flash: bootloader_{args.mcu}.hex")
            print(f"  2. Or use Arduino IDE with custom board definition")
            return 0
        else:
            print(f"\n❌ Build failed")
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
