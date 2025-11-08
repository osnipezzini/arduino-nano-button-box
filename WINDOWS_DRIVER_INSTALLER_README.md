# V-USB Driver Installer para Windows

App automático para instalar drivers V-USB no Windows, detectando o dispositivo pela ID.

## 📋 Características

- ✅ Detecção automática de dispositivos USB pela Vendor ID e Product ID
- ✅ Download automático do driver V-USB
- ✅ Instalação com um clique
- ✅ Interface gráfica amigável
- ✅ Suporte a múltiplos dispositivos
- ✅ Geração de drivers customizados com INF files
- ✅ Instalação manual como fallback

## 🚀 Uso Rápido

### Opção 1: Executável Windows (Recomendado)

1. **Baixar**: `V-USB Driver Installer.exe`
2. **Executar como Administrador**
3. **Conectar o dispositivo USB**
4. **Clicar em "Detect Device"**
5. **Clicar em "Install Driver"**

### Opção 2: Executar com Python

```bash
# Instalar dependências
pip install tk

# Executar
python3 windows_driver_installer.py
```

## 🔧 Gerar Drivers Customizados

### Criar driver para seu dispositivo

```bash
# Driver padrão (Button Box)
python3 generate_vusb_driver.py

# Driver customizado
python3 generate_vusb_driver.py \
    --name "Meu Dispositivo" \
    --vendor-id 0x16c0 \
    --product-id 0x05df

# Listar drivers gerados
python3 generate_vusb_driver.py --list
```

### Estrutura do pacote gerado

```
vusb_drivers/
└── vusb_driver_Button_Box/
    ├── vusb_driver.inf          # Driver INF file
    ├── install_driver.bat       # Script de instalação
    └── README.txt               # Instruções
```

## 🏗️ Compilar Executável Windows

### Pré-requisitos

```bash
pip install pyinstaller
```

### Compilar

```bash
python3 build_windows_installer.py
```

Resultado: `dist/V-USB Driver Installer.exe`

## 📱 Configurações de Dispositivos

### Button Box (Padrão)
- **Vendor ID**: 0x16c0
- **Product ID**: 0x05df
- **Descrição**: Arduino Button Box (V-USB)

### Adicionar novo dispositivo

Edite `windows_driver_installer.py` e adicione em `DeviceConfig.DEFAULT_CONFIGS`:

```python
"Meu Dispositivo": {
    "vendor_id": "0x1234",
    "product_id": "0x5678",
    "description": "Descrição do dispositivo"
}
```

## 🔍 Detecção de Dispositivos

O app detecta dispositivos usando:

1. **PowerShell WMI** - Busca por VID/PID
2. **Verificação de status** - Verifica se o dispositivo está conectado
3. **Informações do dispositivo** - Nome, descrição e status

### Verificar manualmente

```powershell
# PowerShell como Admin
Get-WmiObject Win32_PnPEntity | Where-Object {
    $_.DeviceID -match "VID_16C0" -and $_.DeviceID -match "PID_05DF"
}
```

## ⚙️ Instalação de Driver

### Método 1: pnputil (Windows 7+)

```bash
pnputil /add-driver vusb_driver.inf /install
```

### Método 2: Device Manager

1. Conectar dispositivo
2. Abrir Device Manager (Win+X → Device Manager)
3. Procurar por dispositivo desconhecido
4. Clicar direito → Update driver
5. Selecionar pasta com driver

### Método 3: Desabilitar assinatura de driver (Windows 10/11)

Se receber erro de assinatura:

1. Pressionar Shift + Restart
2. Troubleshoot → Advanced options → Startup Settings
3. Pressionar F7 (Disable driver signature enforcement)
4. Reiniciar e tentar novamente

## 🐛 Troubleshooting

### "Device not found"
- Verificar conexão USB
- Tentar outra porta USB
- Verificar Device Manager para dispositivos desconhecidos
- Verificar Vendor ID e Product ID

### "Installation failed"
- Executar como Administrador
- Desabilitar assinatura de driver (Windows 10/11)
- Tentar instalação manual

### "Admin privileges required"
- Clicar direito no executável
- Selecionar "Run as Administrator"

### Driver não aparece em Device Manager
- Reconectar o dispositivo
- Reiniciar o computador
- Verificar se o driver foi realmente instalado com `pnputil /enum-drivers`

## 📦 Distribuição

### Criar pacote para distribuição

```bash
# Gerar driver customizado
python3 generate_vusb_driver.py --name "Meu Dispositivo"

# Copiar executável
cp dist/"V-USB Driver Installer.exe" vusb_drivers/vusb_driver_Meu_Dispositivo/

# Zipar para distribuição
# Resultado: vusb_drivers/vusb_driver_Meu_Dispositivo.zip
```

## 🔐 Segurança

- ✅ Requer privilégios de Administrador
- ✅ Verifica assinatura de driver
- ✅ Usa WinUSB (driver assinado Microsoft)
- ✅ Sem modificações de registro perigosas

## 📝 Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `windows_driver_installer.py` | App principal com GUI |
| `build_windows_installer.py` | Script para compilar executável |
| `generate_vusb_driver.py` | Gerador de drivers customizados |
| `vusb_driver_template.inf` | Template de INF file |
| `WINDOWS_DRIVER_INSTALLER_README.md` | Este arquivo |

## 🔗 Referências

- [V-USB Official](https://www.obdev.at/products/vusb/)
- [WinUSB Driver](https://docs.microsoft.com/en-us/windows-hardware/drivers/usbcon/winusb)
- [Device Manager](https://support.microsoft.com/en-us/windows/open-device-manager-a7f2db18-270f-6dd9-d289-cead87d1b93b)

## 📄 Licença

V-USB é licenciado sob GNU General Public License (GPL).

## 💡 Dicas

1. **Testar primeiro**: Use a função "Detect Device" antes de instalar
2. **Backup**: Guarde o driver original antes de atualizar
3. **Múltiplos dispositivos**: Gere drivers separados para cada dispositivo
4. **Documentação**: Inclua o README.txt no pacote de distribuição

## 🤝 Suporte

Para problemas ou dúvidas:
1. Verificar Troubleshooting acima
2. Consultar documentação V-USB
3. Verificar Device Manager para detalhes do erro
