from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_2, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor
import time

tank = MoveTank(OUTPUT_A, OUTPUT_B)
ultra = UltrasonicSensor(INPUT_2)
gyro = GyroSensor(INPUT_3)
time.sleep(0.5)

stan = "pylososennya"
vkhid = time.time()
start_time = time.time() 

def perekhid(novyi):
    global stan, vkhid
    print(f"{stan} -> {novyi}")
    stan = novyi
    vkhid = time.time()
    if novyi == "rozvorot":
        gyro.reset() 

print("Старт місії: Робот-пилосос")

while time.time() - start_time < 60:
    d = ultra.distance_centimeters

    if stan == "pylososennya":
        tank.on(SpeedPercent(40), SpeedPercent(40))
        if d < 40:
            perekhid("pidhid")

    elif stan == "pidhid":
        tank.on(SpeedPercent(15), SpeedPercent(15)) 
        if d < 12:
            perekhid("rozvorot")

    elif stan == "rozvorot":
        tank.on(SpeedPercent(30), SpeedPercent(-30)) 
        if gyro.angle >= 90:
            tank.off()
            perekhid("pylososennya") 


    if time.time() - vkhid > 10:
        print(f"Таймаут у стані {stan}! Робот застряг.")
        tank.on_for_seconds(SpeedPercent(-20), SpeedPercent(-20), 1) 
        perekhid("rozvorot") 

tank.off()
print("Прибирання завершено.")
