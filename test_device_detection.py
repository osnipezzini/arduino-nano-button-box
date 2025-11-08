#!/usr/bin/env python3
"""
Test script for USB device detection
Useful for debugging device detection issues
"""

import subprocess
import json
import sys
from typing import List, Dict, Optional


class DeviceDetectionTester:
    """Test USB device detection"""
    
    @staticmethod
    def get_all_usb_devices() -> List[Dict]:
        """Get all USB devices"""
        try:
            ps_cmd = """
            Get-WmiObject Win32_PnPEntity | Where-Object {
                $_.DeviceID -match "USB"
            } | Select-Object Name, Description, DeviceID, Status | ConvertTo-Json
            """
            
            result = subprocess.run(
                ["powershell", "-Command", ps_cmd],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0 and result.stdout.strip():
                try:
                    data = json.loads(result.stdout)
                    if isinstance(data, list):
                        return data
                    return [data] if data else []
                except json.JSONDecodeError:
                    return []
            
            return []
        except Exception as e:
            print(f"Error getting USB devices: {e}")
            return []
    
    @staticmethod
    def find_device_by_vid_pid(vendor_id: str, product_id: str) -> Optional[Dict]:
        """Find specific device by VID/PID"""
        try:
            vid = int(vendor_id.replace("0x", ""), 16)
            pid = int(product_id.replace("0x", ""), 16)
            
            ps_cmd = f"""
            $devices = Get-WmiObject Win32_PnPEntity | Where-Object {{
                $_.DeviceID -match "VID_{vid:04X}" -and $_.DeviceID -match "PID_{pid:04X}"
            }}
            
            if ($devices) {{
                $devices | Select-Object Name, Description, DeviceID, Status | ConvertTo-Json
            }}
            """
            
            result = subprocess.run(
                ["powershell", "-Command", ps_cmd],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0 and result.stdout.strip():
                try:
                    data = json.loads(result.stdout)
                    if isinstance(data, list):
                        return data[0] if data else None
                    return data
                except json.JSONDecodeError:
                    return None
            
            return None
        except Exception as e:
            print(f"Error finding device: {e}")
            return None
    
    @staticmethod
    def parse_device_id(device_id: str) -> Dict:
        """Parse Windows device ID to extract VID/PID"""
        parts = device_id.split("\\")
        info = {
            "full_id": device_id,
            "vendor_id": None,
            "product_id": None,
            "serial": None
        }
        
        for part in parts:
            if part.startswith("VID_"):
                info["vendor_id"] = f"0x{part[4:8]}"
            elif part.startswith("PID_"):
                info["product_id"] = f"0x{part[4:8]}"
        
        return info
    
    @staticmethod
    def test_detection():
        """Run detection tests"""
        print("=" * 70)
        print("USB Device Detection Test")
        print("=" * 70)
        
        # Get all USB devices
        print("\n1. Scanning all USB devices...")
        print("-" * 70)
        
        devices = DeviceDetectionTester.get_all_usb_devices()
        
        if devices:
            print(f"Found {len(devices)} USB device(s):\n")
            
            for i, device in enumerate(devices, 1):
                print(f"{i}. {device.get('Name', 'Unknown')}")
                print(f"   Description: {device.get('Description', 'N/A')}")
                print(f"   Status: {device.get('Status', 'Unknown')}")
                
                device_id = device.get('DeviceID', '')
                if device_id:
                    parsed = DeviceDetectionTester.parse_device_id(device_id)
                    if parsed['vendor_id']:
                        print(f"   Vendor ID: {parsed['vendor_id']}")
                    if parsed['product_id']:
                        print(f"   Product ID: {parsed['product_id']}")
                    print(f"   Device ID: {device_id}")
                
                print()
        else:
            print("No USB devices found")
        
        # Test specific device detection
        print("\n2. Testing specific device detection...")
        print("-" * 70)
        
        test_cases = [
            ("0x16c0", "0x05df", "V-USB Button Box (Default)"),
            ("0x2341", "0x0043", "Arduino Uno"),
            ("0x2341", "0x0243", "Arduino Micro"),
        ]
        
        for vendor_id, product_id, description in test_cases:
            print(f"\nSearching for {description}")
            print(f"  VID: {vendor_id}, PID: {product_id}")
            
            device = DeviceDetectionTester.find_device_by_vid_pid(vendor_id, product_id)
            
            if device:
                print(f"  ✓ Found: {device.get('Name', 'Unknown')}")
                print(f"    Status: {device.get('Status', 'Unknown')}")
            else:
                print(f"  ✗ Not found (not connected or not detected)")
        
        # Interactive search
        print("\n3. Interactive device search...")
        print("-" * 70)
        
        try:
            vendor_id = input("\nEnter Vendor ID (hex, e.g., 0x16c0): ").strip()
            product_id = input("Enter Product ID (hex, e.g., 0x05df): ").strip()
            
            if vendor_id and product_id:
                print(f"\nSearching for VID={vendor_id}, PID={product_id}...")
                
                device = DeviceDetectionTester.find_device_by_vid_pid(vendor_id, product_id)
                
                if device:
                    print("\n✓ Device found!")
                    print(f"  Name: {device.get('Name', 'Unknown')}")
                    print(f"  Description: {device.get('Description', 'N/A')}")
                    print(f"  Status: {device.get('Status', 'Unknown')}")
                    print(f"  Device ID: {device.get('DeviceID', 'N/A')}")
                else:
                    print("\n✗ Device not found")
                    print("  Make sure the device is connected and recognized by Windows")
        except KeyboardInterrupt:
            print("\nSkipped interactive search")
        
        print("\n" + "=" * 70)
        print("Test complete!")
        print("=" * 70)


def main():
    """Main entry point"""
    if sys.platform != "win32":
        print("Error: This test script requires Windows")
        print("It uses PowerShell and WMI which are Windows-specific")
        sys.exit(1)
    
    try:
        tester = DeviceDetectionTester()
        tester.test_detection()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
