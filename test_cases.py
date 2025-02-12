import pytest
from temperature_controller import TemperatureController

@pytest.fixture
def controller():
    return TemperatureController()

def test_Temp_Equal(controller):
    controller.update(I_Tref=25, I_Treal=25, St_State="Running")
    assert controller.O_SC_ON == 0
    assert controller.O_SR_ON == 0

def test_Temp_Higher(controller):
    controller.update(I_Tref=25, I_Treal=26, St_State="Running")
    assert controller.O_SC_ON == 0
    assert controller.O_SR_ON == 1

def test_Temp_Lower(controller):
    controller.update(I_Tref=25, I_Treal=24, St_State="Running")
    assert controller.O_SC_ON == 1
    assert controller.O_SR_ON == 0

def test_Heating_Fail(controller):
    controller.update(I_Tref=25, I_Treal=24, I_Error_SC=1, St_State="Running")
    assert controller.O_ERROR_SYS == 1

def test_Cooling_Fail(controller):
    controller.update(I_Tref=25, I_Treal=26, I_Error_SR=1, St_State="Running")
    assert controller.O_ERROR_SYS == 1

def test_Error_Over_2s(controller):
    for _ in range(3):  # Simula 3 ciclos de 2s
        controller.update(I_Tref=25, I_Treal=24, I_Error_SC=1, St_State="Running")
    assert controller.O_ERROR_SYS == 1  # Debería reiniciar pero en este caso simplemente sigue en error

def test_Stopped_State(controller):
    controller.update(I_Tref=25, I_Treal=24, St_State="Stopped")
    assert controller.O_SC_ON == 0
    assert controller.O_SR_ON == 0

def test_Combat_Mode(controller):
    controller.update(I_Tref=25, I_Treal=24.8, St_State="Combat", T_combate=10)
    assert controller.O_ERROR_SYS == 0  # En este caso, debería mantener el 80% del tiempo dentro del rango
    assert controller.O_SC_ON == 0
    assert controller.O_SR_ON == 0

def test_Combat_Failure(controller):
    controller.update(I_Tref=25, I_Treal=20, St_State="Combat", T_combate=10)
    assert controller.O_ERROR_SYS == 1  # Debería fallar porque la temperatura no se mantiene en el rango

def test_Sensor_Out_of_Range(controller):
    controller.update(I_Tref=25, I_Treal=-50, St_State="Running")
    assert controller.O_ERROR_SYS == 1
