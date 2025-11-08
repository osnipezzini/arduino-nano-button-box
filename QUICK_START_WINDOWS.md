# 🚀 Quick Start - V-USB Driver Installer

## Para Usuários Finais

### Opção 1: Usar Executável (Mais Fácil)

1. **Baixar** `V-USB Driver Installer.exe`
2. **Clicar direito** → "Run as Administrator"
3. **Conectar** o dispositivo USB
4. **Clicar** em "Detect Device"
5. **Clicar** em "Install Driver"
6. **Pronto!** ✓

---

## Para Desenvolvedores

### Setup Rápido

```bash
# 1. Clonar/baixar o projeto
cd arduino-nano-button-box

# 2. Windows: Executar setup
setup_windows_installer.bat

# Linux/Mac: Instalar dependências
pip install -r requirements_windows_installer.txt
python build_windows_installer.py
```

### Testar Detecção de Dispositivos

```bash
# Windows
python test_device_detection.py

# Isso mostrará:
# - Todos os dispositivos USB conectados
# - Vendor ID e Product ID
# - Status do dispositivo
```

### Gerar Driver Customizado

```bash
# Driver padrão
python generate_vusb_driver.py

# Driver customizado
python generate_vusb_driver.py \
    --name "Meu Dispositivo" \
    --vendor-id 0x16c0 \
    --product-id 0x05df

# Resultado: vusb_drivers/vusb_driver_Meu_Dispositivo/
```

### Executar GUI Diretamente

```bash
python windows_driver_installer.py
```

---

## 📁 Arquivos Principais

| Arquivo | Descrição |
|---------|-----------|
| `windows_driver_installer.py` | App principal com GUI |
| `generate_vusb_driver.py` | Gera drivers customizados |
| `test_device_detection.py` | Testa detecção de dispositivos |
| `build_windows_installer.py` | Compila executável |
| `setup_windows_installer.bat` | Setup automático (Windows) |

---

## 🔧 Configurações

### Adicionar Novo Dispositivo

Edite `windows_driver_installer.py`:

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
            "description": "Descrição"
        }
    }
```

---

## ⚠️ Troubleshooting

### "Device not found"
```bash
# Verificar dispositivos conectados
python test_device_detection.py

# Procurar por "Unknown device" no Device Manager
# Verificar Vendor ID e Product ID
```

### "Admin privileges required"
- Clicar direito no executável
- Selecionar "Run as Administrator"

### "Installation failed"
- Desabilitar assinatura de driver (Windows 10/11):
  1. Pressionar Shift + Restart
  2. Troubleshoot → Advanced options → Startup Settings
  3. Pressionar F7
  4. Reiniciar

---

## 📦 Distribuição

### Criar Pacote para Distribuição

```bash
# 1. Gerar driver customizado
python generate_vusb_driver.py --name "Meu Dispositivo"

# 2. Copiar executável
cp dist/"V-USB Driver Installer.exe" vusb_drivers/vusb_driver_Meu_Dispositivo/

# 3. Zipar
# Resultado: vusb_drivers/vusb_driver_Meu_Dispositivo.zip
```

---

## 🔗 Referências

- [V-USB Official](https://www.obdev.at/products/vusb/)
- [Windows Device Manager](https://support.microsoft.com/en-us/windows/open-device-manager-a7f2db18-270f-6dd9-d289-cead87d1b93b)
- [WinUSB Driver](https://docs.microsoft.com/en-us/windows-hardware/drivers/usbcon/winusb)

---

## 💡 Dicas

✓ Testar detecção antes de instalar  
✓ Executar como Administrador  
✓ Usar porta USB diferente se não detectar  
✓ Reconectar dispositivo após instalação  

---

**Pronto para começar?** Veja `WINDOWS_DRIVER_INSTALLER_README.md` para documentação completa.
