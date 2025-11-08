# 🎯 Customizar Drivers V-USB para SODevs

Guia prático para customizar drivers com múltiplos Button Box, cada um com seu próprio VID/PID.

## 📋 Visão Geral

Você pode ter múltiplos Button Box conectados simultaneamente, cada um com:
- **Nome único** (ex: "Omega Buttons V1", "Omega Buttons V2")
- **Manufacturer** (ex: "SODevs")
- **VID/PID diferentes** (para identificar cada um)

---

## 🚀 Uso Rápido

### Opção 1: Gerar um Driver Customizado

```bash
# Gerar driver com seu nome e manufacturer
python generate_vusb_driver.py \
    --name "Omega Buttons" \
    --manufacturer "SODevs" \
    --vendor-id 0x16c0 \
    --product-id 0x05df
```

**Resultado:**
```
vusb_drivers/vusb_driver_Omega_Buttons/
├── vusb_driver.inf          (Manufacturer: SODevs, Device: Omega Buttons)
├── install_driver.bat
└── README.txt
```

### Opção 2: Gerar Múltiplos Drivers (Recomendado)

```bash
# Usar script pronto para gerar todos os drivers SODevs
python generate_sodevs_drivers.py
```

**Resultado:**
```
vusb_drivers/
├── vusb_driver_Omega_Buttons/      (VID:0x16c0, PID:0x05df)
├── vusb_driver_Omega_Buttons_V2/   (VID:0x16c0, PID:0x05e0)
└── vusb_driver_Omega_Buttons_V3/   (VID:0x16c0, PID:0x05e1)
```

---

## 🔧 Customizar Drivers

### Editar generate_sodevs_drivers.py

Abra o arquivo e customize a lista de dispositivos:

```python
devices = [
    {
        "name": "Omega Buttons",
        "manufacturer": "SODevs",
        "vendor_id": "0x16c0",
        "product_id": "0x05df",
        "description": "Button Box Principal"
    },
    {
        "name": "Omega Buttons V2",
        "manufacturer": "SODevs",
        "vendor_id": "0x16c0",
        "product_id": "0x05e0",
        "description": "Button Box Versão 2"
    }
]
```

### Adicionar Novo Device

```python
{
    "name": "Omega Buttons V4",
    "manufacturer": "SODevs",
    "vendor_id": "0x16c0",
    "product_id": "0x05e2",
    "description": "Button Box Versão 4"
}
```

---

## 📝 Exemplos Práticos

### Exemplo 1: Driver Simples com Manufacturer

```bash
python generate_vusb_driver.py \
    --name "Omega Buttons" \
    --manufacturer "SODevs"
```

**INF file gerado:**
```ini
[Strings]
MANUFACTURER="SODevs"
DEVICE_NAME="Omega Buttons"
VENDOR_ID=16c0
PRODUCT_ID=05df
```

### Exemplo 2: Múltiplos Devices com VID/PID Diferentes

```bash
# Device 1
python generate_vusb_driver.py \
    --name "Omega Buttons V1" \
    --manufacturer "SODevs" \
    --vendor-id 0x16c0 \
    --product-id 0x05df

# Device 2
python generate_vusb_driver.py \
    --name "Omega Buttons V2" \
    --manufacturer "SODevs" \
    --vendor-id 0x16c0 \
    --product-id 0x05e0

# Device 3
python generate_vusb_driver.py \
    --name "Omega Buttons V3" \
    --manufacturer "SODevs" \
    --vendor-id 0x16c0 \
    --product-id 0x05e1
```

### Exemplo 3: Usar Script Automático

```bash
python generate_sodevs_drivers.py
```

Resultado:
```
Gerando 3 drivers...

📦 Button Box Principal
   Nome: Omega Buttons
   Fabricante: SODevs
   VID: 0x16c0 | PID: 0x05df
   ✅ Sucesso!

📦 Button Box Versão 2
   Nome: Omega Buttons V2
   Fabricante: SODevs
   VID: 0x16c0 | PID: 0x05e0
   ✅ Sucesso!

📦 Button Box Versão 3
   Nome: Omega Buttons V3
   Fabricante: SODevs
   VID: 0x16c0 | PID: 0x05e1
   ✅ Sucesso!

✅ Todos os drivers foram gerados com sucesso!
```

---

## 🎯 Atribuir VID/PID Únicos

### Tabela de VID/PID Disponíveis

Para V-USB (Vendor ID 0x16c0), você pode usar:

| Device | Vendor ID | Product ID | Descrição |
|--------|-----------|-----------|-----------|
| Omega Buttons V1 | 0x16c0 | 0x05df | Principal |
| Omega Buttons V2 | 0x16c0 | 0x05e0 | Versão 2 |
| Omega Buttons V3 | 0x16c0 | 0x05e1 | Versão 3 |
| Omega Buttons V4 | 0x16c0 | 0x05e2 | Versão 4 |
| Omega Buttons V5 | 0x16c0 | 0x05e3 | Versão 5 |

### Usar Vendor ID Próprio

Se você tiver seu próprio Vendor ID (ex: 0x1234):

```bash
python generate_vusb_driver.py \
    --name "Omega Buttons" \
    --manufacturer "SODevs" \
    --vendor-id 0x1234 \
    --product-id 0x0001
```

---

## 📦 Estrutura de Drivers Gerados

Cada driver gerado tem esta estrutura:

```
vusb_driver_Omega_Buttons/
├── vusb_driver.inf
│   └─ Contém: MANUFACTURER="SODevs"
│   └─ Contém: DEVICE_NAME="Omega Buttons"
│   └─ Contém: VENDOR_ID=16c0
│   └─ Contém: PRODUCT_ID=05df
│
├── install_driver.bat
│   └─ Script para instalar driver no Windows
│
└── README.txt
    └─ Instruções de instalação
```

---

## 🔍 Verificar Drivers Gerados

### Listar Todos os Drivers

```bash
python generate_vusb_driver.py --list
```

Resultado:
```
Configured devices:
  • Omega Buttons
  • Omega Buttons V2
  • Omega Buttons V3
```

### Verificar Conteúdo do INF

```bash
# Windows
type vusb_drivers\vusb_driver_Omega_Buttons\vusb_driver.inf

# Linux/Mac
cat vusb_drivers/vusb_driver_Omega_Buttons/vusb_driver.inf
```

Você verá:
```ini
[Strings]
MANUFACTURER="SODevs"
DEVICE_NAME="Omega Buttons"
VENDOR_ID=16c0
PRODUCT_ID=05df
```

---

## 💾 Distribuir Drivers

### Passo 1: Gerar Todos os Drivers

```bash
python generate_sodevs_drivers.py
```

### Passo 2: Compilar Executável

```bash
python build_windows_installer.py
```

Resultado: `dist/V-USB Driver Installer.exe`

### Passo 3: Copiar Executável para Cada Driver

```bash
# Windows
copy dist\"V-USB Driver Installer.exe" vusb_drivers\vusb_driver_Omega_Buttons\
copy dist\"V-USB Driver Installer.exe" vusb_drivers\vusb_driver_Omega_Buttons_V2\
copy dist\"V-USB Driver Installer.exe" vusb_drivers\vusb_driver_Omega_Buttons_V3\

# Linux/Mac
cp dist/"V-USB Driver Installer.exe" vusb_drivers/vusb_driver_Omega_Buttons/
cp dist/"V-USB Driver Installer.exe" vusb_drivers/vusb_driver_Omega_Buttons_V2/
cp dist/"V-USB Driver Installer.exe" vusb_drivers/vusb_driver_Omega_Buttons_V3/
```

### Passo 4: Zipar para Distribuição

```bash
# Windows
# Clicar direito em vusb_driver_Omega_Buttons → Send to → Compressed (zipped) folder

# Linux/Mac
zip -r vusb_driver_Omega_Buttons.zip vusb_drivers/vusb_driver_Omega_Buttons/
zip -r vusb_driver_Omega_Buttons_V2.zip vusb_drivers/vusb_driver_Omega_Buttons_V2/
zip -r vusb_driver_Omega_Buttons_V3.zip vusb_drivers/vusb_driver_Omega_Buttons_V3/
```

---

## 🖥️ Instalar Drivers no Windows

### Para Cada Device

1. **Extrair ZIP**
   ```
   vusb_driver_Omega_Buttons/
   ├── V-USB Driver Installer.exe
   ├── vusb_driver.inf
   ├── install_driver.bat
   └── README.txt
   ```

2. **Executar Instalador**
   ```
   Clicar direito em V-USB Driver Installer.exe
   → Run as Administrator
   ```

3. **Conectar Device**
   - Conectar o Button Box via USB

4. **Detectar e Instalar**
   - Clicar "Detect Device"
   - Clicar "Install Driver"

5. **Verificar em Device Manager**
   ```
   Win+X → Device Manager
   Procurar por "Omega Buttons" (ou "Omega Buttons V2", etc)
   ```

---

## 🔧 Troubleshooting

### "Device not found"

Verificar se o VID/PID está correto:

```bash
python test_device_detection.py
```

Procurar pelo VID/PID do seu device na lista.

### "Múltiplos devices com mesmo VID/PID"

Se você conectar 2 Button Box com o mesmo VID/PID, Windows não conseguirá diferenciá-los.

**Solução:** Use VID/PID diferentes para cada device:

```bash
# Device 1
python generate_vusb_driver.py \
    --name "Omega Buttons 1" \
    --manufacturer "SODevs" \
    --vendor-id 0x16c0 \
    --product-id 0x05df

# Device 2
python generate_vusb_driver.py \
    --name "Omega Buttons 2" \
    --manufacturer "SODevs" \
    --vendor-id 0x16c0 \
    --product-id 0x05e0
```

### "Driver não aparece em Device Manager"

1. Reconectar o device
2. Reiniciar o computador
3. Verificar: `pnputil /enum-drivers`

---

## 📊 Exemplo Completo: 3 Button Box

### Passo 1: Gerar Drivers

```bash
python generate_sodevs_drivers.py
```

### Passo 2: Estrutura Criada

```
vusb_drivers/
├── vusb_driver_Omega_Buttons/
│   ├── vusb_driver.inf (SODevs, Omega Buttons, 0x16c0:0x05df)
│   ├── install_driver.bat
│   └── README.txt
│
├── vusb_driver_Omega_Buttons_V2/
│   ├── vusb_driver.inf (SODevs, Omega Buttons V2, 0x16c0:0x05e0)
│   ├── install_driver.bat
│   └── README.txt
│
└── vusb_driver_Omega_Buttons_V3/
    ├── vusb_driver.inf (SODevs, Omega Buttons V3, 0x16c0:0x05e1)
    ├── install_driver.bat
    └── README.txt
```

### Passo 3: Device Manager após Instalação

```
Device Manager
├── Omega Buttons (COM3)
├── Omega Buttons V2 (COM4)
└── Omega Buttons V3 (COM5)
```

Cada um com seu próprio VID/PID e porta COM!

---

## 💡 Dicas

✅ **Use nomes descritivos**
- "Omega Buttons" (principal)
- "Omega Buttons V2" (versão 2)
- "Omega Buttons Teste" (para testes)

✅ **Sempre use manufacturer "SODevs"**
- Facilita identificar seus devices

✅ **Atribua VID/PID sequenciais**
- 0x05df, 0x05e0, 0x05e1, etc.

✅ **Documente seus VID/PID**
- Crie uma tabela com mapeamento

✅ **Teste antes de distribuir**
- Instale em uma máquina Windows
- Verifique em Device Manager

---

## 📞 Referência Rápida

| Comando | Descrição |
|---------|-----------|
| `python generate_vusb_driver.py --name "X" --manufacturer "Y"` | Gerar driver simples |
| `python generate_vusb_driver.py --name "X" --manufacturer "Y" --vendor-id 0x1234 --product-id 0x5678` | Gerar com VID/PID customizado |
| `python generate_sodevs_drivers.py` | Gerar todos os drivers SODevs |
| `python generate_vusb_driver.py --list` | Listar drivers gerados |
| `python test_device_detection.py` | Testar detecção de devices |
| `python build_windows_installer.py` | Compilar executável |

---

**Pronto!** Agora você pode gerar múltiplos drivers customizados para seus Button Box com nomes e VID/PID diferentes. 🚀
