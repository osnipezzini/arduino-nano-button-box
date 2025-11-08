#!/usr/bin/env python3
"""
Configuration loader for V-USB Driver Installer
Loads device configurations from JSON file
"""

import json
from pathlib import Path
from typing import Dict, Optional, Any


class ConfigLoader:
    """Load and manage configuration"""
    
    DEFAULT_CONFIG_FILE = "device_config.json"
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = Path(config_file or self.DEFAULT_CONFIG_FILE)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        if not self.config_file.exists():
            print(f"Warning: Config file not found: {self.config_file}")
            return self._get_default_config()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing config file: {e}")
            return self._get_default_config()
        except Exception as e:
            print(f"Error loading config file: {e}")
            return self._get_default_config()
    
    @staticmethod
    def _get_default_config() -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "devices": {
                "Button Box": {
                    "vendor_id": "0x16c0",
                    "product_id": "0x05df",
                    "description": "Arduino Button Box (V-USB)"
                }
            },
            "driver_settings": {
                "auto_download": True,
                "timeout_seconds": 30,
                "require_admin": True
            },
            "ui_settings": {
                "window_width": 600,
                "window_height": 500
            }
        }
    
    def get_devices(self) -> Dict[str, Dict[str, str]]:
        """Get all configured devices"""
        return self.config.get("devices", {})
    
    def get_device(self, device_name: str) -> Optional[Dict[str, str]]:
        """Get specific device configuration"""
        devices = self.get_devices()
        return devices.get(device_name)
    
    def get_driver_settings(self) -> Dict[str, Any]:
        """Get driver settings"""
        return self.config.get("driver_settings", {})
    
    def get_ui_settings(self) -> Dict[str, Any]:
        """Get UI settings"""
        return self.config.get("ui_settings", {})
    
    def get_advanced_settings(self) -> Dict[str, Any]:
        """Get advanced settings"""
        return self.config.get("advanced", {})
    
    def add_device(self, device_name: str, vendor_id: str, product_id: str,
                   description: str = "", mcu: str = "", notes: str = "") -> bool:
        """Add new device to configuration"""
        if device_name in self.config.get("devices", {}):
            print(f"Device '{device_name}' already exists")
            return False
        
        if "devices" not in self.config:
            self.config["devices"] = {}
        
        self.config["devices"][device_name] = {
            "vendor_id": vendor_id,
            "product_id": product_id,
            "description": description or f"Custom {device_name}",
            "mcu": mcu or "atmega328p",
            "notes": notes or ""
        }
        
        return self.save_config()
    
    def remove_device(self, device_name: str) -> bool:
        """Remove device from configuration"""
        if device_name not in self.config.get("devices", {}):
            print(f"Device '{device_name}' not found")
            return False
        
        del self.config["devices"][device_name]
        return self.save_config()
    
    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def print_config(self):
        """Print configuration in readable format"""
        print("\n" + "="*70)
        print("Configuration Summary")
        print("="*70)
        
        # Devices
        print("\nDevices:")
        devices = self.get_devices()
        for name, config in devices.items():
            print(f"\n  {name}:")
            print(f"    Vendor ID: {config.get('vendor_id')}")
            print(f"    Product ID: {config.get('product_id')}")
            print(f"    Description: {config.get('description')}")
            if config.get('mcu'):
                print(f"    MCU: {config.get('mcu')}")
            if config.get('notes'):
                print(f"    Notes: {config.get('notes')}")
        
        # Driver Settings
        print("\n\nDriver Settings:")
        driver_settings = self.get_driver_settings()
        for key, value in driver_settings.items():
            print(f"  {key}: {value}")
        
        # UI Settings
        print("\n\nUI Settings:")
        ui_settings = self.get_ui_settings()
        for key, value in ui_settings.items():
            print(f"  {key}: {value}")
        
        print("\n" + "="*70 + "\n")


def main():
    """Test configuration loader"""
    import sys
    
    print("V-USB Driver Installer - Configuration Loader")
    print("="*70)
    
    loader = ConfigLoader()
    
    # Print current configuration
    loader.print_config()
    
    # Interactive menu
    while True:
        print("\nOptions:")
        print("1. List devices")
        print("2. Add device")
        print("3. Remove device")
        print("4. Show full config")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            print("\nConfigured devices:")
            for name, config in loader.get_devices().items():
                print(f"  • {name}: {config.get('description')}")
        
        elif choice == "2":
            name = input("Device name: ").strip()
            vid = input("Vendor ID (e.g., 0x16c0): ").strip()
            pid = input("Product ID (e.g., 0x05df): ").strip()
            desc = input("Description: ").strip()
            
            if loader.add_device(name, vid, pid, desc):
                print("✓ Device added")
            else:
                print("✗ Failed to add device")
        
        elif choice == "3":
            name = input("Device name to remove: ").strip()
            if loader.remove_device(name):
                print("✓ Device removed")
            else:
                print("✗ Failed to remove device")
        
        elif choice == "4":
            loader.print_config()
        
        elif choice == "5":
            print("Exiting...")
            break
        
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
