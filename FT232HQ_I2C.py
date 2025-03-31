from pyftdi.i2c import I2cController
import time

class FT232HQ_I2C:
    def __init__(self, url='ftdi://ftdi:ft232h/1', freq=100000):
        """
        Inicializa el controlador I2C
        
        Args:
            url (str): URL del dispositivo FTDI
            freq (int): Frecuencia del bus I2C en Hz (por defecto 100kHz)
        """
        self.url = url
        self.freq = freq
        self.i2c = None
        self.connected = False
        
        # Configuración por defecto de pines I2C
        # SDA: ADBUS0
        # SCL: ADBUS1
        self.sda_pin = 0
        self.scl_pin = 1

    def connect(self):
        """
        Establece la conexión I2C
        """
        try:
            self.i2c = I2cController()
            self.i2c.configure(self.url, freq=self.freq)
            self.connected = True
            print("Conexión I2C establecida exitosamente")
        except Exception as e:
            print(f"Error al conectar I2C: {str(e)}")
            self.connected = False

    def disconnect(self):
        """
        Cierra la conexión I2C
        """
        if self.i2c:
            self.i2c.terminate()
        self.connected = False
        print("Conexión I2C cerrada")

    def start(self):
        """
        Genera la condición de START en el bus I2C
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        self.i2c.get_port().start()

    def stop(self):
        """
        Genera la condición de STOP en el bus I2C
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        self.i2c.get_port().stop()

    def write_byte(self, data):
        """
        Escribe un byte en el bus I2C
        
        Args:
            data (int): Byte a escribir (0-255)
            
        Returns:
            bool: True si el dispositivo respondió con ACK
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        return self.i2c.get_port().write([data]) == 1

    def read_byte(self, ack=True):
        """
        Lee un byte del bus I2C
        
        Args:
            ack (bool): Si se debe enviar ACK después de la lectura
            
        Returns:
            int: Byte leído (0-255)
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        return self.i2c.get_port().read(1)[0]

    def write_data(self, address, data):
        """
        Escribe datos a un dispositivo I2C
        
        Args:
            address (int): Dirección del dispositivo (7 bits)
            data (list): Lista de bytes a escribir
            
        Returns:
            bool: True si la escritura fue exitosa
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        
        try:
            port = self.i2c.get_port(address)
            port.write(data)
            return True
        except Exception as e:
            print(f"Error en escritura I2C: {str(e)}")
            return False

    def read_data(self, address, length):
        """
        Lee datos de un dispositivo I2C
        
        Args:
            address (int): Dirección del dispositivo (7 bits)
            length (int): Cantidad de bytes a leer
            
        Returns:
            list: Lista de bytes leídos
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        
        try:
            port = self.i2c.get_port(address)
            return port.read(length)
        except Exception as e:
            print(f"Error en lectura I2C: {str(e)}")
            return []

    def scan_bus(self):
        """
        Escanea el bus I2C en busca de dispositivos
        
        Returns:
            list: Lista de direcciones de dispositivos encontrados
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        
        devices = []
        for addr in range(128):  # Escanear direcciones 0-127
            try:
                port = self.i2c.get_port(addr)
                port.write([])  # Intenta escribir 0 bytes
                devices.append(addr)
            except:
                continue
        return devices

    def write_register(self, address, register, data):
        """
        Escribe datos en un registro específico de un dispositivo I2C
        
        Args:
            address (int): Dirección del dispositivo (7 bits)
            register (int): Dirección del registro
            data (list): Datos a escribir
            
        Returns:
            bool: True si la escritura fue exitosa
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        
        try:
            port = self.i2c.get_port(address)
            port.write([register] + data)
            return True
        except Exception as e:
            print(f"Error en escritura de registro: {str(e)}")
            return False

    def read_register(self, address, register, length=1):
        """
        Lee datos de un registro específico de un dispositivo I2C
        
        Args:
            address (int): Dirección del dispositivo (7 bits)
            register (int): Dirección del registro
            length (int): Cantidad de bytes a leer
            
        Returns:
            list: Datos leídos del registro
        """
        if not self.connected:
            raise Exception("Dispositivo no conectado")
        
        try:
            port = self.i2c.get_port(address)
            port.write([register])
            return port.read(length)
        except Exception as e:
            print(f"Error en lectura de registro: {str(e)}")
            return []

if __name__ == "__main__":
    # Ejemplo de uso
    i2c = FT232HQ_I2C(freq=100000)  # 100kHz
    
    try:
        i2c.connect()
        
        # Escanear el bus
        print("Escaneando bus I2C...")
        devices = i2c.scan_bus()
        print(f"Dispositivos encontrados: {[hex(addr) for addr in devices]}")
        
        if devices:
            # Ejemplo de escritura y lectura
            device_addr = devices[0]
            print(f"\nProbando dispositivo en dirección {hex(device_addr)}")
            
            # Escribir datos
            test_data = [0x01, 0x02, 0x03]
            if i2c.write_data(device_addr, test_data):
                print("Escritura exitosa")
            
            # Leer datos
            read_data = i2c.read_data(device_addr, 3)
            print(f"Datos leídos: {[hex(x) for x in read_data]}")
        
    finally:
        i2c.disconnect() 