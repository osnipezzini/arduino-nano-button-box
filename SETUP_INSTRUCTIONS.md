# Button Box - Setup Instructions (Windows & Linux)

## Prerequisites

### Required Hardware
- **Arduino Leonardo** (easiest) or **Arduino Nano with V-USB bootloader** (requires initial setup)
- 4x4 Matrix Keypad (or 5x5 for expansion)
- USB Cable (USB-B for Arduino)

### For Arduino Nano Users
If using Arduino Nano, you must first install the V-USB bootloader. See: **BOOTLOADER_VUSB_GUIDE.md**

### Required Libraries
1. **Keypad Library** by Mark Stanley & Alexander Brevig
2. **Joystick Library** by Matthew Heironimus

## Installation Steps

### 1. Install Arduino IDE
- Download from: https://www.arduino.cc/en/software

### 2. Install Required Libraries

**Via Arduino IDE:**
- Go to: `Sketch` → `Include Library` → `Manage Libraries`
- Search for "Keypad" and install by Mark Stanley & Alexander Brevig
- Search for "Joystick" and install by Matthew Heironimus

### 3. Board Setup

#### For Arduino Leonardo (Recommended)
- Connect via USB
- Go to: `Tools` → `Board` → Select `Arduino Leonardo`
- Select the correct COM port
- Upload the sketch

#### For Arduino Nano (Requires V-USB)
- This requires a custom bootloader (advanced)
- Alternative: Use Arduino Leonardo instead

### 4. Wiring

**Matrix Keypad to Arduino:**
```
Row Pins (Arduino):     5, 4, 3, 2
Column Pins (Arduino):  9, 8, 7, 6

Keypad Layout:
    Col0  Col1  Col2  Col3
    (9)   (8)   (7)   (6)
Row0(5)  A     B     C     D
Row1(4)  E     F     G     H
Row2(3)  I     J     K     L
Row3(2)  M     N     O     P
```

## Expansion to 5x5 Matrix (25 buttons)

To expand from 4x4 to 5x5:

1. **Update ROWS and COLS:**
```cpp
const byte ROWS = 5;
const byte COLS = 5;
```

2. **Extend keys array:**
```cpp
char keys[ROWS][COLS] = {
    {'A', 'B', 'C', 'D', 'E'},
    {'F', 'G', 'H', 'I', 'J'},
    {'K', 'L', 'M', 'N', 'O'},
    {'P', 'Q', 'R', 'S', 'T'},
    {'U', 'V', 'W', 'X', 'Y'}};
```

3. **Add new pins:**
```cpp
byte rowPins[ROWS] = {5, 4, 3, 2, 1};    // Add pin 1 for 5th row
byte colPins[COLS] = {9, 8, 7, 6, 10};   // Add pin 10 for 5th column
```

4. **Update getButtonIndex() function** to handle new keys Q-Y

## Testing

### Windows
1. Connect Arduino via USB
2. Go to: `Settings` → `Devices` → `Bluetooth & devices` → `Connected devices`
3. Your device should appear as "Arduino Leonardo" or similar
4. Test in any game that supports gamepad input

### Linux
1. Connect Arduino via USB
2. Run: `lsusb` to verify connection
3. Run: `jstest /dev/input/js0` to test button presses
4. Test in any game supporting gamepad input

## Troubleshooting

### Device not recognized
- Ensure correct board is selected in Arduino IDE
- Try different USB cable
- Reinstall CH340 drivers (if using Nano)

### Buttons not responding
- Check wiring against diagram
- Verify Keypad library is installed
- Check Serial monitor for debug messages

### Compilation errors
- Ensure Joystick library is installed
- Check Arduino IDE board selection
- Verify library versions are compatible

## Features

✅ 32 buttons supported (expandable)  
✅ Windows & Linux compatible  
✅ Standard HID gamepad protocol  
✅ Real-time button press/release detection  
✅ Serial debug output  
✅ Easy expansion to 5x5 or larger matrices  

## Notes

- The Joystick library supports up to 32 buttons in standard HID mode
- For more than 32 buttons, you'll need additional multiplexing hardware
- Serial debugging can be disabled by commenting out Serial lines for production use
