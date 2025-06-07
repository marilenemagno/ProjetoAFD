# ProjetoAFD

Implementação de Autômatos Finitos Determinísticos (AFDs) e Transdutores Finitos usando Python.

1a - Implemente AFDs, em uma linguagem de programação à sua escolha, que aceitem
todas as cadeias em {0,1}* que representam cada 1 seguido imediatamente de dois 0.

import tkinter as tk
from tkinter import ttk, messagebox

class AFDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AFD - Cada 1 seguido por dois 0s")
        self.root.geometry("600x500")
        
        # Configuração do AFD
        self.afd = {
            'estados': {'q0', 'q1', 'q2', 'qE'},
            'alfabeto': {'0', '1'},
            'transicoes': {
                'q0': {'0': 'q0', '1': 'q1'},
                'q1': {'0': 'q2', '1': 'qE'},
                'q2': {'0': 'q0', '1': 'qE'},
                'qE': {'0': 'qE', '1': 'qE'}
            },
            'estado_inicial': 'q0',
            'estados_finais': {'q0'}
        }
        
        self.estado_atual = self.afd['estado_inicial']
        self.criar_interface()
    
    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text="AFD para {0,1}* com cada 1 seguido por dois 0s", 
                 font=('Helvetica', 12, 'bold')).pack(pady=10)
        
        # Entrada de texto
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Digite uma cadeia:").pack(side=tk.LEFT)
        self.entrada = ttk.Entry(input_frame, width=30)
        self.entrada.pack(side=tk.LEFT, padx=5)
        self.entrada.bind('<KeyRelease>', self.validar_cadeia)
        
        # Botão de verificação
        ttk.Button(main_frame, text="Verificar", command=self.verificar_cadeia).pack(pady=5)
        
        # Área de resultado
        self.resultado = ttk.Label(main_frame, text="Estado atual: q0", font=('Helvetica', 10))
        self.resultado.pack(pady=10)
        
        # Canvas para desenhar o AFD
        self.canvas = tk.Canvas(main_frame, width=550, height=300, bg='white')
        self.canvas.pack(pady=10)
        self.desenhar_afd()
        
        # Status
        self.status = ttk.Label(main_frame, text="Pronto para validar cadeias", foreground="blue")
        self.status.pack()
    
    def desenhar_afd(self):
        self.canvas.delete("all")
        
        # Posições dos estados
        estados_pos = {
            'q0': (100, 150),
            'q1': (300, 50),
            'q2': (300, 250),
            'qE': (500, 150)
        }
        
        # Desenhar transições
        # q0 -> q0 (loop)
        self.canvas.create_oval(70, 120, 130, 180, outline='black', width=2)
        self.canvas.create_text(100, 100, text="0")
        
        # q0 -> q1
        self.canvas.create_line(130, 140, 270, 70, arrow=tk.LAST, width=2)
        self.canvas.create_text(200, 100, text="1")
        
        # q1 -> q2
        self.canvas.create_line(300, 80, 300, 220, arrow=tk.LAST, width=2)
        self.canvas.create_text(320, 150, text="0")
        
        # q2 -> q0
        self.canvas.create_line(270, 250, 130, 160, arrow=tk.LAST, width=2)
        self.canvas.create_text(200, 220, text="0")
        
        # qE loop (não visível inicialmente)
        self.canvas.create_oval(470, 120, 530, 180, outline='black', width=2, dash=(4,2))
        self.canvas.create_text(500, 100, text="0,1", state=tk.HIDDEN)
        
        # Desenhar estados
        for estado, pos in estados_pos.items():
            x, y = pos
            cor = 'red' if estado == 'qE' else 'white'
            if estado in self.afd['estados_finais']:
                self.canvas.create_oval(x-30, y-30, x+30, y+30, outline='black', width=2, fill=cor)
                self.canvas.create_oval(x-20, y-20, x+20, y+20, outline='black', width=2, fill=cor)
            else:
                self.canvas.create_oval(x-30, y-30, x+30, y+30, outline='black', width=2, fill=cor)
            
            self.canvas.create_text(x, y, text=estado, font=('Helvetica', 10, 'bold'))
        
        # Destacar estado atual
        self.atualizar_estado_desenho()
    
    def atualizar_estado_desenho(self):
        # Resetar todas as cores
        for estado in self.afd['estados']:
            self.canvas.itemconfig(f"estado_{estado}", fill='white')
        
        # Colorir estado atual
        cor = '#ffcc00'  # amarelo para estado atual
        self.canvas.itemconfig(f"estado_{self.estado_atual}", fill=cor)
    
    def validar_cadeia(self, event=None):
        cadeia = self.entrada.get()
        
        # Filtrar caracteres inválidos
        cadeia_filtrada = ''.join(c for c in cadeia if c in self.afd['alfabeto'])
        if cadeia_filtrada != cadeia:
            self.entrada.delete(0, tk.END)
            self.entrada.insert(0, cadeia_filtrada)
        
        # Processar cadeia
        self.estado_atual = self.afd['estado_inicial']
        for simbolo in cadeia_filtrada:
            self.estado_atual = self.afd['transicoes'][self.estado_atual].get(simbolo, 'qE')
        
        # Atualizar interface
        self.resultado.config(text=f"Estado atual: {self.estado_atual}")
        self.atualizar_estado_desenho()
        
        # Verificar se é válido
        valido = self.estado_atual in self.afd['estados_finais']
        cor = 'green' if valido else 'red'
        self.resultado.config(foreground=cor)
        
        # Mostrar status
        if not cadeia_filtrada:
            self.status.config(text="Digite uma cadeia com 0s e 1s", foreground="blue")
        else:
            status_text = "Cadeia válida" if valido else "Cadeia inválida"
            self.status.config(text=status_text, foreground=cor)
    
    def verificar_cadeia(self):
        cadeia = self.entrada.get()
        self.validar_cadeia()
        
        valido = self.estado_atual in self.afd['estados_finais']
        cadeia_display = cadeia if cadeia else "ε (vazia)"
        
        messagebox.showinfo(
            "Resultado",
            f"Cadeia: {cadeia_display}\n"
            f"Estado final: {self.estado_atual}\n"
            f"Resultado: {'ACEITA' if valido else 'REJEITADA'}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = AFDApp(root)
    root.mainloop()

