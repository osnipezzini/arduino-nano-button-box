#!/usr/bin/env python3
"""
Generate customized V-USB driver package with INF file
"""

import argparse
import shutil
import sys
from pathlib import Path
from typing import Optional


class VUSBDriverGenerator:
    """Generate customized V-USB driver packages"""
    
    def __init__(self, output_dir: str = "vusb_drivers"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.template_path = Path(__file__).parent / "vusb_driver_template.inf"
    
    def generate_inf(self, device_name: str, vendor_id: str, product_id: str,
                     manufacturer: str = "V-USB Project") -> str:
        """Generate INF file content"""
        
        # Ensure vendor_id and product_id are in correct format (without 0x)
        vendor_id = vendor_id.replace("0x", "").upper()
        product_id = product_id.replace("0x", "").upper()
        
        # Pad to 4 digits
        vendor_id = vendor_id.zfill(4)
        product_id = product_id.zfill(4)
        
        inf_content = f"""[Version]
Signature="$Windows NT$"
Class=USB
ClassGuid={{36FC9E60-C465-11CF-8056-444553540000}}
Provider=%MANUFACTURER%
DriverVer=01/01/2024,1.0.0.0
CatalogFile=vusb_driver.cat

[Manufacturer]
%MANUFACTURER%=Devices,NT,NTx86

[Devices.NT]
%DEVICE_NAME%=USB_Install, USB\VID_{vendor_id}&PID_{product_id}

[Devices.NTx86]
%DEVICE_NAME%=USB_Install, USB\VID_{vendor_id}&PID_{product_id}

[USB_Install.NT]
Include=winusb.inf
Needs=WinUSB.NT

[USB_Install.NT.Services]
Include=winusb.inf
AddService=WinUSB,0x00000002,WinUSB_ServiceInstall

[WinUSB_ServiceInstall]
DisplayName="WinUSB Driver"
ServiceType=1
StartType=3
ErrorControl=1
ServiceBinary=%12%\WinUSB.sys

[USB_Install.NT.Wmi]
Include=winusb.inf
Needs=WinUSB.NT.Wmi

[USB_Install.NT.CoInstallers]
AddReg=CoInstallers_AddReg
CopyFiles=CoInstallers_CopyFiles

[CoInstallers_AddReg]
HKR,,CoInstallers32,0x00010000,"WinUSBCoInstaller.dll"

[CoInstallers_CopyFiles]
WinUSBCoInstaller.dll

[DestinationDirs]
CoInstallers_CopyFiles=11

[SourceDisksNames]
1="V-USB Driver Installation Disk"

[SourceDisksFiles]
WinUSBCoInstaller.dll=1

[Strings]
MANUFACTURER="{manufacturer}"
DEVICE_NAME="{device_name}"
VENDOR_ID={vendor_id}
PRODUCT_ID={product_id}
"""
        return inf_content
    
    def generate_driver_package(self, device_name: str, vendor_id: str, product_id: str,
                               manufacturer: str = "V-USB Project",
                               include_readme: bool = True) -> Optional[Path]:
        """Generate complete driver package"""
        
        # Create driver directory
        safe_name = device_name.replace(" ", "_").replace("/", "_")
        driver_dir = self.output_dir / f"vusb_driver_{safe_name}"
        driver_dir.mkdir(exist_ok=True)
        
        print(f"Generating driver package: {driver_dir}")
        
        # Generate INF file
        inf_content = self.generate_inf(device_name, vendor_id, product_id, manufacturer)
        inf_file = driver_dir / "vusb_driver.inf"
        inf_file.write_text(inf_content)
        print(f"✓ Created: {inf_file.name}")
        
        # Create README
        if include_readme:
            readme_content = f"""# V-USB Driver for {device_name}

## Device Information
- **Manufacturer**: {manufacturer}
- **Name**: {device_name}
- **Vendor ID**: {vendor_id}
- **Product ID**: {product_id}

## Installation Instructions

### Automatic Installation (Recommended)
1. Run `V-USB Driver Installer.exe`
2. Select your device from the dropdown
3. Click "Detect Device"
4. Click "Install Driver"

### Manual Installation
1. Connect your device to USB
2. Open Device Manager (Win+X → Device Manager)
3. Look for an unknown device with VID {vendor_id.replace('0x', '')} and PID {product_id.replace('0x', '')}
4. Right-click → Update driver
5. Choose "Browse my computer for driver software"
6. Select this folder
7. Click "Next" and follow the prompts

### Manual Installation (Windows 10/11)
1. Open PowerShell as Administrator
2. Run: `pnputil /add-driver vusb_driver.inf /install`

## Troubleshooting

### Device not detected
- Ensure the device is properly connected
- Try a different USB port
- Check Device Manager for unknown devices

### Installation fails
- Run as Administrator
- Disable driver signature enforcement (Windows 10/11)
- Try manual installation steps above

### Driver signature enforcement
On Windows 10/11, you may need to disable driver signature enforcement:
1. Hold Shift and click Restart
2. Select Troubleshoot → Advanced options → Startup Settings
3. Press F7 to disable driver signature enforcement
4. Restart and try installation again

## Support
For issues or questions, visit: https://www.obdev.at/products/vusb/

## License
V-USB is licensed under the GNU General Public License (GPL).
See LICENSE file for details.
"""
            readme_file = driver_dir / "README.txt"
            readme_file.write_text(readme_content)
            print(f"✓ Created: {readme_file.name}")
        
        # Create installation batch script
        batch_content = f"""@echo off
REM V-USB Driver Installation Script
REM Device: {device_name}

echo Installing V-USB Driver for {device_name}...
echo.

REM Check for admin privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: This script requires administrator privileges.
    echo Please run as Administrator.
    pause
    exit /b 1
)

REM Install driver
echo Installing driver...
pnputil /add-driver vusb_driver.inf /install

if %errorlevel% equ 0 (
    echo.
    echo Success! Driver installed.
    echo Please reconnect your device.
) else (
    echo.
    echo Error: Installation failed.
    echo Try manual installation or disable driver signature enforcement.
)

pause
"""
        batch_file = driver_dir / "install_driver.bat"
        batch_file.write_text(batch_content)
        print(f"✓ Created: {batch_file.name}")
        
        print(f"\n✓ Driver package created: {driver_dir}")
        return driver_dir
    
    def list_packages(self):
        """List generated driver packages"""
        packages = list(self.output_dir.glob("vusb_driver_*"))
        
        if not packages:
            print("No driver packages found")
            return
        
        print(f"\nGenerated driver packages ({len(packages)}):")
        for pkg in sorted(packages):
            inf_files = list(pkg.glob("*.inf"))
            if inf_files:
                print(f"  • {pkg.name}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Generate customized V-USB driver packages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  # Generate driver for Button Box (padrão)
  python3 generate_vusb_driver.py --name "Button Box"
  
  # Generate driver com manufacturer customizado
  python3 generate_vusb_driver.py --name "Omega Buttons" --manufacturer "SODevs"
  
  # Generate driver com VID/PID customizados
  python3 generate_vusb_driver.py --name "Device 1" --manufacturer "SODevs" \\
      --vendor-id 0x1234 --product-id 0x5678
  
  # Generate múltiplos devices com IDs diferentes
  python3 generate_vusb_driver.py --name "Omega Buttons V1" --manufacturer "SODevs" \\
      --vendor-id 0x16c0 --product-id 0x05df
  python3 generate_vusb_driver.py --name "Omega Buttons V2" --manufacturer "SODevs" \\
      --vendor-id 0x16c0 --product-id 0x05e0
  
  # List generated packages
  python3 generate_vusb_driver.py --list
        """
    )
    
    parser.add_argument("--name", default="Arduino Device",
                       help="Device name (default: Arduino Device)")
    parser.add_argument("--manufacturer", default="V-USB Project",
                       help="Manufacturer name (default: V-USB Project)")
    parser.add_argument("--vendor-id", default="0x16c0",
                       help="USB Vendor ID (default: 0x16c0)")
    parser.add_argument("--product-id", default="0x05df",
                       help="USB Product ID (default: 0x05df)")
    parser.add_argument("--output-dir", default="vusb_drivers",
                       help="Output directory (default: vusb_drivers)")
    parser.add_argument("--list", action="store_true",
                       help="List generated packages")
    
    args = parser.parse_args()
    
    try:
        generator = VUSBDriverGenerator(args.output_dir)
        
        if args.list:
            generator.list_packages()
            return 0
        
        driver_dir = generator.generate_driver_package(
            args.name,
            args.vendor_id,
            args.product_id,
            args.manufacturer
        )
        
        if driver_dir:
            print(f"\n📦 Driver package ready for distribution!")
            print(f"Location: {driver_dir}")
            return 0
        else:
            print("✗ Failed to generate driver package")
            return 1
            
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
