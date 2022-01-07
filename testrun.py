from HW import thermalSensor
from HW import crollingThermal
import time
# information
time.sleep(1)
mlx,lepton=crollingThermal.calibratedTemperature()
wrist=thermalSensor.checkWristTemperature()
print("wrist="+str(wrist))
wrist=float(wrist)+float(mlx)
wrist=round(wrist,2)
print("calibratedWrist="+str(wrist))


