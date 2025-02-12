import time
import random

class TemperatureController:
    def __init__(self):
        self.I_Tref = 25.0  # Temperatura de referencia en grados Celsius
        self.I_Treal = 25.0  # Temperatura real inicial
        self.O_SC_ON = False  # Estado del sistema de calefacción
        self.O_SR_ON = False  # Estado del sistema de refrigeración
        self.I_Error_SC = False  # Error en calefacción
        self.I_Error_SR = False  # Error en refrigeración
        self.O_ERROR_SYS = False  # Error general del sistema
        self.state = "stopped"  # Estados: stopped, running, combat
        self.combat_time = 0
    
    def check_subsystems(self):
        """ Verifica el estado de los subsistemas """
        if self.I_Error_SC or self.I_Error_SR:
            self.O_ERROR_SYS = True
            print("Error en subsistemas detectado!")
            return False
        print("Subsistemas operativos.")
        return True
    
    def control_temperature(self):
        """ Controla la temperatura para alcanzar la referencia """
        if not self.check_subsystems():
            return
        
        if self.I_Treal < self.I_Tref - 0.5:
            self.O_SC_ON = True
            self.O_SR_ON = False
            print("Activando calefacción.")
        elif self.I_Treal > self.I_Tref + 0.5:
            self.O_SC_ON = False
            self.O_SR_ON = True
            print("Activando refrigeración.")
        else:
            self.O_SC_ON = False
            self.O_SR_ON = False
            print("Temperatura en rango, no se activa calefacción ni refrigeración.")
    
    def enter_combat_mode(self, target_temp, duration):
        """ Modo combate: Mantener temperatura en un rango durante un tiempo determinado """
        self.state = "combat"
        self.I_Tref = target_temp
        self.combat_time = duration
        print(f"Entrando en modo combate. Objetivo: {target_temp}°C por {duration} segundos.")
        start_time = time.time()
        while time.time() - start_time < duration:
            self.control_temperature()
            time.sleep(2)
    
    def handle_errors(self):
        """ Manejo de errores y reinicio si es necesario """
        if self.O_ERROR_SYS:
            print("Error detectado en el sistema. Esperando 2 segundos...")
            time.sleep(2)
            if self.O_ERROR_SYS:
                self.restart_system()
    
    def restart_system(self):
        """ Reinicia el sistema en caso de error prolongado """
        print("Reiniciando el sistema...")
        self.O_ERROR_SYS = False
        self.I_Error_SC = False
        self.I_Error_SR = False
        self.state = "stopped"
        print("Sistema reiniciado correctamente.")
    
    def run(self):
        """ Ejecuta el controlador en su estado normal """
        self.state = "running"
        print("Iniciando controlador de temperatura...")
        while True:
            self.I_Treal += random.uniform(-0.5, 0.5)  # Simulación de variaciones en la temperatura
            print(f"Temperatura actual: {self.I_Treal:.2f}°C")
            self.control_temperature()
            self.handle_errors()
            print(f"Estado: {self.state} | SC: {self.O_SC_ON} | SR: {self.O_SR_ON} | Error: {self.O_ERROR_SYS}\n")
            time.sleep(2)

if __name__ == "__main__":
    controller = TemperatureController()
    controller.run()
