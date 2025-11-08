# Arduino Nano V-USB Bootloader Installation Guide

## Overview
V-USB permite que Arduino Nano emule um dispositivo USB HID sem hardware adicional. Isso requer reprogramar o bootloader uma única vez.

## Prerequisites

### Hardware Required
- Arduino Nano (ATmega328P)
- Arduino UNO (or another Arduino) to act as ISP programmer
- 6 jumper wires
- USB cable for the programmer Arduino

### Software Required
- Arduino IDE (latest version)
- V-USB bootloader files (included in this guide)

## Step 1: Prepare the ISP Programmer

### 1.1 Upload ArduinoISP Sketch
1. Connect your **programmer Arduino (UNO)** via USB
2. Open Arduino IDE
3. Go to: `File` → `Examples` → `ArduinoISP` → `ArduinoISP`
4. Select correct board and COM port for the UNO
5. Upload the sketch

### 1.2 Wiring Diagram (UNO as ISP → Nano)

```
Arduino UNO (Programmer)    →    Arduino Nano (Target)
Pin 13 (SCK)                →    Pin 7 (SCK)
Pin 11 (MOSI)               →    Pin 6 (MOSI)
Pin 12 (MISO)               →    Pin 8 (MISO)
Pin 10 (SS)                 →    Pin 1 (RESET)
GND                         →    GND
5V                          →    VCC
```

**Important:** Do NOT connect USB to Nano during programming!

## Step 2: Install V-USB Bootloader

### 2.1 Download V-USB Bootloader
The V-USB bootloader for ATmega328P is available at:
- https://github.com/obdev/v-usb

Or use the pre-compiled version for Arduino Nano:
- Search for "micronucleus bootloader" (alternative V-USB implementation)

### 2.2 Add Bootloader to Arduino IDE

1. Locate Arduino IDE installation folder:
   - **Windows**: `C:\Users\[YourUsername]\AppData\Local\Arduino15\packages`
   - **Linux**: `~/.arduino15/packages`
   - **macOS**: `~/Library/Arduino15/packages`

2. Create folder structure:
   ```
   arduino15/packages/arduino/hardware/avr/1.8.x/bootloaders/atmega/
   ```

3. Copy V-USB bootloader files (`.hex` files) to this folder

### 2.3 Configure Board Definition

Edit: `arduino15/packages/arduino/hardware/avr/1.8.x/boards.txt`

Add this board definition:

```
##############################################################
nano_vusb.name=Arduino Nano (V-USB)
nano_vusb.vid.0=0x16c0
nano_vusb.pid.0=0x05df

nano_vusb.upload.tool=avrisp
nano_vusb.upload.protocol=avrisp
nano_vusb.upload.maximum_size=28672
nano_vusb.upload.maximum_data_size=2048
nano_vusb.upload.speed=19200
nano_vusb.upload.use_1200bps_touch=false
nano_vusb.upload.wait_for_upload_port=false

nano_vusb.bootloader.tool=avrisp
nano_vusb.bootloader.low_fuses=0xdf
nano_vusb.bootloader.high_fuses=0xda
nano_vusb.bootloader.extended_fuses=0x05
nano_vusb.bootloader.unlock_bits=0x3f
nano_vusb.bootloader.lock_bits=0x0f
nano_vusb.bootloader.file=atmega/micronucleus-t88-2.0.hex

nano_vusb.build.mcu=atmega328p
nano_vusb.build.f_cpu=16000000L
nano_vusb.build.board=AVR_NANO
nano_vusb.build.core=arduino
nano_vusb.build.variant=eightanaloginputs
nano_vusb.build.vid=0x16c0
nano_vusb.build.pid=0x05df
```

## Step 3: Burn the Bootloader

### 3.1 Setup Arduino IDE

1. **Disconnect** Nano from USB
2. Connect Nano to UNO programmer via jumper wires (see wiring diagram)
3. Open Arduino IDE
4. Go to: `Tools` → `Board` → Select `Arduino Nano (V-USB)`
5. Go to: `Tools` → `Programmer` → Select `AVR ISP`
6. Go to: `Tools` → `Port` → Select the **UNO's COM port** (not Nano!)

### 3.2 Burn Bootloader

1. Go to: `Tools` → `Burn Bootloader`
2. Wait for completion (should take ~30 seconds)
3. You should see: "Done burning bootloader"

### 3.3 Verify Success

If successful:
- LED on UNO may blink during process
- No error messages
- Bootloader is now installed

## Step 4: Test V-USB Connection

### 4.1 Install Drivers (Windows Only)

1. Download libusb drivers from: https://github.com/libusb/libusb/wiki/Windows
2. Install using Zadig tool (included in libusb package)
3. Select "Arduino Nano (V-USB)" device
4. Install WinUSB driver

### 4.2 Connect Nano to Computer

1. Disconnect from UNO programmer
2. Connect Nano directly to computer via USB
3. **Windows**: Device should appear in Device Manager
4. **Linux**: Run `lsusb` - should show V-USB device (16c0:05df)

## Step 5: Upload Joystick Code

### 5.1 Setup Arduino IDE for V-USB Nano

1. Go to: `Tools` → `Board` → Select `Arduino Nano (V-USB)`
2. Go to: `Tools` → `Port` → Select Nano's COM port
3. Go to: `Tools` → `Programmer` → Select `AVR ISP` (or USB if available)

### 5.2 Upload Code

1. Open `ButtonBox.ino`
2. Click `Upload` (or `Sketch` → `Upload Using Programmer`)
3. Code should upload successfully

## Troubleshooting

### "Bootloader not found" error
- Verify bootloader files are in correct folder
- Check boards.txt syntax
- Restart Arduino IDE

### "avrdude: stk500_recv(): programmer is not responding"
- Check wiring between UNO and Nano
- Verify UNO has ArduinoISP uploaded
- Ensure Nano is NOT connected to USB during programming

### Device not recognized on Windows
- Install libusb drivers with Zadig
- Check Device Manager for unknown devices
- Try different USB port

### Device not recognized on Linux
- Run: `lsusb` to verify connection
- Check permissions: `sudo usermod -a -G dialout $USER`
- Restart computer after permission change

### Code upload fails after bootloader
- Ensure correct board selected (Arduino Nano V-USB)
- Try uploading with `Sketch` → `Upload Using Programmer`
- Check USB cable connection

## Important Notes

⚠️ **Backup Original Bootloader** (Optional)
Before burning, you can backup the original bootloader:
```bash
avrdude -c avrisp -p m328p -P COM3 -b 19200 -U flash:r:nano_backup.hex:i
```

⚠️ **Restore Original Bootloader** (If needed)
To revert to standard Arduino Nano bootloader:
```bash
avrdude -c avrisp -p m328p -P COM3 -b 19200 -U flash:w:nano_original.hex:i
```

## References

- V-USB Project: https://www.obdev.at/products/vusb/index.html
- Micronucleus (Alternative): https://github.com/micronucleus/micronucleus
- Arduino ISP: https://www.arduino.cc/en/Tutorial/BuiltInExamples/ArduinoISP

## Next Steps

After successful bootloader installation:
1. Upload the `ButtonBox.ino` code
2. Connect Nano to computer via USB
3. Test in Windows/Linux gamepad settings
4. Expand to 5x5 matrix as needed
