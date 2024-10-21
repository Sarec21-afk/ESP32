import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports


class ESP32:
    def __init__(self, root):
        self.root = root
        self.root.title("ESP32 Communicator")
        
        self.serial_port = None
        self.create_widgets()

    def create_widgets(self):
        # Puerto Serie
        self.port_label = ttk.Label(self.root, text="Seleccionar Puerto:")
        self.port_label.pack(pady=5)
        
        self.port_combobox = ttk.Combobox(self.root)
        self.port_combobox['values'] = self.get_serial_ports()
        self.port_combobox.pack(pady=5)
        
        self.connect_button = ttk.Button(self.root, text="Conectar", command=self.connect)
        self.connect_button.pack(pady=5)

        # Enviar Número
        self.num_entry_label = ttk.Label(self.root, text="Enviar Número:")
        self.num_entry_label.pack(pady=5)
        
        self.num_entry = ttk.Entry(self.root)
        self.num_entry.pack(pady=5)

        self.send_button = ttk.Button(self.root, text="Enviar", command=self.send_number)
        self.send_button.pack(pady=5)

        # Resultado
        self.result_label = ttk.Label(self.root, text="Resultado:")
        self.result_label.pack(pady=5)
        
        self.result_value = ttk.Label(self.root, text="")
        self.result_value.pack(pady=5)
    
    def get_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect(self):
        selected_port = self.port_combobox.get()
        if selected_port:
            self.serial_port = serial.Serial(selected_port, baudrate=115200, timeout=1)
            print(f"Conectado al puerto {selected_port}")

    def send_number(self):
        if self.serial_port and self.serial_port.is_open:
            number = self.num_entry.get()
            if number.isdigit():
                self.serial_port.write(f"{number}\n".encode('utf-8'))
                response = self.serial_port.readline().decode('utf-8').strip()
                self.result_value.config(text=response)
            else:
                messagebox.showerror("Error", "Por favor, introduce un número válido.")
        else:
            messagebox.showerror("Error", "Por favor, conecta al puerto primero.")


root = tk.Tk()
app = ESP32(root)
root.mainloop()
