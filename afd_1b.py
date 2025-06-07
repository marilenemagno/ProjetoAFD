import tkinter as tk
from tkinter import ttk, messagebox
from time import sleep

class AFDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AFD - Último 'b' e Número Par de 'a's")
        self.root.geometry("800x700")
        
        # Configuração do AFD
        self.afd = {
            'estados': {'q0', 'q1', 'q2', 'q3'},
            'alfabeto': {'a', 'b'},
            'transicoes': {
                'q0': {'a': 'q2', 'b': 'q1'},
                'q1': {'a': 'q2', 'b': 'q1'},
                'q2': {'a': 'q0', 'b': 'q3'},
                'q3': {'a': 'q0', 'b': 'q3'}
            },
            'estado_inicial': 'q0',
            'estados_finais': {'q1'}
        }
        
        self.estado_atual = self.afd['estado_inicial']
        self.historico = []
        self.criar_interface()
    
    def criar_interface(self):
        # Configuração do estilo
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(title_frame, 
                 text="AFD para Linguagem {a,b}*", 
                 font=('Helvetica', 14, 'bold')).pack(side=tk.LEFT)
        
        ttk.Label(title_frame, 
                 text="Último símbolo 'b' e número par de 'a's", 
                 font=('Helvetica', 12)).pack(side=tk.LEFT, padx=10)
        
        # Área de controle
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        # Entrada de texto
        input_frame = ttk.Frame(control_frame)
        input_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        ttk.Label(input_frame, text="Digite uma cadeia:").pack(anchor=tk.W)
        self.entrada = ttk.Entry(input_frame, font=('Courier', 12))
        self.entrada.pack(fill=tk.X, pady=5)
        self.entrada.bind('<KeyRelease>', self.validar_cadeia)
        
        # Botões
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(side=tk.RIGHT, padx=10)
        
        ttk.Button(btn_frame, text="Verificar", command=self.verificar_cadeia).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Passo a Passo", command=self.passo_a_passo).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar).pack(fill=tk.X, pady=2)
        
        # Exemplos rápidos
        example_frame = ttk.Frame(main_frame)
        example_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(example_frame, text="Exemplos:").pack(anchor=tk.W)
        
        examples = ["b", "aab", "abab", "a", "ba", "abb"]
        for ex in examples:
            btn = ttk.Button(example_frame, text=ex, width=4,
                            command=lambda e=ex: self.inserir_exemplo(e))
            btn.pack(side=tk.LEFT, padx=2)
        
        # Área de resultado
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill=tk.X, pady=10)
        
        self.resultado = ttk.Label(result_frame, text="Estado atual: q0", 
                                 font=('Helvetica', 11, 'bold'))
        self.resultado.pack(anchor=tk.W)
        
        self.status = ttk.Label(result_frame, text="Pronto para validar cadeias", 
                              foreground="blue")
        self.status.pack(anchor=tk.W)
        
        # Canvas para o AFD
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, width=750, height=350, 
                               bg='white', highlightthickness=0)
        self.canvas.pack()
        
        # Histórico
        hist_frame = ttk.Frame(main_frame)
        hist_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(hist_frame, text="Histórico:").pack(anchor=tk.W)
        self.hist_text = tk.Text(hist_frame, height=4, font=('Courier', 10))
        self.hist_text.pack(fill=tk.X)
        
        self.desenhar_afd()
    
    def inserir_exemplo(self, exemplo):
        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, exemplo)
        self.validar_cadeia()
    
    def desenhar_afd(self):
        self.canvas.delete("all")
        
        # Posições dos estados
        estados_pos = {
            'q0': (150, 150),
            'q1': (500, 150),
            'q2': (150, 280),
            'q3': (500, 280)
        }
        
        # Desenhar transições
        # q0 -> q2 (a)
        self.canvas.create_line(150, 180, 150, 250, arrow=tk.LAST, width=2, tags="transicao")
        self.canvas.create_text(130, 215, text="a", tags="transicao")
        
        # q0 -> q1 (b)
        self.canvas.create_line(180, 150, 470, 150, arrow=tk.LAST, width=2, tags="transicao")
        self.canvas.create_text(325, 130, text="b", tags="transicao")
        
        # q1 -> q2 (a)
        self.canvas.create_line(470, 180, 180, 250, arrow=tk.LAST, width=2, tags="transicao")
        self.canvas.create_text(325, 215, text="a", tags="transicao")
        
        # q1 -> q1 (b) loop
        self.canvas.create_oval(500, 120, 540, 160, outline='black', width=2, tags="transicao")
        self.canvas.create_text(540, 140, text="b", tags="transicao")
        
        # q2 -> q0 (a)
        self.canvas.create_line(150, 250, 150, 180, arrow=tk.LAST, width=2, tags="transicao")
        self.canvas.create_text(170, 215, text="a", tags="transicao")
        
        # q2 -> q3 (b)
        self.canvas.create_line(180, 280, 470, 280, arrow=tk.LAST, width=2, tags="transicao")
        self.canvas.create_text(325, 300, text="b", tags="transicao")
        
        # q3 -> q0 (a)
        self.canvas.create_line(470, 280, 180, 150, arrow=tk.LAST, width=2, tags="transicao")
        self.canvas.create_text(325, 215, text="a", tags="transicao")
        
        # q3 -> q3 (b) loop
        self.canvas.create_oval(500, 250, 540, 290, outline='black', width=2, tags="transicao")
        self.canvas.create_text(540, 270, text="b", tags="transicao")
        
        # Desenhar estados
        for estado, pos in estados_pos.items():
            x, y = pos
            color = 'white'
            outline = 'black'
            width = 2
            
            if estado == self.estado_atual:
                color = '#fffacd'  # amarelo claro para estado atual
                outline = '#ffa500'
                width = 3
            
            if estado in self.afd['estados_finais']:
                # Estado final (círculo duplo)
                self.canvas.create_oval(x-30, y-30, x+30, y+30, 
                                      outline=outline, width=width, 
                                      fill=color, tags=f"estado_{estado}")
                self.canvas.create_oval(x-20, y-20, x+20, y+20, 
                                      outline=outline, width=width, 
                                      fill=color, tags=f"estado_{estado}")
            else:
                self.canvas.create_oval(x-30, y-30, x+30, y+30, 
                                      outline=outline, width=width, 
                                      fill=color, tags=f"estado_{estado}")
            
            self.canvas.create_text(x, y, text=estado, 
                                 font=('Helvetica', 10, 'bold'), 
                                 tags=f"estado_{estado}")
        
        # Estado inicial (seta)
        self.canvas.create_line(80, 150, 120, 150, arrow=tk.LAST, width=2, tags="inicio")
        
        # Legenda
        self.canvas.create_text(650, 50, text="Legenda:", anchor=tk.NW, font=('Helvetica', 9, 'bold'))
        self.canvas.create_text(650, 70, text="Verde: Válido", anchor=tk.NW, fill="green")
        self.canvas.create_text(650, 90, text="Vermelho: Inválido", anchor=tk.NW, fill="red")
        self.canvas.create_text(650, 110, text="Amarelo: Estado Atual", anchor=tk.NW, fill="#ffa500")
    
    def atualizar_interface(self):
        self.desenhar_afd()
        
        # Atualizar histórico
        self.hist_text.delete(1.0, tk.END)
        if self.historico:
            for passo in self.historico:
                self.hist_text.insert(tk.END, f"{passo}\n")
    
    def validar_cadeia(self, event=None):
        cadeia = self.entrada.get().lower()
        
        # Filtrar caracteres inválidos
        cadeia_filtrada = ''.join(c for c in cadeia if c in self.afd['alfabeto'])
        if cadeia_filtrada != cadeia:
            self.entrada.delete(0, tk.END)
            self.entrada.insert(0, cadeia_filtrada)
        
        # Processar cadeia
        self.estado_atual = self.afd['estado_inicial']
        self.historico = [f"Início: q0"]
        
        for i, simbolo in enumerate(cadeia_filtrada, 1):
            estado_anterior = self.estado_atual
            self.estado_atual = self.afd['transicoes'][self.estado_atual].get(simbolo, 'qE')
            self.historico.append(f"Passo {i}: '{simbolo}' | {estado_anterior} → {self.estado_atual}")
        
        # Atualizar interface
        self.atualizar_interface()
        
        # Verificar se é válido
        valido = self.estado_atual in self.afd['estados_finais']
        cor = 'green' if valido else 'red'
        self.resultado.config(text=f"Estado atual: {self.estado_atual}", foreground=cor)
        
        # Mostrar status
        if not cadeia_filtrada:
            self.status.config(text="Digite uma cadeia com 'a's e 'b's", foreground="blue")
        else:
            status_text = "Cadeia VÁLIDA (último 'b' e número par de 'a's)" if valido else "Cadeia INVÁLIDA"
            self.status.config(text=status_text, foreground=cor)
    
    def passo_a_passo(self):
        cadeia = self.entrada.get().lower()
        cadeia_filtrada = ''.join(c for c in cadeia if c in self.afd['alfabeto'])
        
        if not cadeia_filtrada:
            messagebox.showinfo("Aviso", "Digite uma cadeia válida primeiro")
            return
        
        # Resetar para estado inicial
        self.estado_atual = self.afd['estado_inicial']
        self.historico = [f"Início: q0"]
        self.atualizar_interface()
        self.root.update()
        sleep(1)
        
        for i, simbolo in enumerate(cadeia_filtrada, 1):
            estado_anterior = self.estado_atual
            self.estado_atual = self.afd['transicoes'][self.estado_atual].get(simbolo, 'qE')
            self.historico.append(f"Passo {i}: '{simbolo}' | {estado_anterior} → {self.estado_atual}")
            
            self.atualizar_interface()
            self.root.update()
            sleep(1)
        
        valido = self.estado_atual in self.afd['estados_finais']
        cor = 'green' if valido else 'red'
        self.resultado.config(text=f"Estado final: {self.estado_atual}", foreground=cor)
        
        messagebox.showinfo("Resultado", 
                          f"Cadeia: {cadeia_filtrada if cadeia_filtrada else 'ε (vazia)'}\n"
                          f"Estado final: {self.estado_atual}\n"
                          f"Resultado: {'ACEITA' if valido else 'REJEITADA'}")
    
    def verificar_cadeia(self):
        self.validar_cadeia()
        cadeia = self.entrada.get().lower()
        cadeia_filtrada = ''.join(c for c in cadeia if c in self.afd['alfabeto'])
        
        valido = self.estado_atual in self.afd['estados_finais']
        cadeia_display = cadeia_filtrada if cadeia_filtrada else "ε (vazia)"
        
        messagebox.showinfo("Resultado",
                          f"Cadeia: {cadeia_display}\n"
                          f"Estado final: {self.estado_atual}\n"
                          f"Resultado: {'ACEITA' if valido else 'REJEITADA'}\n\n"
                          f"Condições:\n"
                          f"1. Último símbolo é 'b': {'Sim' if cadeia_filtrada and cadeia_filtrada[-1] == 'b' else 'Não'}\n"
                          f"2. Número de 'a's é par: {'Sim' if cadeia_filtrada.count('a') % 2 == 0 else 'Não'}")
    
    def limpar(self):
        self.entrada.delete(0, tk.END)
        self.estado_atual = self.afd['estado_inicial']
        self.historico = []
        self.resultado.config(text="Estado atual: q0", foreground="black")
        self.status.config(text="Pronto para validar cadeias", foreground="blue")
        self.hist_text.delete(1.0, tk.END)
        self.atualizar_interface()


if __name__ == "__main__":
    root = tk.Tk()
    app = AFDApp(root)
    root.mainloop()