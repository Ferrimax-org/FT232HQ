from pyftdi.usbtools import UsbTools

def list_ftdi_devices():
    print("Buscando dispositivos FTDI...")
    try:
        devices = UsbTools.find_all()
        if not devices:
            print("No se encontraron dispositivos FTDI")
            return
        
        print("\nDispositivos FTDI encontrados:")
        for device in devices:
            print(f"\nURL: {device}")
            print(f"Vendor ID: 0x{device.vid:04x}")
            print(f"Product ID: 0x{device.pid:04x}")
            print(f"Serial Number: {device.sn}")
            print("-" * 50)
    except Exception as e:
        print(f"Error al buscar dispositivos: {str(e)}")

if __name__ == "__main__":
    list_ftdi_devices() 