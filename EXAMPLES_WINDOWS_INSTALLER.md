# 📚 Exemplos - V-USB Driver Installer para Windows

## 1️⃣ Exemplo: Instalação Básica

### Cenário
Você tem um Arduino Button Box com V-USB e quer instalar o driver automaticamente.

### Passo a Passo

```bash
# 1. Conectar o dispositivo USB
# (Dispositivo aparecerá como "Unknown device" no Device Manager)

# 2. Executar o instalador
python windows_driver_installer.py

# 3. Na GUI:
#    - Selecionar "Button Box" no dropdown
#    - Clicar "Detect Device"
#    - Clicar "Install Driver"
#    - Pronto! ✓
```

### Resultado
```
✓ Device found: Arduino Button Box
✓ Driver installed successfully!
✓ Device aparece em Device Manager como "Arduino Button Box"
```

---

## 2️⃣ Exemplo: Compilar Executável

### Cenário
Você quer distribuir um executável Windows para usuários finais.

### Passo a Passo

```bash
# 1. Instalar dependências
pip install -r requirements_windows_installer.txt

# 2. Compilar
python build_windows_installer.py

# 3. Resultado
# dist/V-USB Driver Installer.exe (≈50-100 MB)
```

### Distribuição

```bash
# Copiar para pasta de distribuição
cp dist/"V-USB Driver Installer.exe" /path/to/distribution/

# Usuários finais:
# 1. Baixar V-USB Driver Installer.exe
# 2. Clicar direito → Run as Administrator
# 3. Seguir instruções na GUI
```

---

## 3️⃣ Exemplo: Gerar Driver Customizado

### Cenário
Você tem um dispositivo customizado com VID/PID diferentes e quer criar um pacote de driver.

### Passo a Passo

```bash
# 1. Gerar driver para seu dispositivo
python generate_vusb_driver.py \
    --name "Meu Dispositivo Customizado" \
    --vendor-id 0x1234 \
    --product-id 0x5678

# 2. Resultado
# vusb_drivers/vusb_driver_Meu_Dispositivo_Customizado/
#   ├── vusb_driver.inf
#   ├── install_driver.bat
#   └── README.txt
```

### Usar o Driver Gerado

```bash
# Opção 1: Executar script batch
cd vusb_drivers/vusb_driver_Meu_Dispositivo_Customizado/
install_driver.bat

# Opção 2: Instalação manual
# Device Manager → Unknown device
# Clicar direito → Update driver
# Selecionar: vusb_drivers/vusb_driver_Meu_Dispositivo_Customizado/
```

---

## 4️⃣ Exemplo: Testar Detecção de Dispositivos

### Cenário
Você quer verificar se seu dispositivo é detectado corretamente.

### Passo a Passo

```bash
# 1. Executar teste
python test_device_detection.py

# 2. Saída esperada
# ========================================
# USB Device Detection Test
# ========================================
# 
# 1. Scanning all USB devices...
# Found 5 USB device(s):
# 
# 1. Arduino Button Box
#    Description: Arduino Button Box (V-USB)
#    Status: OK
#    Vendor ID: 0x16c0
#    Product ID: 0x05df
#    Device ID: USB\VID_16C0&PID_05DF\...
```

### Busca Interativa

```bash
# O script pergunta:
# Enter Vendor ID (hex, e.g., 0x16c0): 0x16c0
# Enter Product ID (hex, e.g., 0x05df): 0x05df

# Resultado:
# ✓ Device found!
#   Name: Arduino Button Box
#   Description: Arduino Button Box (V-USB)
#   Status: OK
#   Device ID: USB\VID_16C0&PID_05DF\...
```

---

## 5️⃣ Exemplo: Adicionar Novo Dispositivo

### Cenário
Você quer adicionar um novo dispositivo à lista de configuração.

### Método 1: Editar device_config.json

```json
{
  "devices": {
    "Button Box": {
      "vendor_id": "0x16c0",
      "product_id": "0x05df",
      "description": "Arduino Button Box (V-USB)"
    },
    "Novo Dispositivo": {
      "vendor_id": "0x1234",
      "product_id": "0x5678",
      "description": "Meu Dispositivo Customizado",
      "mcu": "atmega328p",
      "notes": "Dispositivo customizado com V-USB"
    }
  }
}
```

### Método 2: Usar config_loader.py

```bash
# 1. Executar
python config_loader.py

# 2. Menu interativo
# Options:
# 1. List devices
# 2. Add device
# 3. Remove device
# 4. Show full config
# 5. Exit
# 
# Select option (1-5): 2

# 3. Responder perguntas
# Device name: Novo Dispositivo
# Vendor ID (e.g., 0x16c0): 0x1234
# Product ID (e.g., 0x05df): 0x5678
# Description: Meu Dispositivo Customizado

# 4. Resultado
# ✓ Device added
```

### Método 3: Editar windows_driver_installer.py

```python
class DeviceConfig:
    DEFAULT_CONFIGS = {
        "Button Box": {
            "vendor_id": "0x16c0",
            "product_id": "0x05df",
            "description": "Arduino Button Box (V-USB)"
        },
        "Novo Dispositivo": {  # ← Adicionar aqui
            "vendor_id": "0x1234",
            "product_id": "0x5678",
            "description": "Meu Dispositivo Customizado"
        }
    }
```

---

## 6️⃣ Exemplo: Troubleshooting - Device Not Found

### Cenário
Você conectou o dispositivo mas ele não é detectado.

### Diagnóstico

```bash
# 1. Testar detecção
python test_device_detection.py

# 2. Verificar Device Manager
# Win+X → Device Manager
# Procurar por "Unknown device"
# Clicar direito → Properties
# Verificar "Device ID" para VID/PID
```

### Solução

```bash
# Se o dispositivo não aparece em Device Manager:
# 1. Tentar outra porta USB
# 2. Tentar outro cabo USB
# 3. Reiniciar o computador
# 4. Verificar se o dispositivo está alimentado

# Se aparece como "Unknown device":
# 1. Executar windows_driver_installer.py
# 2. Clicar "Detect Device"
# 3. Clicar "Install Driver"
```

---

## 7️⃣ Exemplo: Troubleshooting - Admin Privileges

### Cenário
Você recebe erro "Admin privileges required".

### Solução

```bash
# Opção 1: Clicar direito no executável
# 1. Clicar direito em V-USB Driver Installer.exe
# 2. Selecionar "Run as Administrator"
# 3. Clicar "Yes" na confirmação

# Opção 2: Criar atalho com privilégios
# 1. Clicar direito em V-USB Driver Installer.exe
# 2. Selecionar "Send to" → "Desktop (create shortcut)"
# 3. Clicar direito no atalho
# 4. Selecionar "Properties"
# 5. Clicar "Advanced"
# 6. Marcar "Run as Administrator"
# 7. Clicar OK
```

---

## 8️⃣ Exemplo: Troubleshooting - Driver Signature

### Cenário
Você recebe erro de assinatura de driver em Windows 10/11.

### Solução

```bash
# 1. Desabilitar assinatura de driver (temporário)
# Pressionar Shift + Restart
# Troubleshoot → Advanced options → Startup Settings
# Pressionar F7 (Disable driver signature enforcement)
# Computador reinicia

# 2. Instalar driver
# python windows_driver_installer.py
# Clicar "Install Driver"

# 3. Reabilitar assinatura (opcional)
# Reiniciar normalmente
```

---

## 9️⃣ Exemplo: Criar Pacote de Distribuição

### Cenário
Você quer distribuir um pacote completo com executável e driver.

### Passo a Passo

```bash
# 1. Compilar executável
python build_windows_installer.py
# Resultado: dist/V-USB Driver Installer.exe

# 2. Gerar driver customizado
python generate_vusb_driver.py --name "Button Box"
# Resultado: vusb_drivers/vusb_driver_Button_Box/

# 3. Copiar executável para pasta do driver
cp dist/"V-USB Driver Installer.exe" vusb_drivers/vusb_driver_Button_Box/

# 4. Criar arquivo ZIP
# Selecionar: vusb_drivers/vusb_driver_Button_Box/
# Clicar direito → Send to → Compressed (zipped) folder
# Resultado: vusb_driver_Button_Box.zip

# 5. Distribuir
# Enviar vusb_driver_Button_Box.zip para usuários
# Usuários extraem e executam V-USB Driver Installer.exe
```

### Estrutura do Pacote

```
vusb_driver_Button_Box.zip
└── vusb_driver_Button_Box/
    ├── V-USB Driver Installer.exe
    ├── vusb_driver.inf
    ├── install_driver.bat
    └── README.txt
```

---

## 🔟 Exemplo: Setup Automático (Windows)

### Cenário
Você quer fazer setup automático em uma máquina Windows.

### Passo a Passo

```bash
# 1. Clonar/baixar o projeto
git clone <repo-url>
cd arduino-nano-button-box

# 2. Executar setup
setup_windows_installer.bat

# 3. O script faz automaticamente:
#    - Verifica Python
#    - Instala dependências
#    - Compila executável
#    - Mostra instruções finais

# 4. Resultado
# ✓ Setup complete!
# Executable location: dist\V-USB Driver Installer.exe
```

---

## 🎯 Resumo de Exemplos

| Exemplo | Arquivo | Comando |
|---------|---------|---------|
| Instalação básica | windows_driver_installer.py | `python windows_driver_installer.py` |
| Compilar executável | build_windows_installer.py | `python build_windows_installer.py` |
| Gerar driver | generate_vusb_driver.py | `python generate_vusb_driver.py --name "..."` |
| Testar detecção | test_device_detection.py | `python test_device_detection.py` |
| Gerenciar config | config_loader.py | `python config_loader.py` |
| Setup automático | setup_windows_installer.bat | `setup_windows_installer.bat` |

---

## 💡 Dicas Práticas

### ✅ Boas Práticas

1. **Sempre testar detecção primeiro**
   ```bash
   python test_device_detection.py
   ```

2. **Executar como Administrador**
   - Clicar direito → Run as Administrator

3. **Usar porta USB diferente se não detectar**
   - Tentar todas as portas USB

4. **Reconectar dispositivo após instalação**
   - Desconectar e reconectar USB

5. **Verificar Device Manager**
   - Win+X → Device Manager
   - Procurar por "Arduino Button Box"

### ❌ Erros Comuns

1. **Não executar como Admin**
   - ❌ Erro: "Admin privileges required"
   - ✅ Solução: Clicar direito → Run as Administrator

2. **Dispositivo não conectado**
   - ❌ Erro: "Device not found"
   - ✅ Solução: Conectar dispositivo e tentar novamente

3. **VID/PID incorreto**
   - ❌ Erro: "Device not found"
   - ✅ Solução: Verificar com `test_device_detection.py`

4. **Driver assinado**
   - ❌ Erro: "Installation failed"
   - ✅ Solução: Desabilitar assinatura de driver

---

## 📞 Suporte

Para problemas não listados aqui:
1. Consultar `WINDOWS_DRIVER_INSTALLER_README.md`
2. Executar `test_device_detection.py`
3. Verificar `device_config.json`
4. Consultar documentação V-USB oficial

---

**Última atualização**: 2024-01-01  
**Versão**: 1.0.0
