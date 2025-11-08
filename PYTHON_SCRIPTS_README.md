# Python Scripts para V-USB Bootloader

Scripts Python para compilar e flashear bootloader V-USB customizado com suporte a múltiplos MCUs e nomes de device personalizados.

## 📁 Arquivos

- **`build_vusb_bootloader.py`** - Compila bootloader V-USB
- **`flash_bootloader.py`** - Flasheia bootloader via ISP
- **`setup_vusb.sh`** - Menu interativo (Linux/macOS)

## 🚀 Quick Start

### 1. Tornar scripts executáveis

```bash
chmod +x build_vusb_bootloader.py flash_bootloader.py setup_vusb.sh
```

### 2. Verificar dependências

```bash
python3 build_vusb_bootloader.py --check-deps
python3 flash_bootloader.py --check-deps
```

### 3. Compilar bootloader

```bash
python3 build_vusb_bootloader.py --mcu nano --name "Button Box"
```

### 4. Flashear bootloader

```bash
python3 flash_bootloader.py \
  --mcu atmega328p \
  --hex bootloader_builds/bootloader_nano_Button_Box.hex \
  --port /dev/ttyUSB0 \
  --full
```

## 📖 Documentação Detalhada

### build_vusb_bootloader.py

Compila bootloader V-USB com configurações customizadas.

#### Uso Básico

```bash
python3 build_vusb_bootloader.py --mcu NANO --name "Device Name"
```

#### Opções

```
--vusb-path PATH          Caminho para V-USB (padrão: v-usb)
--output-dir DIR          Diretório de saída (padrão: bootloader_builds)
--mcu MCU                 MCU alvo: nano, micro, leonardo, uno, attiny85
--name NAME               Nome do device USB (máx 32 chars)
--vendor-id ID            Vendor ID USB (padrão: 0x16c0)
--product-id ID           Product ID USB (padrão: 0x05df)
--list-mcus               Lista MCUs disponíveis
--check-deps              Verifica dependências
```

#### Exemplos

```bash
# Arduino Nano com nome customizado
python3 build_vusb_bootloader.py --mcu nano --name "Button Box"

# Arduino Micro com IDs customizados
python3 build_vusb_bootloader.py \
  --mcu micro \
  --name "Game Controller" \
  --vendor-id 0x1234 \
  --product-id 0x5678

# ATtiny85
python3 build_vusb_bootloader.py --mcu attiny85 --name "Tiny Device"

# Listar MCUs disponíveis
python3 build_vusb_bootloader.py --list-mcus
```

#### Saída

```
============================================================
Building V-USB Bootloader
============================================================
MCU: Arduino Nano (ATmega328P)
Device Name: Button Box
Vendor ID: 0x16c0
Product ID: 0x05df
============================================================

📋 Copying V-USB source files...
⚙️  Creating usbconfig.h...
📝 Creating Makefile...
📋 Copying firmware source...
🔨 Compiling bootloader...
...
✅ Bootloader compiled successfully!
📦 Output: bootloader_builds/build_nano_Button_Box/bootloader.hex
💾 Saved to: bootloader_builds/bootloader_nano_Button_Box.hex
```

### flash_bootloader.py

Flasheia bootloader compilado via programador ISP.

#### Uso Básico

```bash
python3 flash_bootloader.py \
  --mcu atmega328p \
  --hex bootloader.hex \
  --port /dev/ttyUSB0 \
  --full
```

#### Opções

```
--mcu MCU                 MCU alvo: atmega328p, atmega32u4, attiny85
--hex FILE                Arquivo .hex para flashear
--port PORT               Porta serial (COM3, /dev/ttyUSB0, etc)
--programmer TYPE         Tipo de programador (padrão: avrisp)
--baud RATE               Taxa de baud (padrão: 19200)
--full                    Sequência completa (backup, fuses, flash, verify)
--backup FILE             Fazer backup do bootloader atual
--set-fuses               Configurar fuses do MCU
--verify                  Verificar após flashear
--detect-ports            Detectar portas seriais disponíveis
--check-deps              Verificar se avrdude está instalado
```

#### Exemplos

```bash
# Sequência completa (recomendado)
python3 flash_bootloader.py \
  --mcu atmega328p \
  --hex bootloader_nano_Button_Box.hex \
  --port /dev/ttyUSB0 \
  --full

# Apenas flashear
python3 flash_bootloader.py \
  --mcu atmega328p \
  --hex bootloader.hex \
  --port /dev/ttyUSB0

# Fazer backup
python3 flash_bootloader.py \
  --mcu atmega328p \
  --port /dev/ttyUSB0 \
  --backup bootloader_backup.hex

# Detectar portas
python3 flash_bootloader.py --detect-ports

# Com baud rate customizado
python3 flash_bootloader.py \
  --mcu atmega328p \
  --hex bootloader.hex \
  --port COM3 \
  --baud 9600 \
  --full
```

#### Sequência Completa (--full)

1. **Backup** - Salva bootloader atual
2. **Fuses** - Configura fuses para V-USB
3. **Flash** - Flasheia novo bootloader
4. **Verify** - Verifica integridade

### setup_vusb.sh

Menu interativo para facilitar todo o processo (Linux/macOS).

#### Uso

```bash
./setup_vusb.sh
```

#### Menu

```
V-USB Bootloader Setup
1) Check dependencies
2) List available MCUs
3) Build bootloader
4) Flash bootloader
5) Full setup (build + flash)
6) Backup current bootloader
7) Restore bootloader
8) Exit
```

## 🔧 Configurações de MCU

### Arduino Nano (ATmega328P)
```
MCU: atmega328p
F_CPU: 16 MHz
USB Port: B
Fuses: Low=0xdf, High=0xda, Ext=0x05
```

### Arduino Micro (ATmega32U4)
```
MCU: atmega32u4
F_CPU: 16 MHz
USB Port: D
Fuses: Low=0xdf, High=0xd9, Ext=0xc3
```

### Arduino Leonardo (ATmega32U4)
```
MCU: atmega32u4
F_CPU: 16 MHz
USB Port: D
Fuses: Low=0xdf, High=0xd9, Ext=0xc3
```

### ATtiny85
```
MCU: attiny85
F_CPU: 16.5 MHz
USB Port: B
Fuses: Low=0xe1, High=0xdd, Ext=0xff
```

## 📊 Estrutura de Saída

```
bootloader_builds/
├── build_nano_Button_Box/
│   ├── bootloader.hex
│   ├── bootloader.elf
│   ├── usbconfig.h
│   ├── Makefile
│   ├── main.c
│   ├── oddebug.c
│   ├── oddebug.h
│   └── usbdrv/
│       ├── usbdrv.c
│       ├── usbdrv.h
│       ├── usbdrvasm.S
│       └── ...
├── bootloader_nano_Button_Box.hex
└── ...
```

## 🔌 Wiring ISP Programmer

```
Arduino UNO (Programmer)    →    Arduino Nano (Target)
Pin 13 (SCK)                →    Pin 7 (SCK)
Pin 11 (MOSI)               →    Pin 6 (MOSI)
Pin 12 (MISO)               →    Pin 8 (MISO)
Pin 10 (SS)                 →    Pin 1 (RESET)
GND                         →    GND
5V                          →    VCC
```

## ❌ Troubleshooting

### "avr-gcc not found"
```bash
sudo apt-get install gcc-avr avr-libc  # Linux
brew install avr-gcc                    # macOS
```

### "avrdude not found"
```bash
sudo apt-get install avrdude  # Linux
brew install avrdude           # macOS
```

### "Programmer is not responding"
- Verifique as conexões ISP
- Certifique-se de que o UNO tem ArduinoISP carregado
- Tente reduzir baud rate: `--baud 9600`

### "Device not recognized" após flash
- Verifique se os fuses foram configurados
- Tente restaurar bootloader original
- Verifique drivers USB (Windows)

### Restaurar Bootloader Original

```bash
python3 flash_bootloader.py \
  --mcu atmega328p \
  --hex bootloader_backup.hex \
  --port /dev/ttyUSB0 \
  --full
```

## 📝 Workflow Típico

### 1. Primeira Vez

```bash
# Verificar dependências
python3 build_vusb_bootloader.py --check-deps

# Compilar bootloader
python3 build_vusb_bootloader.py --mcu nano --name "Button Box"

# Preparar ISP (conectar UNO com ArduinoISP)

# Flashear com sequência completa
python3 flash_bootloader.py \
  --mcu atmega328p \
  --hex bootloader_builds/bootloader_nano_Button_Box.hex \
  --port /dev/ttyUSB0 \
  --full
```

### 2. Atualizar Device Name

```bash
# Compilar com novo nome
python3 build_vusb_bootloader.py --mcu nano --name "New Name"

# Flashear (sem fuses, já configurados)
python3 flash_bootloader.py \
  --mcu atmega328p \
  --hex bootloader_builds/bootloader_nano_New_Name.hex \
  --port /dev/ttyUSB0
```

### 3. Restaurar Original

```bash
# Se você fez backup
python3 flash_bootloader.py \
  --mcu atmega328p \
  --hex bootloader_backup.hex \
  --port /dev/ttyUSB0 \
  --full
```

## 🎓 Referências

- V-USB: https://www.obdev.at/products/vusb/
- AVRDude: https://www.nongnu.org/avrdude/
- ATmega328P: https://ww1.microchip.com/
- Arduino ISP: https://www.arduino.cc/en/Tutorial/BuiltInExamples/ArduinoISP

## 📄 Licença

Estes scripts são fornecidos como-está para facilitar o desenvolvimento com V-USB.

## 💡 Dicas

- ✅ Sempre faça backup antes de flashear
- ✅ Use `--full` na primeira vez
- ✅ Mantenha os arquivos .hex para referência
- ✅ Teste em Windows/Linux após flash
- ✅ Documente suas configurações customizadas
