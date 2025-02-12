class TemperatureController:
    def __init__(self):
        self.O_SC_ON = 0  # Señal para calefacción
        self.O_SR_ON = 0  # Señal para refrigeración
        self.O_ERROR_SYS = 0  # Señal de error

    def update(self, I_Tref, I_Treal, I_Error_SC=0, I_Error_SR=0, St_State="Running", T_combate=None):
        """
        Actualiza el estado del controlador según los parámetros de entrada.
        """
        if St_State == "Stopped":
            self.O_SC_ON, self.O_SR_ON = 0, 0
            return

        if I_Error_SC or I_Error_SR:
            self.O_ERROR_SYS = 1
        else:
            self.O_ERROR_SYS = 0

        if St_State == "Running":
            if I_Treal <= I_Tref - 0.51:
                self.O_SC_ON, self.O_SR_ON = 1, 0
            elif I_Treal >= I_Tref + 0.51:
                self.O_SC_ON, self.O_SR_ON = 0, 1
            else:
                self.O_SC_ON, self.O_SR_ON = 0, 0

        elif St_State == "Combat":
            time_within_range = 0  # Simula tiempo dentro del rango
            total_time = T_combate if T_combate else 10  # Default 10s

            for _ in range(total_time):
                if (I_Tref - 0.5) <= I_Treal <= (I_Tref + 0.5):
                    time_within_range += 1

            if time_within_range / total_time < 0.8:
                self.O_ERROR_SYS = 1

            # Aplicar lógica de temperatura igual que en Running
            if I_Treal <= I_Tref - 0.51:
                self.O_SC_ON, self.O_SR_ON = 1, 0
            elif I_Treal >= I_Tref + 0.51:
                self.O_SC_ON, self.O_SR_ON = 0, 1
            else:
                self.O_SC_ON, self.O_SR_ON = 0, 0
