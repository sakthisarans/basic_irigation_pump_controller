from machine import Pin
import time
import _thread

phone_no=['+918925317177','+917904381916','+919865976062','+919442695271']


time.sleep(5)
moisture=machine.ADC(28)
gsm=machine.UART(0,baudrate=9600)
led=Pin(25,Pin.OUT)
led.low()
led1=Pin(13,Pin.OUT)
led1.high()
gsm.write("AT+CMGF=1\r\n")
time.sleep(0.5)
gsm.write("AT+CLIP=1\r\n")
time.sleep(0.5)
motor_stat=False
off_time=0
onby=''

def gsm_read():
    gsm1=gsm
    while True:
        if gsm1.any():
            val1=gsm1.read().decode().split()
            print(val1)
            if val1[0]=='+CLIP:':
                mobno=(val1[1].replace('\"',' ')).split()
                mobno=mobno[0].strip()
                print(mobno)
                global motor_stat
                if not(motor_stat) and (mobno in phone_no):
                    global onby
                    onby=mobno
                    gsm.write('ATH\r\n')
                    time.sleep(0.5)
                    motor_stat=True
                    led1.low()
                elif not(mobno in phone_no):
                    gsm.write('ATH\r\n')
                    time.sleep(0.5)
                    gsm.write(f'AT+CMGS="{mobno}"\r\n')
                    time.sleep(0.5)
                    gsm.write((chr(13)+'you are not allowed to call this number'+chr(26)+'\r\n'))
                else:
                    gsm.write('ATH\r\n')
                    time.sleep(0.5)
                    motor_stat=False
                    led1.high()
            elif val1[0]=='+CMT:':
                mobno=(val1[1].replace('\"',' ')).split()
                mobno=mobno[0].strip()
                print(mobno)
                process=val1[2].split('-')
                if process[0].lower()=='on' and (mobno in phone_no):
                    global onby
                    onby=mobno
                    led1.low()
                    global motor_stat
                    motor_stat=True
                    try:
                        global  off_time
                        off_tim=int(str(process[1]).strip())
                        off_time=off_tim
                    except :
                        print('error')
                elif (process[0].lower()=='off') and (mobno in phone_no):
                    onby=''
                    led1.high()
            time.sleep(1)

try:
    _thread.start_new_thread(gsm_read, ())
    time.sleep(1)
except Exception as ex:
    print('exception '+str(ex))
    
while True:
    if motor_stat and off_time>0:
        off_time=off_time-1
        if off_time==1:
            print('off')
            print(onby)
            gsm.write(f'AT+CMGS="{onby}"\r\n')
            time.sleep(0.5)
            gsm.write((chr(13)+'motor turned off by automatic system'+chr(26)+'\r\n'))
            time.sleep(1)
            onby=''
            motor_stat=False
            off_time=0
            led1.high()
    led.toggle()
    time.sleep(1)
    