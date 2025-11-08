#!/usr/bin/env python3
"""
Generate SODevs V-USB Driver Packages
Script para gerar drivers customizados para múltiplos Button Box com VID/PID diferentes
"""

import subprocess
import sys
from pathlib import Path


def generate_driver(name: str, manufacturer: str, vendor_id: str, product_id: str):
    """Generate a single driver package"""
    print(f"\n{'='*70}")
    print(f"Gerando driver: {name}")
    print(f"{'='*70}")
    
    cmd = [
        "python3",
        "generate_vusb_driver.py",
        "--name", name,
        "--manufacturer", manufacturer,
        "--vendor-id", vendor_id,
        "--product-id", product_id
    ]
    
    result = subprocess.run(cmd)
    return result.returncode == 0


def main():
    """Generate all SODevs drivers"""
    
    print("\n" + "="*70)
    print("SODevs V-USB Driver Generator")
    print("="*70)
    
    # Define your devices here
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
        },
        {
            "name": "Omega Buttons V3",
            "manufacturer": "SODevs",
            "vendor_id": "0x16c0",
            "product_id": "0x05e1",
            "description": "Button Box Versão 3"
        }
    ]
    
    print(f"\nGerando {len(devices)} drivers...\n")
    
    success_count = 0
    failed_count = 0
    
    for device in devices:
        print(f"\n📦 {device['description']}")
        print(f"   Nome: {device['name']}")
        print(f"   Fabricante: {device['manufacturer']}")
        print(f"   VID: {device['vendor_id']} | PID: {device['product_id']}")
        
        if generate_driver(
            device["name"],
            device["manufacturer"],
            device["vendor_id"],
            device["product_id"]
        ):
            success_count += 1
            print(f"   ✅ Sucesso!")
        else:
            failed_count += 1
            print(f"   ❌ Falha!")
    
    # Summary
    print(f"\n{'='*70}")
    print("Resumo da Geração")
    print(f"{'='*70}")
    print(f"✅ Sucesso: {success_count}/{len(devices)}")
    print(f"❌ Falha: {failed_count}/{len(devices)}")
    
    if failed_count == 0:
        print(f"\n✅ Todos os drivers foram gerados com sucesso!")
        print(f"\nDrivers disponíveis em: vusb_drivers/")
        print(f"\nPróximos passos:")
        print(f"  1. Compilar executável: python build_windows_installer.py")
        print(f"  2. Copiar para cada pasta de driver")
        print(f"  3. Zipar cada pasta para distribuição")
        return 0
    else:
        print(f"\n❌ Alguns drivers falharam na geração")
        return 1


if __name__ == "__main__":
    sys.exit(main())
