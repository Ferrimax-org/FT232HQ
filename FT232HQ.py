from pyftdi.spi import SpiController
from pyftdi.gpio import GpioController
import time

class FT232HQ:
    # Definición de pines
    ADBUS = {
        'ADBUS0': 0,
        'ADBUS1': 1,
        'ADBUS2': 2,
        'ADBUS3': 3,
        'ADBUS4': 4,
        'ADBUS5': 5,
        'ADBUS6': 6,
        'ADBUS7': 7
    }
    
    ACBUS = {
        'ACBUS0': 8,
        'ACBUS1': 9,
        'ACBUS2': 10,
        'ACBUS3': 11,
        'ACBUS4': 12,
        'ACBUS5': 13,
        'ACBUS6': 14,
        'ACBUS7': 15,
        'ACBUS8': 16,
        'ACBUS9': 17
    }

    def __init__(self, url='ftdi://ftdi:ft232h/1'):
        """
        Inicializa la conexión con el FT232HQ
        
        Args:
            url (str): URL del dispositivo FTDI (por defecto: ftdi://ftdi:ft232h/1)
        """
        self.url = url
        self.spi = None
        self.gpio = None
        self.connected = False
        self.adbus_direction = 0  # 0 = entrada, 1 = salida
        self.acbus_direction = 0  # 0 = entrada, 1 = salida

    def connect(self):
        """
        Establece la conexión con el dispositivo
        """
        try:
            # Inicializar controlador SPI
            self.spi = SpiController()
            self.spi.configure(self.url)
            
            # Inicializar controlador GPIO
            self.gpio = GpioController()
            self.gpio.open_from_url(self.url)
            
            # Configurar todos los pines como entradas por defecto
            self.set_all_pins_as_input()
            
            self.connected = True
            print("Conexión establecida exitosamente")
        except Exception as e:
            print(f"Error al conectar: {str(e)}")
            self.connected = False

    def set_all_pins_as_input(self):
        """
        Configura todos los pines como entradas
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        
        # Configurar ADBUS como entradas
        for pin in self.ADBUS.values():
            self.gpio.set_direction(pin, 0)
        
        # Configurar ACBUS como entradas
        for pin in self.ACBUS.values():
            self.gpio.set_direction(pin, 0)
        
        self.adbus_direction = 0
        self.acbus_direction = 0

    def configure_adbus(self, pins, direction='input'):
        """
        Configura los pines ADBUS como entradas o salidas
        
        Args:
            pins (list): Lista de nombres de pines (ej: ['ADBUS0', 'ADBUS1'])
            direction (str): 'input' o 'output'
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        
        dir_value = 1 if direction == 'output' else 0
        
        for pin_name in pins:
            if pin_name in self.ADBUS:
                self.gpio.set_direction(self.ADBUS[pin_name], dir_value)
        
        self.adbus_direction = dir_value

    def configure_acbus(self, pins, direction='input'):
        """
        Configura los pines ACBUS como entradas o salidas
        
        Args:
            pins (list): Lista de nombres de pines (ej: ['ACBUS0', 'ACBUS1'])
            direction (str): 'input' o 'output'
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        
        dir_value = 1 if direction == 'output' else 0
        
        for pin_name in pins:
            if pin_name in self.ACBUS:
                self.gpio.set_direction(self.ACBUS[pin_name], dir_value)
        
        self.acbus_direction = dir_value

    def write_adbus(self, pin_name, value):
        """
        Escribe un valor en un pin ADBUS
        
        Args:
            pin_name (str): Nombre del pin (ej: 'ADBUS0')
            value (int): 0 o 1
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        
        if pin_name in self.ADBUS:
            self.gpio.write(self.ADBUS[pin_name], value)

    def write_acbus(self, pin_name, value):
        """
        Escribe un valor en un pin ACBUS
        
        Args:
            pin_name (str): Nombre del pin (ej: 'ACBUS0')
            value (int): 0 o 1
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        
        if pin_name in self.ACBUS:
            self.gpio.write(self.ACBUS[pin_name], value)

    def read_adbus(self, pin_name):
        """
        Lee el valor de un pin ADBUS
        
        Args:
            pin_name (str): Nombre del pin (ej: 'ADBUS0')
            
        Returns:
            int: 0 o 1
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        
        if pin_name in self.ADBUS:
            return self.gpio.read(self.ADBUS[pin_name])

    def read_acbus(self, pin_name):
        """
        Lee el valor de un pin ACBUS
        
        Args:
            pin_name (str): Nombre del pin (ej: 'ACBUS0')
            
        Returns:
            int: 0 o 1
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        
        if pin_name in self.ACBUS:
            return self.gpio.read(self.ACBUS[pin_name])

    def read_all_adbus(self):
        """
        Lee el estado de todos los pines ADBUS
        
        Returns:
            dict: Diccionario con el estado de cada pin
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        
        return {pin_name: self.read_adbus(pin_name) for pin_name in self.ADBUS}

    def read_all_acbus(self):
        """
        Lee el estado de todos los pines ACBUS
        
        Returns:
            dict: Diccionario con el estado de cada pin
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        
        return {pin_name: self.read_acbus(pin_name) for pin_name in self.ACBUS}

    def disconnect(self):
        """
        Cierra la conexión con el dispositivo
        """
        if self.spi:
            self.spi.terminate()
        if self.gpio:
            self.gpio.close()
        self.connected = False
        print("Conexión cerrada")

    def write_spi(self, data, cs=0, freq=30E6):
        """
        Escribe datos a través del bus SPI
        
        Args:
            data (bytes): Datos a escribir
            cs (int): Número del pin CS a usar
            freq (float): Frecuencia del bus SPI en Hz
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        
        port = self.spi.get_port(cs=cs, freq=freq, mode=0)
        port.write(data)

    def read_spi(self, length, cs=0, freq=30E6):
        """
        Lee datos a través del bus SPI
        
        Args:
            length (int): Cantidad de bytes a leer
            cs (int): Número del pin CS a usar
            freq (float): Frecuencia del bus SPI en Hz
            
        Returns:
            bytes: Datos leídos
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        
        port = self.spi.get_port(cs=cs, freq=freq, mode=0)
        return port.read(length)

    def set_gpio(self, pins, values):
        """
        Establece el estado de los pines GPIO
        
        Args:
            pins (list): Lista de pines a configurar
            values (list): Valores correspondientes (0 o 1)
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        
        for pin, value in zip(pins, values):
            self.gpio.set_direction(pin, 1)  # 1 = salida
            self.gpio.write(pin, value)

    def read_gpio(self, pins):
        """
        Lee el estado de los pines GPIO
        
        Args:
            pins (list): Lista de pines a leer
            
        Returns:
            list: Valores leídos
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        
        values = []
        for pin in pins:
            self.gpio.set_direction(pin, 0)  # 0 = entrada
            values.append(self.gpio.read(pin))
        return values

if __name__ == "__main__":
    # Ejemplo de uso
    ft232 = FT232HQ()
    try:
        ft232.connect()
        
        # Ejemplo de configuración de pines
        ft232.configure_adbus(['ADBUS0', 'ADBUS1'], 'output')
        ft232.configure_acbus(['ACBUS0', 'ACBUS1'], 'input')
        
        # Ejemplo de escritura
        ft232.write_adbus('ADBUS0', 1)
        ft232.write_adbus('ADBUS1', 0)
        
        # Ejemplo de lectura
        print("Estado ADBUS:", ft232.read_all_adbus())
        print("Estado ACBUS:", ft232.read_all_acbus())
        
        time.sleep(1)
    finally:
        ft232.disconnect()
