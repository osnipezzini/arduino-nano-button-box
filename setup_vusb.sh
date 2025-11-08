#!/bin/bash
# V-USB Setup Helper Script
# Facilita o processo de compilação e flash do bootloader V-USB

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

check_command() {
    if ! command -v $1 &> /dev/null; then
        return 1
    fi
    return 0
}

# Main menu
show_menu() {
    echo -e "\n${BLUE}V-USB Bootloader Setup${NC}"
    echo "1) Check dependencies"
    echo "2) List available MCUs"
    echo "3) Build bootloader"
    echo "4) Flash bootloader"
    echo "5) Full setup (build + flash)"
    echo "6) Backup current bootloader"
    echo "7) Restore bootloader"
    echo "8) Exit"
    echo -n "Select option: "
}

# Check dependencies
check_deps() {
    print_header "Checking Dependencies"
    
    local missing=0
    
    for cmd in python3 avr-gcc avrdude make; do
        if check_command $cmd; then
            print_success "$cmd installed"
        else
            print_error "$cmd not found"
            missing=$((missing + 1))
        fi
    done
    
    if [ $missing -eq 0 ]; then
        print_success "All dependencies installed!"
        return 0
    else
        print_error "$missing dependencies missing"
        echo -e "\n${YELLOW}Install with:${NC}"
        echo "  Ubuntu/Debian: sudo apt-get install gcc-avr avr-libc avrdude make"
        echo "  macOS: brew install avr-gcc avrdude"
        return 1
    fi
}

# List MCUs
list_mcus() {
    print_header "Available MCUs"
    python3 build_vusb_bootloader.py --list-mcus
}

# Build bootloader
build_bootloader() {
    print_header "Build V-USB Bootloader"
    
    echo "Available MCUs: nano, micro, leonardo, uno, attiny85"
    read -p "Select MCU: " mcu
    
    read -p "Device name (max 32 chars) [Button Box]: " name
    name=${name:-"Button Box"}
    
    read -p "Vendor ID [0x16c0]: " vendor_id
    vendor_id=${vendor_id:-"0x16c0"}
    
    read -p "Product ID [0x05df]: " product_id
    product_id=${product_id:-"0x05df"}
    
    print_info "Building bootloader..."
    python3 build_vusb_bootloader.py \
        --mcu "$mcu" \
        --name "$name" \
        --vendor-id "$vendor_id" \
        --product-id "$product_id"
    
    if [ $? -eq 0 ]; then
        print_success "Bootloader built successfully!"
        echo -e "\n${BLUE}Output:${NC} bootloader_builds/bootloader_${mcu}_${name// /_}.hex"
    else
        print_error "Build failed"
        return 1
    fi
}

# Flash bootloader
flash_bootloader() {
    print_header "Flash V-USB Bootloader"
    
    echo "Available MCUs: atmega328p, atmega32u4, attiny85"
    read -p "Select MCU: " mcu
    
    read -p "Hex file path: " hex_file
    
    if [ ! -f "$hex_file" ]; then
        print_error "File not found: $hex_file"
        return 1
    fi
    
    read -p "Serial port (e.g., /dev/ttyUSB0, COM3): " port
    
    read -p "Baud rate [19200]: " baud
    baud=${baud:-"19200"}
    
    read -p "Execute full sequence? (backup, fuses, flash, verify) [y/n]: " full
    
    print_info "Flashing bootloader..."
    
    if [ "$full" = "y" ] || [ "$full" = "Y" ]; then
        python3 flash_bootloader.py \
            --mcu "$mcu" \
            --hex "$hex_file" \
            --port "$port" \
            --baud "$baud" \
            --full
    else
        python3 flash_bootloader.py \
            --mcu "$mcu" \
            --hex "$hex_file" \
            --port "$port" \
            --baud "$baud"
    fi
    
    if [ $? -eq 0 ]; then
        print_success "Bootloader flashed successfully!"
    else
        print_error "Flash failed"
        return 1
    fi
}

# Full setup
full_setup() {
    print_header "Full V-USB Setup"
    
    print_info "Step 1: Check dependencies"
    if ! check_deps; then
        print_error "Dependencies missing. Please install them first."
        return 1
    fi
    
    print_info "Step 2: Build bootloader"
    build_bootloader
    if [ $? -ne 0 ]; then
        return 1
    fi
    
    print_info "Step 3: Flash bootloader"
    flash_bootloader
}

# Backup bootloader
backup_bootloader() {
    print_header "Backup Current Bootloader"
    
    echo "Available MCUs: atmega328p, atmega32u4, attiny85"
    read -p "Select MCU: " mcu
    
    read -p "Serial port (e.g., /dev/ttyUSB0, COM3): " port
    
    read -p "Output file [bootloader_backup.hex]: " output
    output=${output:-"bootloader_backup.hex"}
    
    read -p "Baud rate [19200]: " baud
    baud=${baud:-"19200"}
    
    print_info "Backing up bootloader..."
    python3 flash_bootloader.py \
        --mcu "$mcu" \
        --port "$port" \
        --baud "$baud" \
        --backup "$output"
    
    if [ $? -eq 0 ]; then
        print_success "Bootloader backed up to: $output"
    else
        print_error "Backup failed"
        return 1
    fi
}

# Restore bootloader
restore_bootloader() {
    print_header "Restore Bootloader"
    
    echo "Available MCUs: atmega328p, atmega32u4, attiny85"
    read -p "Select MCU: " mcu
    
    read -p "Backup file to restore: " hex_file
    
    if [ ! -f "$hex_file" ]; then
        print_error "File not found: $hex_file"
        return 1
    fi
    
    read -p "Serial port (e.g., /dev/ttyUSB0, COM3): " port
    
    read -p "Baud rate [19200]: " baud
    baud=${baud:-"19200"}
    
    print_warning "This will restore the bootloader from backup"
    read -p "Continue? [y/n]: " confirm
    
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        print_info "Cancelled"
        return 0
    fi
    
    print_info "Restoring bootloader..."
    python3 flash_bootloader.py \
        --mcu "$mcu" \
        --hex "$hex_file" \
        --port "$port" \
        --baud "$baud" \
        --full
    
    if [ $? -eq 0 ]; then
        print_success "Bootloader restored successfully!"
    else
        print_error "Restore failed"
        return 1
    fi
}

# Main loop
main() {
    print_header "V-USB Bootloader Setup Helper"
    
    while true; do
        show_menu
        read -r option
        
        case $option in
            1) check_deps ;;
            2) list_mcus ;;
            3) build_bootloader ;;
            4) flash_bootloader ;;
            5) full_setup ;;
            6) backup_bootloader ;;
            7) restore_bootloader ;;
            8) 
                print_info "Exiting..."
                exit 0
                ;;
            *)
                print_error "Invalid option"
                ;;
        esac
    done
}

# Run main
main
