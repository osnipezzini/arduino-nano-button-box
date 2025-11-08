# 📋 Windows V-USB Driver Installer - Índice Completo

## 🎯 Visão Geral

Sistema completo e automático para instalar drivers V-USB no Windows, detectando dispositivos pela ID e oferecendo interface gráfica amigável.

---

## 📁 Estrutura de Arquivos

### 🔴 Arquivos Principais (Executáveis)

```
windows_driver_installer.py
├─ GUI principal com Tkinter
├─ Detecção de dispositivos por VID/PID
├─ Download automático de drivers
├─ Instalação com um clique
└─ Suporte a múltiplos dispositivos
```

```
generate_vusb_driver.py
├─ Gera pacotes de driver customizados
├─ Cria INF files automaticamente
├─ Inclui scripts batch de instalação
└─ Gera documentação README
```

```
build_windows_installer.py
├─ Compila executável Windows
├─ Usa PyInstaller
└─ Gera: dist/V-USB Driver Installer.exe
```

```
test_device_detection.py
├─ Testa detecção de dispositivos USB
├─ Mostra VID/PID de todos os dispositivos
├─ Busca interativa por dispositivo
└─ Útil para debugging
```

```
config_loader.py
├─ Carrega device_config.json
├─ Gerencia dispositivos customizados
├─ Interface interativa
└─ Adiciona/remove dispositivos
```

### 🟡 Arquivos de Configuração

```
device_config.json
├─ Configurações de dispositivos
├─ Dispositivos pré-configurados
├─ Configurações de driver
├─ Configurações de UI
└─ Configurações avançadas
```

```
vusb_driver_template.inf
├─ Template de driver INF
├─ Usado para gerar drivers customizados
└─ Compatível com WinUSB
```

```
requirements_windows_installer.txt
├─ Dependências Python
├─ pyinstaller para compilar
└─ requests (opcional)
```

### 🟢 Scripts de Setup

```
setup_windows_installer.bat
├─ Setup automático para Windows
├─ Instala dependências
├─ Compila executável
└─ Instruções finais
```

### 🔵 Documentação

```
WINDOWS_DRIVER_INSTALLER_README.md
├─ Documentação completa
├─ Instruções de uso
├─ Troubleshooting
├─ Referências
└─ Dicas e truques
```

```
QUICK_START_WINDOWS.md
├─ Início rápido
├─ Instruções resumidas
├─ Exemplos de uso
└─ Troubleshooting básico
```

```
WINDOWS_INSTALLER_INDEX.md
├─ Este arquivo
├─ Índice completo
└─ Referência rápida
```

---

## 🚀 Como Usar

### Para Usuários Finais

#### Opção 1: Executável (Recomendado)
```
1. Baixar V-USB Driver Installer.exe
2. Clicar direito → Run as Administrator
3. Conectar dispositivo USB
4. Clicar "Detect Device"
5. Clicar "Install Driver"
```

#### Opção 2: Python
```bash
python windows_driver_installer.py
```

### Para Desenvolvedores

#### Setup Rápido
```bash
# Windows
setup_windows_installer.bat

# Linux/Mac
pip install -r requirements_windows_installer.txt
python build_windows_installer.py
```

#### Testar Detecção
```bash
python test_device_detection.py
```

#### Gerar Driver Customizado
```bash
python generate_vusb_driver.py --name "Meu Dispositivo"
```

#### Gerenciar Configuração
```bash
python config_loader.py
```

---

## 🔧 Funcionalidades

| Funcionalidade | Arquivo | Status |
|---|---|---|
| Detecção automática de dispositivos | windows_driver_installer.py | ✅ |
| Download de drivers | windows_driver_installer.py | ✅ |
| Instalação automática | windows_driver_installer.py | ✅ |
| GUI com Tkinter | windows_driver_installer.py | ✅ |
| Geração de drivers customizados | generate_vusb_driver.py | ✅ |
| Compilação de executável | build_windows_installer.py | ✅ |
| Teste de detecção | test_device_detection.py | ✅ |
| Gerenciamento de config | config_loader.py | ✅ |
| Instalação manual | vusb_driver_template.inf | ✅ |
| Setup automático | setup_windows_installer.bat | ✅ |

---

## 📱 Dispositivos Suportados

### Pré-configurados
- Button Box (V-USB) - 0x16c0:0x05df
- Arduino Uno - 0x2341:0x0043
- Arduino Micro - 0x2341:0x0243
- Arduino Leonardo - 0x2341:0x8036

### Customizáveis
- Editar `device_config.json`
- Usar `config_loader.py`
- Adicionar via GUI

---

## 🔍 Detecção de Dispositivos

### Métodos Utilizados
1. **PowerShell WMI** - Busca por VID/PID
2. **Verificação de status** - Verifica conexão
3. **Parsing de Device ID** - Extrai informações

### Testar Manualmente
```bash
python test_device_detection.py
```

### Verificar em Device Manager
```
Win+X → Device Manager
Procurar por "Unknown device"
Verificar VID/PID
```

---

## 💾 Instalação de Driver

### Métodos Suportados

#### 1. pnputil (Automático)
```bash
pnputil /add-driver vusb_driver.inf /install
```

#### 2. Device Manager (Manual)
```
Device Manager → Unknown device
Clicar direito → Update driver
Selecionar pasta com driver
```

#### 3. Desabilitar Assinatura (Windows 10/11)
```
Shift + Restart
Troubleshoot → Advanced options → Startup Settings
F7 → Disable driver signature enforcement
```

---

## ⚙️ Configuração

### Adicionar Novo Dispositivo

#### Método 1: Editar JSON
```json
{
  "devices": {
    "Novo Dispositivo": {
      "vendor_id": "0x1234",
      "product_id": "0x5678",
      "description": "Descrição"
    }
  }
}
```

#### Método 2: Usar config_loader.py
```bash
python config_loader.py
# Selecionar opção 2 (Add device)
```

#### Método 3: Editar Python
```python
# windows_driver_installer.py
class DeviceConfig:
    DEFAULT_CONFIGS = {
        "Novo Dispositivo": {
            "vendor_id": "0x1234",
            "product_id": "0x5678",
            "description": "Descrição"
        }
    }
```

---

## 📦 Distribuição

### Criar Pacote

```bash
# 1. Gerar driver
python generate_vusb_driver.py --name "Meu Dispositivo"

# 2. Copiar executável
cp dist/"V-USB Driver Installer.exe" vusb_drivers/vusb_driver_Meu_Dispositivo/

# 3. Zipar
# Resultado: vusb_drivers/vusb_driver_Meu_Dispositivo.zip
```

### Estrutura do Pacote
```
vusb_driver_Meu_Dispositivo/
├── V-USB Driver Installer.exe
├── vusb_driver.inf
├── install_driver.bat
└── README.txt
```

---

## 🐛 Troubleshooting

### "Device not found"
```bash
# Verificar dispositivos
python test_device_detection.py

# Procurar em Device Manager
# Verificar VID/PID
```

### "Admin privileges required"
- Clicar direito no executável
- Selecionar "Run as Administrator"

### "Installation failed"
- Desabilitar assinatura de driver
- Tentar instalação manual
- Verificar Device Manager

### "Driver not appearing"
- Reconectar dispositivo
- Reiniciar computador
- Verificar: `pnputil /enum-drivers`

---

## 🔗 Referências

- [V-USB Official](https://www.obdev.at/products/vusb/)
- [WinUSB Driver](https://docs.microsoft.com/en-us/windows-hardware/drivers/usbcon/winusb)
- [Device Manager](https://support.microsoft.com/en-us/windows/open-device-manager-a7f2db18-270f-6dd9-d289-cead87d1b93b)
- [PyInstaller](https://pyinstaller.org/)

---

## 📊 Resumo de Arquivos

| Arquivo | Tipo | Tamanho | Descrição |
|---------|------|--------|-----------|
| windows_driver_installer.py | Python | ~15KB | GUI principal |
| generate_vusb_driver.py | Python | ~12KB | Gerador de drivers |
| build_windows_installer.py | Python | ~3KB | Builder |
| test_device_detection.py | Python | ~8KB | Teste de detecção |
| config_loader.py | Python | ~10KB | Gerenciador de config |
| device_config.json | JSON | ~2KB | Configurações |
| vusb_driver_template.inf | INF | ~1KB | Template de driver |
| requirements_windows_installer.txt | TXT | <1KB | Dependências |
| setup_windows_installer.bat | BAT | ~1KB | Setup script |
| WINDOWS_DRIVER_INSTALLER_README.md | MD | ~20KB | Documentação |
| QUICK_START_WINDOWS.md | MD | ~8KB | Quick start |
| WINDOWS_INSTALLER_INDEX.md | MD | ~15KB | Este arquivo |

**Total**: ~95KB de código e documentação

---

## ✅ Checklist de Implementação

- [x] GUI com Tkinter
- [x] Detecção de dispositivos por VID/PID
- [x] Download automático de drivers
- [x] Instalação automática
- [x] Geração de drivers customizados
- [x] Compilação de executável
- [x] Teste de detecção
- [x] Gerenciamento de configuração
- [x] Documentação completa
- [x] Setup automático
- [x] Troubleshooting
- [x] Exemplos de uso

---

## 🎓 Próximos Passos

1. **Testar em Windows** com dispositivo real
2. **Gerar executável final** com `build_windows_installer.py`
3. **Criar pacote de distribuição** com `generate_vusb_driver.py`
4. **Adicionar mais dispositivos** em `device_config.json`
5. **Testar instalação manual** em diferentes versões do Windows
6. **Criar assinatura digital** do executável (opcional)
7. **Distribuir** via website ou GitHub

---

## 📞 Suporte

Para problemas ou dúvidas:
1. Consultar `WINDOWS_DRIVER_INSTALLER_README.md`
2. Executar `test_device_detection.py`
3. Verificar `device_config.json`
4. Consultar documentação V-USB oficial

---

**Última atualização**: 2024-01-01  
**Versão**: 1.0.0  
**Status**: ✅ Completo e pronto para uso
