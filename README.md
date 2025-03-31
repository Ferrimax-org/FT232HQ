# Controlador FT232HQ con Python

Este proyecto implementa una interfaz Python para controlar el chip FT232HQ a través de USB, proporcionando acceso a sus funcionalidades de GPIO, SPI e I2C. También incluye un módulo específico para el sensor de temperatura TMP100.

## Requisitos

- Python 3.6 o superior
- Drivers FTDI instalados en el sistema
- Dependencias Python:

    ```
  pyftdi>=0.56.0
  pyusb>=1.2.1
  ```

## Instalación

1. Instalar los drivers FTDI:
   - Descargar e instalar los drivers desde: https://ftdichip.com/drivers/d2xx-drivers/

2. Instalar las dependencias Python:

   ```bash
   pip install -r requirements.txt
   ```

## Estructura del Proyecto

- `FT232HQ.py`: Módulo principal para controlar el FT232HQ
- `FT232HQ_I2C.py`: Módulo para comunicación I2C
- `TMP100.py`: Módulo para controlar el sensor de temperatura TMP100

## Módulo FT232HQ

### Características

- Control de pines GPIO (ADBUS[7:0] y ACBUS[9:0])
- Comunicación SPI
- Comunicación I2C

### Uso Básico

```python
from FT232HQ import FT232HQ

ft232 = FT232HQ()
try:
    ft232.connect()
    
    # Configurar pines como salidas
    ft232.configure_adbus(['ADBUS0', 'ADBUS1'], 'output')
    
    # Escribir en pines
    ft232.write_adbus('ADBUS0', 1)
    
    # Leer pines
    print(ft232.read_all_adbus())
    
finally:
    ft232.disconnect()
```

## Módulo FT232HQ_I2C

### Características

- Configuración de frecuencia del bus
- Funciones de bajo nivel (START, STOP, read/write)
- Escaneo de dispositivos
- Manejo de registros

### Uso Básico

```python
from FT232HQ_I2C import FT232HQ_I2C

i2c = FT232HQ_I2C(freq=100000)  # 100kHz
try:
    i2c.connect()
    
    # Escanear dispositivos
    devices = i2c.scan_bus()
    print(f"Dispositivos encontrados: {[hex(addr) for addr in devices]}")
    
    # Escribir datos
    i2c.write_data(0x48, [0x01, 0x02, 0x03])
    
    # Leer datos
    data = i2c.read_data(0x48, 3)
    
finally:
    i2c.disconnect()
```

## Módulo TMP100

### Características

- Soporte para 4 direcciones I2C (A0 y A1 pines)
- Resoluciones de 9-12 bits
- Límites de temperatura configurables
- Modo termostato
- Modo de bajo consumo

### Uso Básico

```python
from FT232HQ_I2C import FT232HQ_I2C
from TMP100 import TMP100

i2c = FT232HQ_I2C(freq=100000)
try:
    i2c.connect()
    
    # Crear instancia del sensor
    sensor = TMP100(i2c, address='00', resolution=12)
    
    # Leer temperatura
    temp = sensor.read_temperature()
    print(f"Temperatura: {temp:.2f}°C")
    
    # Configurar límites
    sensor.set_high_limit(30.0)
    sensor.set_low_limit(20.0)
    
finally:
    i2c.disconnect()
```

## Configuración de Pines

### Pines GPIO

- ADBUS[7:0]: Pines 0-7
- ACBUS[9:0]: Pines 8-17

### Pines I2C

- SDA: ADBUS0 (pin 0)
- SCL: ADBUS1 (pin 1)

### Pines SPI

- MOSI: ADBUS0 (pin 0)
- MISO: ADBUS1 (pin 1)
- SCK: ADBUS2 (pin 2)
- CS: Configurable

## Solución de Problemas

1. **Error de conexión**:
   - Verificar que los drivers FTDI estén instalados
   - Comprobar que el dispositivo esté conectado
   - Verificar la URL del dispositivo en el código

2. **Error de comunicación I2C**:
   - Verificar las conexiones físicas
   - Comprobar la dirección del dispositivo
   - Asegurar que la frecuencia del bus sea compatible

3. **Error de lectura del sensor**:
   - Verificar la alimentación del sensor
   - Comprobar las conexiones I2C
   - Verificar la dirección del sensor

## Contribuir

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Fork el repositorio
2. Crea una rama para tu característica
3. Commit tus cambios
4. Push a la rama
5. Crea un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
