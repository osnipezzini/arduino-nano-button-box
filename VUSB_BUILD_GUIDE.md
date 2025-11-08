# V-USB Bootloader Build & Flash Guide

Guia completo para compilar e flashear bootloader V-USB customizado usando Python scripts.

## 📋 Pré-requisitos

### Software Necessário

```bash
# Ubuntu/Debian
sudo apt-get install gcc-avr avr-libc avrdude make python3

# macOS
brew install avr-gcc avrdude
python3 --version  # Deve estar instalado

# Windows
# Instale Arduino IDE ou WinAVR
```

### Hardware Necessário

- Arduino Nano (ou Micro/Leonardo)
- Outro Arduino (UNO) como programador ISP
- 6 jumper wires
- USB cables

## 🚀 Quick Start

### 1. Verificar Dependências

```bash
python3 build_vusb_bootloader.py --check-deps
python3 flash_bootloader.py --check-deps
```

### 2. Listar MCUs Disponíveis

```bash
python3 build_vusb_bootloader.py --list-mcus
```

Saída esperada:
```
Available MCU Configurations:
------------------------------------------------------------
  nano             - Arduino Nano (ATmega328P)
  micro            - Arduino Micro (ATmega32U4)
  leonardo         - Arduino Leonardo (ATmega32U4)
  uno              - Arduino UNO (ATmega328P)
  attiny85         - ATtiny85
------------------------------------------------------------
```

### 3. Compilar Bootloader

```bash
# Para Arduino Nano com nome customizado
python3 build_vusb_bootloader.py --mcu nano --name "Button Box"

# Para Arduino Micro
python3 build_vusb_bootloader.py --mcu micro --name "Game Controller"

# Para Arduino Leonardo
python3 build_vusb_bootloader.py --mcu leonardo --name "My Device"
```

**Saída esperada:**
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

### 4. Preparar Programador ISP

Conecte Arduino UNO como programador ISP:

```
Arduino UNO (Programmer)    →    Arduino Nano (Target)
Pin 13 (SCK)                →    Pin 7 (SCK)
Pin 11 (MOSI)               →    Pin 6 (MOSI)
Pin 12 (MISO)               →    Pin 8 (MISO)
Pin 10 (SS)                 →    Pin 1 (RESET)
GND                         →    GND
5V                          →    VCC
```

**Importante:** NÃO conecte USB ao Nano durante a programação!

### 5. Detectar Porta Serial

```bash
python3 flash_bootloader.py --detect-ports
```

Ou use:
```bash
# Linux
ls /dev/ttyUSB*
ls /dev/ttyACM*

# macOS
ls /dev/tty.usbserial*

# Windows
# Verifique em Device Manager
```

### 6. Flashear Bootloader

#### Opção A: Sequência Completa (Recomendado)

```bash
python3 flash_bootloader.py \
  --mcu atmega328p \
  --hex bootloader_builds/bootloader_nano_Button_Box.hex \
  --port /dev/ttyUSB0 \
  --full
```

Isso fará:
1. ✅ Backup do bootloader atual
2. ✅ Configurar fuses do MCU
3. ✅ Flashear novo bootloader
4. ✅ Verificar integridade

#### Opção B: Apenas Flashear

```bash
python3 flash_bootloader.py \
  --mcu atmega328p \
  --hex bootloader_builds/bootloader_nano_Button_Box.hex \
  --port /dev/ttyUSB0
```

#### Opção C: Apenas Backup

```bash
python3 flash_bootloader.py \
  --mcu atmega328p \
  --port /dev/ttyUSB0 \
  --backup bootloader_backup.hex
```

## 🎯 Exemplos Completos

### Exemplo 1: Arduino Nano com Nome "Button Box"

```bash
# 1. Compilar
python3 build_vusb_bootloader.py --mcu nano --name "Button Box"

# 2. Flashear (com sequência completa)
python3 flash_bootloader.py \
  --mcu atmega328p \
  --hex bootloader_builds/bootloader_nano_Button_Box.hex \
  --port /dev/ttyUSB0 \
  --full
```

### Exemplo 2: Arduino Micro com Nome "Game Pad"

```bash
# 1. Compilar
python3 build_vusb_bootloader.py --mcu micro --name "Game Pad"

# 2. Flashear
python3 flash_bootloader.py \
  --mcu atmega32u4 \
  --hex bootloader_builds/bootloader_micro_Game_Pad.hex \
  --port /dev/ttyUSB0 \
  --full
```

### Exemplo 3: Customizar Vendor/Product ID

```bash
# Compilar com IDs customizados
python3 build_vusb_bootloader.py \
  --mcu nano \
  --name "My Device" \
  --vendor-id 0x1234 \
  --product-id 0x5678
```

## 🔧 Troubleshooting

### "avrdude not found"
```bash
# Instale avrdude
sudo apt-get install avrdude  # Linux
brew install avrdude           # macOS
```

### "Programmer is not responding"
- Verifique as conexões de jumper wire
- Certifique-se de que o UNO tem ArduinoISP carregado
- Tente uma porta diferente
- Reduza a velocidade de baud: `--baud 9600`

### "Device not recognized" (após flash)
- Verifique se os fuses foram configurados corretamente
- Tente restaurar bootloader original
- Verifique drivers USB (Windows)

### Restaurar Bootloader Original

```bash
# Se você fez backup
python3 flash_bootloader.py \
  --mcu atmega328p \
  --hex bootloader_backup.hex \
  --port /dev/ttyUSB0 \
  --full
```

## 📊 Configurações de MCU

### Arduino Nano (ATmega328P)
- MCU: atmega328p
- F_CPU: 16 MHz
- USB Port: B
- Fuses: Low=0xdf, High=0xda, Ext=0x05

### Arduino Micro (ATmega32U4)
- MCU: atmega32u4
- F_CPU: 16 MHz
- USB Port: D
- Fuses: Low=0xdf, High=0xd9, Ext=0xc3

### Arduino Leonardo (ATmega32U4)
- MCU: atmega32u4
- F_CPU: 16 MHz
- USB Port: D
- Fuses: Low=0xdf, High=0xd9, Ext=0xc3

### ATtiny85
- MCU: attiny85
- F_CPU: 16.5 MHz
- USB Port: B
- Fuses: Low=0xe1, High=0xdd, Ext=0xff

## 🔌 Próximos Passos

Após flashear o bootloader com sucesso:

1. **Desconecte o programador ISP**
2. **Conecte o Arduino via USB** ao computador
3. **Configure Arduino IDE:**
   - Selecione: `Tools` → `Board` → `Arduino Nano (V-USB)`
   - Selecione a porta correta
4. **Upload do código ButtonBox.ino**
5. **Teste em Windows/Linux**

## 📝 Notas Importantes

⚠️ **Backup Importante**
- Sempre faça backup do bootloader original antes de flashear
- Os scripts fazem isso automaticamente com `--full`

⚠️ **Fuses Críticos**
- Fuses incorretos podem "brickear" o Arduino
- Use os valores padrão fornecidos pelos scripts

⚠️ **Nomes de Device**
- Máximo 32 caracteres
- Evite caracteres especiais
- Será exibido no Windows/Linux

## 🎓 Referências

- V-USB Project: https://www.obdev.at/products/vusb/
- AVRDude Manual: https://www.nongnu.org/avrdude/
- ATmega328P Datasheet: https://ww1.microchip.com/

## ✅ Checklist

- [ ] Dependências instaladas (avr-gcc, avrdude, make)
- [ ] V-USB clonado em `v-usb/`
- [ ] Scripts Python têm permissão de execução
- [ ] Arduino UNO com ArduinoISP carregado
- [ ] Conexões ISP verificadas
- [ ] Bootloader compilado com sucesso
- [ ] Bootloader flasheado com sucesso
- [ ] Arduino reconhecido no Windows/Linux
- [ ] Código ButtonBox.ino carregado
- [ ] Botões testados e funcionando
