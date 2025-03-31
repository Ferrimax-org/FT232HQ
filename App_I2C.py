from FT232HQ_I2C import FT232HQ_I2C

# Crear instancia del controlador I2C
i2c = FT232HQ_I2C(freq=100000)  # 100kHz

try:
    # Conectar al dispositivo
    i2c.connect()
    
    # Escanear dispositivos en el bus
    devices = i2c.scan_bus()
    print(f"Dispositivos encontrados: {[hex(addr) for addr in devices]}")
    
    if devices:
        # Ejemplo de escritura en un registro
        device_addr = devices[0]
        register_addr = 0x00
        data = [0x01, 0x02, 0x03]
        
        if i2c.write_register(device_addr, register_addr, data):
            print("Escritura exitosa")
        
        # Leer el registro
        read_data = i2c.read_register(device_addr, register_addr, 3)
        print(f"Datos leídos: {[hex(x) for x in read_data]}")

finally:
    # Cerrar la conexión
    i2c.disconnect()