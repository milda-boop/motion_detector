from machine import Pin, PWM
from time import sleep
import neopixel

pir_pin = Pin(22, Pin.IN)
led_pin = Pin (28, Pin.OUT)
p = neopixel.NeoPixel(Pin(28),1)
buzzer = PWM(Pin(18))
buzzer.freq(500)


# Flags to indicate motion detection state
motion_detected = False

motion_stopped_printed = False

def handle_interrupt(pin):
    global motion_detected
    if pin.value() == 1:  # Rising edge (motion detected)
        motion_detected = True
        #led_pin.value(1)  # Turn on the LED
        colour = (50, 0, 0)  # Red color
        #colour = set_brightness(colour)
        
        p.fill(colour)
        p.write()
        buzzer.duty_u16(1000)
        
    else:  # Falling edge (motion stopped)
        motion_detected = False
        #led_pin.value(0)  # Turn off the LED
        p.fill((0,0,0))
        p.write()
        buzzer.duty_u16(0)
        
pir_pin.irq(trigger=(Pin.IRQ_RISING|Pin.IRQ_FALLING), handler=handle_interrupt)

    
try:
    while True:
        if motion_detected and not motion_stopped_printed:
            print("Motion detected!")
            motion_stopped_printed = True  # Set the flag to indicate motion detected

        elif not motion_detected and motion_stopped_printed:
            print("Motion stopped")
            motion_stopped_printed = False  # Reset the flag

        sleep(0.1)  # Main loop delay

except KeyboardInterrupt:
    print("Keyboard interrupt")
    pir_pin.irq(trigger=0)  # Disable the interrupt
    p.fill((0,0,0))
    p.write()
    
except Exception as e:
    print("An unexpected exception occurred:", e)
