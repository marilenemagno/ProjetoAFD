import tkinter as tk
from tkinter import ttk, messagebox

class MealyMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Máquina de Refrigerantes - Transdutor de Mealy")
        self.root.geometry("800x600")
        
        # Configuração da Máquina de Mealy
        self.machine = {
            'states': {
                'q0': {'value': 0, 'name': "R$0,00"},
                'q1': {'value': 25, 'name': "R$0,25"},
                'q2': {'value': 50, 'name': "R$0,50"},
                'q3': {'value': 75, 'name': "R$0,75"}
            },
            'transitions': {
                'q0': {
                    25: {'next': 'q1', 'output': 0},
                    50: {'next': 'q2', 'output': 0},
                    100: {'next': 'q0', 'output': 1}
                },
                'q1': {
                    25: {'next': 'q2', 'output': 0},
                    50: {'next': 'q3', 'output': 0},
                    100: {'next': 'q0', 'output': 1}
                },
                'q2': {
                    25: {'next': 'q3', 'output': 0},
                    50: {'next': 'q0', 'output': 1},
                    100: {'next': 'q0', 'output': 1}
                },
                'q3': {
                    25: {'next': 'q0', 'output': 1},
                    50: {'next': 'q0', 'output': 1},
                    100: {'next': 'q0', 'output': 1}
                }
            },
            'current_state': 'q0',
            'total': 0,
            'history': []
        }
        
        self.criar_interface()
        self.desenhar_diagrama()
    
    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(title_frame, 
                 text="Transdutor Finito de Mealy - Máquina de Refrigerantes", 
                 font=('Helvetica', 14, 'bold')).pack(anchor=tk.W)
        
        ttk.Label(title_frame, 
                 text="Implementação de um transdutor que libera refrigerante quando R$1,00 ou mais é inserido", 
                 font=('Helvetica', 10)).pack(anchor=tk.W)
        
        # Diagrama de estados
        diagram_frame = ttk.Frame(main_frame)
        diagram_frame.pack(fill=tk.X, pady=10)
        
        self.canvas = tk.Canvas(diagram_frame, width=750, height=250, bg='white')
        self.canvas.pack()
        
        # Controles
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        # Entradas (moedas)
        input_frame = ttk.Frame(control_frame)
        input_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        ttk.Label(input_frame, text="Entrada (Moedas):", font=('Helvetica', 11)).pack(anchor=tk.W)
        
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="25¢", command=lambda: self.processar_entrada(25)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="50¢", command=lambda: self.processar_entrada(50)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="R$1", command=lambda: self.processar_entrada(100)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Reset", command=self.resetar_maquina).pack(side=tk.LEFT, padx=5)
        
        # Saída
        output_frame = ttk.Frame(control_frame)
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        ttk.Label(output_frame, text="Saída:", font=('Helvetica', 11)).pack(anchor=tk.W)
        
        self.output_signal = ttk.Label(output_frame, text="0", font=('Helvetica', 24, 'bold'), 
                                     width=3, anchor=tk.CENTER)
        self.output_signal.pack(pady=5)
        
        self.output_text = ttk.Label(output_frame, text="Nenhuma lata liberada", 
                                   font=('Helvetica', 10))
        self.output_text.pack()
        
        # Histórico
        hist_frame = ttk.Frame(main_frame)
        hist_frame.pack(fill=tk.BOTH, expand=True)
        
        # Histórico de entradas
        input_hist_frame = ttk.Frame(hist_frame)
        input_hist_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(input_hist_frame, text="Histórico de Entradas:", font=('Helvetica', 11)).pack(anchor=tk.W)
        
        self.input_history = tk.Text(input_hist_frame, height=6, state=tk.DISABLED, wrap=tk.WORD)
        self.input_history.pack(fill=tk.BOTH, expand=True)
        
        # Total inserido
        total_frame = ttk.Frame(hist_frame)
        total_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        
        ttk.Label(total_frame, text="Total Inserido:", font=('Helvetica', 11)).pack(anchor=tk.W)
        
        self.total_amount = ttk.Label(total_frame, text="R$ 0,00", font=('Helvetica', 24))
        self.total_amount.pack(pady=10)
    
    def desenhar_diagrama(self):
        self.canvas.delete("all")
        
        # Desenhar estados
        estados = {
            'q0': (100, 125),
            'q1': (250, 125),
            'q2': (400, 125),
            'q3': (550, 125)
        }
        
        for estado, pos in estados.items():
            x, y = pos
            fill_color = "#ffecb3" if estado == self.machine['current_state'] else "white"
            
            self.canvas.create_oval(x-30, y-30, x+30, y+30, outline="black", width=2, fill=fill_color, tags=f"state_{estado}")
            self.canvas.create_text(x, y, text=f"{estado}\n{self.machine['states'][estado]['name']}", 
                                  font=('Helvetica', 8), tags=f"label_{estado}")
        
        # Desenhar transições
        # q0 -> q1 (25¢/0)
        self.canvas.create_line(130, 125, 220, 125, arrow=tk.LAST, width=2)
        self.canvas.create_text(175, 100, text="25¢/0")
        
        # q1 -> q2 (25¢/0)
        self.canvas.create_line(280, 125, 370, 125, arrow=tk.LAST, width=2)
        self.canvas.create_text(325, 100, text="25¢/0")
        
        # q2 -> q3 (25¢/0)
        self.canvas.create_line(430, 125, 520, 125, arrow=tk.LAST, width=2)
        self.canvas.create_text(475, 100, text="25¢/0")
        
        # q3 -> q0 (25¢/1)
        self.canvas.create_line(550, 155, 550, 200, width=2)
        self.canvas.create_line(550, 200, 100, 200, width=2)
        self.canvas.create_line(100, 200, 100, 155, arrow=tk.LAST, width=2)
        self.canvas.create_text(325, 210, text="25¢/1")
        
        # q0 -> q2 (50¢/0)
        self.canvas.create_line(100, 95, 175, 60, width=2)
        self.canvas.create_line(175, 60, 325, 60, width=2)
        self.canvas.create_line(325, 60, 400, 95, arrow=tk.LAST, width=2)
        self.canvas.create_text(250, 50, text="50¢/0")
        
        # q1 -> q3 (50¢/0)
        self.canvas.create_line(250, 95, 325, 60, width=2)
        self.canvas.create_line(325, 60, 475, 60, width=2)
        self.canvas.create_line(475, 60, 550, 95, arrow=tk.LAST, width=2)
        self.canvas.create_text(400, 50, text="50¢/0")
        
        # q2 -> q0 (50¢/1)
        self.canvas.create_line(400, 155, 400, 180, width=2)
        self.canvas.create_line(400, 180, 250, 180, width=2)
        self.canvas.create_line(250, 180, 100, 155, arrow=tk.LAST, width=2)
        self.canvas.create_text(250, 190, text="50¢/1")
        
        # q3 -> q0 (50¢/1)
        self.canvas.create_line(550, 155, 550, 180, width=2)
        self.canvas.create_line(550, 180, 400, 180, width=2)
        self.canvas.create_line(400, 180, 250, 155, arrow=tk.LAST, width=2)
        self.canvas.create_text(475, 190, text="50¢/1")
        
        # q0 -> q0 (R$1/1)
        self.canvas.create_oval(70, 95, 130, 155, width=2)
        self.canvas.create_text(70, 125, text="R$1/1", anchor=tk.E)
        
        # q1 -> q0 (R$1/1)
        self.canvas.create_line(250, 95, 220, 60, width=2)
        self.canvas.create_line(220, 60, 130, 60, width=2)
        self.canvas.create_line(130, 60, 100, 95, arrow=tk.LAST, width=2)
        self.canvas.create_text(175, 50, text="R$1/1")
        
        # q2 -> q0 (R$1/1)
        self.canvas.create_line(400, 95, 370, 60, width=2)
        self.canvas.create_line(370, 60, 220, 60, width=2)
        self.canvas.create_line(220, 60, 100, 95, arrow=tk.LAST, width=2)
        self.canvas.create_text(325, 50, text="R$1/1")
        
        # q3 -> q0 (R$1/1)
        self.canvas.create_line(550, 95, 520, 60, width=2)
        self.canvas.create_line(520, 60, 370, 60, width=2)
        self.canvas.create_line(370, 60, 100, 95, arrow=tk.LAST, width=2)
        self.canvas.create_text(475, 50, text="R$1/1")
    
    def processar_entrada(self, moeda):
        transicoes = self.machine['transitions'][self.machine['current_state']]
        
        if moeda not in transicoes:
            messagebox.showerror("Erro", f"Moeda de {moeda}¢ não é válida neste estado")
            return
        
        transicao = transicoes[moeda]
        
        # Atualiza histórico
        self.machine['history'].append({
            'from': self.machine['current_state'],
            'input': moeda,
            'output': transicao['output'],
            'to': transicao['next']
        })
        
        # Atualiza total
        self.machine['total'] += moeda
        
        # Atualiza estado
        self.machine['current_state'] = transicao['next']
        
        # Atualiza interface
        self.atualizar_interface(transicao['output'])
    
    def atualizar_interface(self, saida):
        # Atualiza saída
        self.output_signal.config(text=str(saida))
        
        if saida == 1:
            self.output_signal.config(foreground="green")
            self.output_text.config(text="Lata liberada!", foreground="green")
        else:
            self.output_signal.config(foreground="red")
            self.output_text.config(text="Nenhuma lata liberada", foreground="black")
        
        # Atualiza histórico
        self.input_history.config(state=tk.NORMAL)
        self.input_history.delete(1.0, tk.END)
        
        for evento in self.machine['history']:
            self.input_history.insert(tk.END, 
                f"Estado {evento['from']} + {evento['input']}¢ → Saída {evento['output']} → Estado {evento['to']}\n")
        
        self.input_history.config(state=tk.DISABLED)
        
        # Atualiza total
        total = self.machine['total'] / 100
        self.total_amount.config(text=f"R$ {total:.2f}".replace('.', ','))
        
        # Redesenha diagrama com estado atual
        self.desenhar_diagrama()
    
    def resetar_maquina(self):
        self.machine['current_state'] = 'q0'
        self.machine['total'] = 0
        self.machine['history'] = []
        self.atualizar_interface(0)


if __name__ == "__main__":
    root = tk.Tk()
    app = MealyMachineApp(root)
    root.mainloop()