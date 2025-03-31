from FT232HQ_I2C import FT232HQ_I2C
import time

class TMP100:
    # Direcciones I2C posibles del TMP100 (A0 y A1 pines)
    ADDRESSES = {
        '00': 0x48,  # A0=0, A1=0
        '01': 0x49,  # A0=0, A1=1
        '10': 0x4A,  # A0=1, A1=0
        '11': 0x4B   # A0=1, A1=1
    }
    
    # Registros del TMP100
    REGISTERS = {
        'TEMPERATURE': 0x00,
        'CONFIGURATION': 0x01,
        'TEMP_HIGH': 0x02,
        'TEMP_LOW': 0x03
    }
    
    # Bits de configuración
    CONFIG_BITS = {
        'SD': 0x01,    # Shutdown mode
        'TM': 0x02,    # Thermostat mode
        'POL': 0x04,   # Thermostat polarity
        'F0': 0x08,    # Fault queue
        'F1': 0x10,    # Fault queue
        'R0': 0x20,    # Resolution
        'R1': 0x40,    # Resolution
        'OS': 0x80     # One-shot
    }
    
    # Resoluciones disponibles
    RESOLUTIONS = {
        9: 0x00,   # 9 bits (0.5°C)
        10: 0x20,  # 10 bits (0.25°C)
        11: 0x40,  # 11 bits (0.125°C)
        12: 0x60   # 12 bits (0.0625°C)
    }

    def __init__(self, i2c, address='00', resolution=12):
        """
        Inicializa el sensor TMP100
        
        Args:
            i2c (FT232HQ_I2C): Instancia del controlador I2C
            address (str): Dirección I2C del sensor ('00', '01', '10', '11')
            resolution (int): Resolución en bits (9-12)
        """
        self.i2c = i2c
        self.address = self.ADDRESSES[address]
        self.resolution = resolution
        
        if resolution not in self.RESOLUTIONS:
            raise ValueError("Resolución debe ser 9, 10, 11 o 12 bits")
        
        # Configurar el sensor
        self._configure()

    def _configure(self):
        """
        Configura el sensor con la resolución especificada
        """
        config = self.RESOLUTIONS[self.resolution]
        self.i2c.write_register(self.address, self.REGISTERS['CONFIGURATION'], [config])

    def read_temperature(self):
        """
        Lee la temperatura actual
        
        Returns:
            float: Temperatura en grados Celsius
        """
        # Leer el registro de temperatura (2 bytes)
        data = self.i2c.read_register(self.address, self.REGISTERS['TEMPERATURE'], 2)
        
        if not data:
            raise Exception("Error al leer la temperatura")
        
        # Convertir los bytes a temperatura
        temp_raw = (data[0] << 8) | data[1]  # Combinar los dos bytes
        temp_raw = temp_raw >> (16 - self.resolution)  # Ajustar según la resolución
        
        # Convertir a grados Celsius
        # Para 12 bits: 1 LSB = 0.0625°C
        # Para 11 bits: 1 LSB = 0.125°C
        # Para 10 bits: 1 LSB = 0.25°C
        # Para 9 bits: 1 LSB = 0.5°C
        lsb_size = 0.0625 * (2 ** (12 - self.resolution))
        temperature = temp_raw * lsb_size
        
        return temperature

    def set_high_limit(self, temperature):
        """
        Establece el límite superior de temperatura
        
        Args:
            temperature (float): Temperatura en grados Celsius
        """
        temp_raw = int(temperature / (0.0625 * (2 ** (12 - self.resolution))))
        data = [(temp_raw >> 8) & 0xFF, temp_raw & 0xFF]
        self.i2c.write_register(self.address, self.REGISTERS['TEMP_HIGH'], data)

    def set_low_limit(self, temperature):
        """
        Establece el límite inferior de temperatura
        
        Args:
            temperature (float): Temperatura en grados Celsius
        """
        temp_raw = int(temperature / (0.0625 * (2 ** (12 - self.resolution))))
        data = [(temp_raw >> 8) & 0xFF, temp_raw & 0xFF]
        self.i2c.write_register(self.address, self.REGISTERS['TEMP_LOW'], data)

    def set_resolution(self, resolution):
        """
        Cambia la resolución del sensor
        
        Args:
            resolution (int): Nueva resolución en bits (9-12)
        """
        if resolution not in self.RESOLUTIONS:
            raise ValueError("Resolución debe ser 9, 10, 11 o 12 bits")
        
        self.resolution = resolution
        self._configure()

    def get_configuration(self):
        """
        Lee la configuración actual del sensor
        
        Returns:
            dict: Diccionario con la configuración actual
        """
        data = self.i2c.read_register(self.address, self.REGISTERS['CONFIGURATION'], 1)
        if not data:
            raise Exception("Error al leer la configuración")
        
        config = data[0]
        return {
            'shutdown': bool(config & self.CONFIG_BITS['SD']),
            'thermostat_mode': bool(config & self.CONFIG_BITS['TM']),
            'thermostat_polarity': bool(config & self.CONFIG_BITS['POL']),
            'fault_queue': ((config & self.CONFIG_BITS['F1']) >> 4) | (config & self.CONFIG_BITS['F0']),
            'resolution': self.resolution,
            'one_shot': bool(config & self.CONFIG_BITS['OS'])
        }

if __name__ == "__main__":
    # Ejemplo de uso
    i2c = FT232HQ_I2C(freq=100000)  # 100kHz
    
    try:
        i2c.connect()
        
        # Crear instancia del sensor (dirección '00', resolución 12 bits)
        sensor = TMP100(i2c, address='00', resolution=12)
        
        # Leer temperatura
        temp = sensor.read_temperature()
        print(f"Temperatura actual: {temp:.2f}°C")
        
        # Configurar límites
        sensor.set_high_limit(30.0)  # 30°C
        sensor.set_low_limit(20.0)   # 20°C
        
        # Leer configuración
        config = sensor.get_configuration()
        print("\nConfiguración actual:")
        for key, value in config.items():
            print(f"{key}: {value}")
        
        # Cambiar resolución a 11 bits
        sensor.set_resolution(11)
        temp = sensor.read_temperature()
        print(f"\nTemperatura con resolución de 11 bits: {temp:.2f}°C")
        
    finally:
        i2c.disconnect() 