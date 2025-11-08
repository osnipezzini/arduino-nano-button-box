#include <Keypad.h>
#include <Joystick.h>

// ============================================
// MATRIX CONFIGURATION (4x4 = 16 buttons)
// To expand to 5x5 (25 buttons):
// - Change ROWS to 5 and COLS to 5
// - Add additional pins to rowPins and colPins
// - Extend the keys array
// ============================================

const byte ROWS = 4; // four rows
const byte COLS = 4; // four columns

char keys[ROWS][COLS] = {
    {'A', 'B', 'C', 'D'},
    {'E', 'F', 'G', 'H'},
    {'I', 'J', 'K', 'L'},
    {'M', 'N', 'O', 'P'}};

byte rowPins[ROWS] = {5, 4, 3, 2};     // connect to the row pinouts of the keypad
byte colPins[COLS] = {9, 8, 7, 6};     // connect to the column pinouts of the keypad

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

// Joystick configuration: 32 buttons (supports expansion)
Joystick_ Joystick(
    JOYSTICK_DEFAULT_REPORT_ID,
    JOYSTICK_TYPE_GAMEPAD,
    32,                    // Button count (max 32 for standard HID)
    0,                     // Hat switch count
    false, false, false,   // X, Y, Z axes (disabled)
    false, false, false,   // Rx, Ry, Rz axes (disabled)
    false, false           // Rudder, Throttle (disabled)
);

// Button state tracking
bool buttonState[ROWS][COLS] = {false};
int buttonIndex = 0;

void setup()
{
  // Initialize Joystick
  Joystick.begin();
  
  // Optional: Serial for debugging (comment out if not needed)
  Serial.begin(9600);
  delay(1000);
  Serial.println("Button Box initialized - 4x4 Matrix");
  Serial.println("Ready for Windows/Linux gamepad input");
}

void loop()
{
  char key = keypad.getKey();
  
  if (key != NO_KEY)
  {
    // Find button index (0-15 for 4x4 matrix)
    buttonIndex = getButtonIndex(key);
    
    KeyState state = keypad.getState();
    
    if (state == PRESSED)
    {
      Joystick.pressButton(buttonIndex);
      Serial.print("Button ");
      Serial.print(buttonIndex + 1);
      Serial.println(" pressed");
    }
    else if (state == RELEASED)
    {
      Joystick.releaseButton(buttonIndex);
      Serial.print("Button ");
      Serial.print(buttonIndex + 1);
      Serial.println(" released");
    }
  }
}

// Convert key character to button index (0-15)
int getButtonIndex(char key)
{
  switch (key)
  {
    case 'A': return 0;
    case 'B': return 1;
    case 'C': return 2;
    case 'D': return 3;
    case 'E': return 4;
    case 'F': return 5;
    case 'G': return 6;
    case 'H': return 7;
    case 'I': return 8;
    case 'J': return 9;
    case 'K': return 10;
    case 'L': return 11;
    case 'M': return 12;
    case 'N': return 13;
    case 'O': return 14;
    case 'P': return 15;
    default: return 0;
  }
}
