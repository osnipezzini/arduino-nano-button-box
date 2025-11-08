#!/usr/bin/env python3
"""
V-USB Driver Installer for Windows
Automatically detects and installs V-USB drivers for Arduino devices
"""

import os
import sys
import json
import ctypes
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import urllib.request
import urllib.error
import zipfile

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False

try:
    import winreg
    HAS_WINREG = True
except ImportError:
    HAS_WINREG = False


class DeviceConfig:
    """USB Device Configuration"""
    DEFAULT_CONFIGS = {
        "Button Box": {
            "vendor_id": "0x16c0",
            "product_id": "0x05df",
            "description": "Arduino Button Box (V-USB)"
        },
        "Arduino Device": {
            "vendor_id": "0x16c0",
            "product_id": "0x05df",
            "description": "Generic Arduino Device (V-USB)"
        }
    }


class WindowsDeviceManager:
    """Manages USB device detection on Windows"""
    
    @staticmethod
    def is_admin() -> bool:
        """Check if running with admin privileges"""
        try:
            return ctypes.windll.shell.IsUserAnAdmin()
        except:
            return False
    
    @staticmethod
    def get_device_list() -> List[Dict]:
        """Get list of USB devices using wmic"""
        try:
            output = subprocess.check_output(
                "wmic logicaldisk get name",
                shell=True,
                stderr=subprocess.DEVNULL,
                text=True
            )
            
            # Try using PowerShell for better USB device detection
            ps_cmd = """
            Get-WmiObject Win32_USBControllerDevice | ForEach-Object {
                [wmi]$hub = $_
                $hub.Dependent
            } | Select-Object Name, Description, DeviceID | ConvertTo-Json
            """
            
            try:
                result = subprocess.run(
                    ["powershell", "-Command", ps_cmd],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0 and result.stdout:
                    return json.loads(result.stdout)
            except:
                pass
            
            return []
        except Exception as e:
            print(f"Error getting device list: {e}")
            return []
    
    @staticmethod
    def find_device_by_id(vendor_id: str, product_id: str) -> Optional[Dict]:
        """Find device by Vendor ID and Product ID"""
        try:
            # Convert hex strings to decimal
            vid = int(vendor_id, 16)
            pid = int(product_id, 16)
            
            # Use PowerShell to find the device
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
                timeout=5
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
    def get_device_status(vendor_id: str, product_id: str) -> Tuple[bool, str]:
        """Check if device is detected and its status"""
        device = WindowsDeviceManager.find_device_by_id(vendor_id, product_id)
        
        if device:
            status = device.get("Status", "Unknown")
            return True, f"Found: {device.get('Name', 'Unknown')} - Status: {status}"
        
        return False, "Device not found"


class DriverInstaller:
    """Handles driver installation"""
    
    VUSB_DRIVER_URL = "https://www.obdev.at/files/vusb/usbdriver.zip"
    
    def __init__(self, temp_dir: Optional[Path] = None):
        self.temp_dir = temp_dir or Path(tempfile.gettempdir()) / "vusb_driver"
        self.temp_dir.mkdir(exist_ok=True)
    
    def download_driver(self, progress_callback=None) -> Optional[Path]:
        """Download V-USB driver"""
        try:
            driver_zip = self.temp_dir / "usbdriver.zip"
            
            if progress_callback:
                progress_callback("Downloading V-USB driver...")
            
            urllib.request.urlretrieve(self.VUSB_DRIVER_URL, driver_zip)
            
            if progress_callback:
                progress_callback("Extracting driver files...")
            
            with zipfile.ZipFile(driver_zip, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
            
            return self.temp_dir
        except Exception as e:
            print(f"Error downloading driver: {e}")
            return None
    
    def find_driver_files(self, driver_dir: Path) -> Optional[Path]:
        """Find driver .inf file"""
        try:
            # Look for .inf files
            inf_files = list(driver_dir.rglob("*.inf"))
            
            if inf_files:
                return inf_files[0].parent
            
            # Look for common driver directories
            for subdir in driver_dir.iterdir():
                if subdir.is_dir():
                    inf_files = list(subdir.glob("*.inf"))
                    if inf_files:
                        return subdir
            
            return None
        except Exception as e:
            print(f"Error finding driver files: {e}")
            return None
    
    def install_driver(self, driver_path: Path, progress_callback=None) -> bool:
        """Install driver using pnputil or dpinst"""
        try:
            if progress_callback:
                progress_callback("Installing driver...")
            
            # Find .inf file
            inf_files = list(driver_path.glob("*.inf"))
            if not inf_files:
                if progress_callback:
                    progress_callback("Error: No .inf file found")
                return False
            
            inf_file = inf_files[0]
            
            # Try using pnputil (Windows 7+)
            try:
                if progress_callback:
                    progress_callback(f"Installing {inf_file.name}...")
                
                result = subprocess.run(
                    ["pnputil", "/add-driver", str(inf_file), "/install"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    if progress_callback:
                        progress_callback("Driver installed successfully!")
                    return True
            except FileNotFoundError:
                pass
            
            # Fallback: Try using dpinst if available
            dpinst_path = driver_path / "dpinst.exe"
            if dpinst_path.exists():
                result = subprocess.run(
                    [str(dpinst_path)],
                    capture_output=True,
                    timeout=60
                )
                return result.returncode == 0
            
            if progress_callback:
                progress_callback("Error: Could not find installation tool")
            return False
            
        except Exception as e:
            if progress_callback:
                progress_callback(f"Error installing driver: {e}")
            return False
    
    def cleanup(self):
        """Clean up temporary files"""
        try:
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
        except Exception as e:
            print(f"Error cleaning up: {e}")


class DriverInstallerGUI:
    """GUI for driver installation"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("V-USB Driver Installer")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Check admin privileges
        if not WindowsDeviceManager.is_admin():
            messagebox.showwarning(
                "Admin Required",
                "This application requires administrator privileges.\n"
                "Please run it as Administrator."
            )
        
        self.installer = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup GUI elements"""
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title = ttk.Label(
            header_frame,
            text="V-USB Driver Installer",
            font=("Arial", 16, "bold")
        )
        title.pack()
        
        subtitle = ttk.Label(
            header_frame,
            text="Automatically detect and install V-USB drivers for Arduino devices"
        )
        subtitle.pack()
        
        # Device selection
        device_frame = ttk.LabelFrame(self.root, text="Device Configuration", padding=10)
        device_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(device_frame, text="Device:").grid(row=0, column=0, sticky=tk.W)
        self.device_var = tk.StringVar(value="Button Box")
        device_combo = ttk.Combobox(
            device_frame,
            textvariable=self.device_var,
            values=list(DeviceConfig.DEFAULT_CONFIGS.keys()),
            state="readonly"
        )
        device_combo.grid(row=0, column=1, sticky=tk.EW, padx=5)
        device_combo.bind("<<ComboboxSelected>>", self.on_device_changed)
        
        # Vendor/Product ID display
        ttk.Label(device_frame, text="Vendor ID:").grid(row=1, column=0, sticky=tk.W)
        self.vendor_id_var = tk.StringVar()
        ttk.Label(device_frame, textvariable=self.vendor_id_var).grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(device_frame, text="Product ID:").grid(row=2, column=0, sticky=tk.W)
        self.product_id_var = tk.StringVar()
        ttk.Label(device_frame, textvariable=self.product_id_var).grid(row=2, column=1, sticky=tk.W)
        
        device_frame.columnconfigure(1, weight=1)
        
        # Device status
        status_frame = ttk.LabelFrame(self.root, text="Device Status", padding=10)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_text = tk.Text(status_frame, height=4, width=60, state=tk.DISABLED)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.detect_btn = ttk.Button(
            button_frame,
            text="Detect Device",
            command=self.detect_device
        )
        self.detect_btn.pack(side=tk.LEFT, padx=5)
        
        self.install_btn = ttk.Button(
            button_frame,
            text="Install Driver",
            command=self.install_driver,
            state=tk.DISABLED
        )
        self.install_btn.pack(side=tk.LEFT, padx=5)
        
        self.browse_btn = ttk.Button(
            button_frame,
            text="Browse Driver...",
            command=self.browse_driver
        )
        self.browse_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress
        progress_frame = ttk.LabelFrame(self.root, text="Progress", padding=10)
        progress_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.progress_text = tk.Text(progress_frame, height=8, width=60)
        self.progress_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(progress_frame, orient=tk.VERTICAL, command=self.progress_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.progress_text.config(yscrollcommand=scrollbar.set)
        
        # Initialize
        self.on_device_changed()
    
    def on_device_changed(self, event=None):
        """Handle device selection change"""
        device_name = self.device_var.get()
        config = DeviceConfig.DEFAULT_CONFIGS.get(device_name, {})
        
        self.vendor_id_var.set(config.get("vendor_id", "0x16c0"))
        self.product_id_var.set(config.get("product_id", "0x05df"))
    
    def log_progress(self, message: str):
        """Log progress message"""
        self.progress_text.config(state=tk.NORMAL)
        self.progress_text.insert(tk.END, f"{message}\n")
        self.progress_text.see(tk.END)
        self.progress_text.config(state=tk.DISABLED)
        self.root.update()
    
    def detect_device(self):
        """Detect connected device"""
        self.progress_text.config(state=tk.NORMAL)
        self.progress_text.delete(1.0, tk.END)
        self.progress_text.config(state=tk.DISABLED)
        
        self.log_progress("Searching for device...")
        
        vendor_id = self.vendor_id_var.get()
        product_id = self.product_id_var.get()
        
        found, status = WindowsDeviceManager.get_device_status(vendor_id, product_id)
        
        # Update status display
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        
        if found:
            self.status_text.insert(tk.END, f"✓ {status}\n\nDevice detected successfully!")
            self.status_text.config(foreground="green")
            self.install_btn.config(state=tk.NORMAL)
        else:
            self.status_text.insert(tk.END, f"✗ {status}\n\nPlease connect the device and try again.")
            self.status_text.config(foreground="red")
            self.install_btn.config(state=tk.DISABLED)
        
        self.status_text.config(state=tk.DISABLED)
        self.log_progress(status)
    
    def install_driver(self):
        """Install driver"""
        self.progress_text.config(state=tk.NORMAL)
        self.progress_text.delete(1.0, tk.END)
        self.progress_text.config(state=tk.DISABLED)
        
        self.log_progress("Starting driver installation...\n")
        
        self.installer = DriverInstaller()
        
        # Download driver
        driver_dir = self.installer.download_driver(self.log_progress)
        if not driver_dir:
            self.log_progress("Failed to download driver")
            messagebox.showerror("Error", "Failed to download driver")
            return
        
        # Find driver files
        driver_path = self.installer.find_driver_files(driver_dir)
        if not driver_path:
            self.log_progress("Failed to find driver files")
            messagebox.showerror("Error", "Failed to find driver files")
            return
        
        self.log_progress(f"Driver files found at: {driver_path}")
        
        # Install driver
        success = self.installer.install_driver(driver_path, self.log_progress)
        
        if success:
            self.log_progress("\n✓ Driver installed successfully!")
            messagebox.showinfo("Success", "Driver installed successfully!")
        else:
            self.log_progress("\n✗ Driver installation failed")
            messagebox.showerror("Error", "Driver installation failed")
        
        # Cleanup
        self.installer.cleanup()
    
    def browse_driver(self):
        """Browse for driver directory"""
        driver_dir = filedialog.askdirectory(title="Select Driver Directory")
        if driver_dir:
            self.progress_text.config(state=tk.NORMAL)
            self.progress_text.delete(1.0, tk.END)
            self.progress_text.config(state=tk.DISABLED)
            
            self.log_progress(f"Using driver from: {driver_dir}\n")
            
            self.installer = DriverInstaller()
            driver_path = self.installer.find_driver_files(Path(driver_dir))
            
            if driver_path:
                self.log_progress(f"Driver files found at: {driver_path}")
                success = self.installer.install_driver(driver_path, self.log_progress)
                
                if success:
                    self.log_progress("\n✓ Driver installed successfully!")
                    messagebox.showinfo("Success", "Driver installed successfully!")
                else:
                    self.log_progress("\n✗ Driver installation failed")
                    messagebox.showerror("Error", "Driver installation failed")
            else:
                self.log_progress("No driver files found in selected directory")
                messagebox.showerror("Error", "No driver files found")


def main():
    """Main entry point"""
    if not HAS_TKINTER:
        print("Error: tkinter is required but not installed")
        print("Install with: pip install tk")
        sys.exit(1)
    
    if not HAS_WINREG:
        print("Warning: This application is designed for Windows")
    
    root = tk.Tk()
    app = DriverInstallerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
