from FT232HQ_I2C import FT232HQ_I2C
from TMP100 import TMP100

# Inicializar el bus I2C
i2c = FT232HQ_I2C(freq=100000)  # 100kHz

try:
    i2c.connect()
    
    # Crear instancia del sensor
    # address='00' significa A0=0, A1=0
    sensor = TMP100(i2c, address='00', resolution=12)
    
    # Leer temperatura
    temp = sensor.read_temperature()
    print(f"Temperatura: {temp:.2f}°C")
    
    # Configurar límites de temperatura
    sensor.set_high_limit(30.0)  # 30°C
    sensor.set_low_limit(20.0)   # 20°C
    
    # Cambiar resolución
    sensor.set_resolution(11)
    
    # Leer configuración actual
    config = sensor.get_configuration()
    print("\nConfiguración:")
    for key, value in config.items():
        print(f"{key}: {value}")

finally:
    i2c.disconnect()
    