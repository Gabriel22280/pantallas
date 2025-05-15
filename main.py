from machine import Pin, ADC, TouchPad, SPI, I2C
import max7219
import ssd1306
import dht
from time import sleep
import network
import ntptime
import time
import gfx
import framebuf
from imagen import (figura)

ancho = 128
alto = 64
archivo = "dog.pbm"
tiempo1 = 4
tiempo2 = 2

# Touch pad
Tp1 = TouchPad(Pin(13))
Tp2 = TouchPad(Pin(12))
Tp3 = TouchPad(Pin(14))

# Pantalla led
spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(18), mosi=Pin(23))
cs = Pin(5, Pin.OUT)
display = max7219.Matrix8x8(spi, cs, 4)

# Pantalla Oled
i2c = I2C(0, sda=Pin(21), scl=Pin(22))
display2 = ssd1306.SSD1306_I2C(128, 64, i2c)
grafica = gfx.GFX(ancho, alto, display2.pixel)

# Sensor de pulso cardiaco
cardio = ADC(Pin(34))
cardio.atten(ADC.ATTN_11DB)

# sensor de temperatura y humedad
th = dht.DHT11(Pin(4))


# Funciones

# WIFI para fecha y hora
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a la red')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Conectado:', wlan.ifconfig())

def sync_time():
    ntptime.settime()
    timezone_offset = -5 * 3600
    local_time = time.localtime(time.time() + timezone_offset)
    return local_time

# Imagenes
def mostrarDisplayInicio():
    horaActual = sync_time()
    fecha = str(horaActual[2]) + "/" + str(horaActual[1]) + "/" + str(horaActual[0]) 
    hora = str(horaActual[3]) + ":" + str(horaActual[4])
    fechaHora = fecha + " - " + hora
    long = len(fechaHora)*8
    for i in range(-long, 32, 1):
        display.text(fechaHora, i, 1, 1)
        display.show()
        sleep(0.05)
        display.fill(0)
    sleep(2)
    mensaje = "Bienvenido a todos"
    long = len(mensaje)*8
    for i in range(-long, 32, 1):
        display.text(mensaje, i, 1, 1)
        display.show()
        sleep(0.05)
        display.fill(0)
    display.vline(4,0,8,1)
    for i in range(-32, 32, 1):
        display.fill(0)
        display.line(i, 3, i+7, 3, 1)
        display.line(i+8, 4, i+11, 7, 1)
        display.line(i+12, 6, i+18, 0, 1)
        display.line(i+19, 1, i+24, 6, 1)
        display.line(i+25, 5, i+27, 3, 1)
        display.line(i+28, 3, i+31, 3, 1)
        display.show()
        sleep(0.08)

def mostrarOledInicio():
    horaActual = sync_time()
    fecha = str(horaActual[2]) + "/" + str(horaActual[1]) + "/" + str(horaActual[0]) 
    hora = str(horaActual[3]) + ":" + str(horaActual[4])
    persona1 = "Gabriel Aley"
    persona2 = "Yureicy Sierra"
    display2.fill(0)
    for i in range(ancho, -ancho, -1):
        display2.text(fecha, i, 10, 1)
        display2.text(hora, i, 20, 1)
        display2.text(persona1, i, 40, 1)
        display2.text(persona2, i, 50, 1)
        display2.show()
        sleep(0.005)
        display2.fill(0)
    for i in range(ancho, -ancho, -2):
        grafica.fill_rect(i+20, 10, 20, 20, 1)
        grafica.fill_rect(i+60, 10, 20, 20, 1)
        grafica.fill_rect(i+30, 40, 20, 20, 1)
        grafica.fill_rect(i+70, 40, 20, 20, 1)
        display2.show()
        sleep(0.005)
        display2.fill(0)

def graficarFiguras():
    display2.fill(0)
    buffer = bytearray(figura)
    fb = framebuf.FrameBuffer(buffer, 128, 64, framebuf.MONO_HLSB)
    display2.framebuf.blit(fb, 0, 0)
    display2.show()
    sleep(tiempo1)
    display2.fill(0)

    with open(archivo, 'rb') as f:
        f.readline()
        f.readline()
        data = bytearray(f.read())
    f.close
    fb = framebuf.FrameBuffer(data, 64, 64, framebuf.MONO_HLSB)
    display2.framebuf.blit(fb, 32, 0)
    display2.show()
    sleep(tiempo2)

def esperar():
    display.fill(0)
    display2.fill(0)
    display2.text("1. TH oled", 20, 10, 1)
    display2.text("2. TH led", 20, 20, 1)
    display2.text("3. pulso", 20, 30, 1)
    display2.show()
    sleep(0.05)

def thOled():
    display.fill(0)
    display2.fill(0)
    display.show()
    display2.show()
    th.measure()
    temp = th.temperature()
    hum = th.humidity()
    textoT = "Temp: " + str(temp)
    textoH = "Hum : " + str(hum)
    display2.text(textoT, 20, 20, 1)
    display2.text(textoH, 20, 30, 1)
    display2.show()
    sleep(2)

def thLed():
    display.fill(0)
    display2.fill(0)
    display.show()
    display2.show()
    th.measure()
    temp = th.temperature()
    hum = th.humidity()
    textoTH = "Temp: " + str(temp) + " - Hum : " + str(hum)
    long = len(textoTH)*8
    for i in range(-long, 32, 1):
        display.text(textoTH, i, 1, 1)
        display.show()
        sleep(0.05)
        display.fill(0)
    sleep(2)

def mostrarPulsoOled():
    display.fill(0)
    display2.fill(0)
    display.show()
    display2.show()
    valor = cardio.read()
    factor = 0.75
    antes = 512
    VFiltrado = factor*antes + (1-factor)*valor
    display2.fill(0)
    for i in range(64, -64, -1):
        display2.text(str(VFiltrado), 30, i, 1)
        display2.show()
        sleep(0.02)
        display2.fill(0)
    sleep(0.5)

def mostrarPulsoLed():
    display.fill(0)
    display2.fill(0)
    display.show()
    display2.show()
    valor = cardio.read()
    factor = 0.75
    antes = 512
    VFiltrado = factor*antes + (1-factor)*valor
    display2.fill(0)
    for i in range(8, -8, -1):
        display.text(str(int(VFiltrado)), 0, i, 1)
        display.show()
        sleep(0.1)
        display.fill(0)
    sleep(0.5)

# Inicializacion

usuario = 'iPhone'
contrasena = 'Aley2201'
connect_wifi(usuario, contrasena)
horaActual = sync_time()

display2.poweron()
estado = 0
mostrarDisplayInicio()
mostrarOledInicio()

while True:
    e1 = Tp1.read()
    if e1 < 150:
        estado = 2
    e2 = Tp2.read()
    if e2 < 150:
        estado = 3
    e3 = Tp3.read()
    if e3 < 150:
        if estado == 4:
            estado = 5
        else:
            estado = 4

    if estado == 0:
        graficarFiguras()
        estado = 1
    if estado == 1:
        esperar()
    if estado == 2:
        thOled()
    if estado == 3:
        thLed()
    if estado == 4:
        mostrarPulsoOled()
    if estado == 5:
        mostrarPulsoLed()
