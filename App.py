from FT232HQ import FT232HQ

# Crear una instancia del dispositivo
ft232 = FT232HQ()
try:
    ft232.connect()
    
    # Configurar algunos pines como salidas
    ft232.configure_adbus(['ADBUS0', 'ADBUS1'], 'output')
    ft232.configure_acbus(['ACBUS0'], 'output')
    
    # Escribir valores
    ft232.write_adbus('ADBUS0', 1)  # Encender ADBUS0
    ft232.write_adbus('ADBUS1', 0)  # Apagar ADBUS1
    ft232.write_acbus('ACBUS0', 1)  # Encender ACBUS0
    
    # Leer todos los pines
    print("Estado ADBUS:", ft232.read_all_adbus())
    print("Estado ACBUS:", ft232.read_all_acbus())
    
finally:
    ft232.disconnect()
    
