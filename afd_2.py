import tkinter as tk
from tkinter import ttk, messagebox
import re

class DetectorComputador:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector de Palavras - Computador")
        self.root.geometry("800x600")
        
        # Texto de exemplo
        self.texto_exemplo = """O computador é uma máquina capaz de variados tipos de tratamento automático de
informações ou processamento de dados. Entende-se por computador um sistema físico que realiza
algum tipo de computação. Assumiu-se que os computadores pessoais e laptops são ícones da era da
informação. O primeiro computador eletromecânico foi construído por Konrad Zuse (1910–1995).
Atualmente, um microcomputador é também chamado computador pessoal ou ainda computador
doméstico."""
        
        self.criar_interface()
    
    def criar_interface(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, 
                 text="Detector de Ocorrências da Palavra 'computador'", 
                 font=('Helvetica', 14, 'bold')).pack(anchor=tk.W)
        
        ttk.Label(header_frame, 
                 text="[1.0 pt] Implemente um autômato finito que reconheça todas as ocorrências da palavra 'computador' no texto", 
                 font=('Helvetica', 10)).pack(anchor=tk.W)
        
        # Área de texto
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(text_frame, text="Digite ou cole seu texto abaixo:", font=('Helvetica', 10)).pack(anchor=tk.W)
        
        self.text_input = tk.Text(text_frame, wrap=tk.WORD, font=('Arial', 11), height=15)
        self.text_input.pack(fill=tk.BOTH, expand=True, pady=5)
        self.text_input.insert(tk.END, self.texto_exemplo)
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Verificar Ocorrências", command=self.verificar_ocorrencias).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_texto).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Texto de Exemplo", command=self.inserir_exemplo).pack(side=tk.LEFT, padx=5)
        
        # Resultados
        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(result_frame, text="Resultados:", font=('Helvetica', 11, 'bold')).pack(anchor=tk.W)
        
        self.contador_label = ttk.Label(result_frame, text="Nenhuma ocorrência encontrada ainda", font=('Helvetica', 10))
        self.contador_label.pack(anchor=tk.W, pady=(5, 0))
        
        self.resultados_text = tk.Text(result_frame, wrap=tk.WORD, font=('Arial', 10), height=6, state=tk.DISABLED)
        self.resultados_text.pack(fill=tk.BOTH, expand=True)
        
        # Configurar barra de rolagem
        scrollbar = ttk.Scrollbar(self.resultados_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.resultados_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.resultados_text.yview)
        
        # Vincular evento de digitação
        self.text_input.bind('<KeyRelease>', self.atualizar_em_tempo_real)
    
    def verificar_ocorrencias(self):
        texto = self.text_input.get("1.0", tk.END)
        ocorrencias = self.encontrar_ocorrencias(texto)
        
        if not ocorrencias:
            messagebox.showinfo("Resultado", "Nenhuma ocorrência da palavra 'computador' foi encontrada.")
        else:
            messagebox.showinfo("Resultado", 
                              f"Foram encontradas {len(ocorrencias)} ocorrências da palavra 'computador'.\n"
                              f"Posições: {', '.join(str(oc['posicao']) for oc in ocorrencias)}")
    
    def encontrar_ocorrencias(self, texto):
        palavra = "computador"
        regex = re.compile(r'\b' + re.escape(palavra) + r'\b', re.IGNORECASE)
        ocorrencias = []
        
        # Encontrar todas as ocorrências
        for match in regex.finditer(texto):
            ocorrencias.append({
                'posicao': match.start(),
                'texto': match.group()
            })
        
        return ocorrencias
    
    def atualizar_em_tempo_real(self, event=None):
        texto = self.text_input.get("1.0", tk.END)
        ocorrencias = self.encontrar_ocorrencias(texto)
        
        # Atualizar contador
        if not ocorrencias:
            self.contador_label.config(text="Nenhuma ocorrência encontrada ainda")
        else:
            plural = "s" if len(ocorrencias) > 1 else ""
            self.contador_label.config(text=f"A palavra 'computador' aparece {len(ocorrencias)} vez{plural} no texto")
        
        # Atualizar área de resultados
        self.resultados_text.config(state=tk.NORMAL)
        self.resultados_text.delete("1.0", tk.END)
        
        if ocorrencias:
            for i, ocorrencia in enumerate(ocorrencias, 1):
                self.resultados_text.insert(tk.END, 
                                         f"{i}ª ocorrência - Posição: {ocorrencia['posicao']}\n")
        
        self.resultados_text.config(state=tk.DISABLED)
        
        # Destacar ocorrências no texto
        self.destacar_palavras()
    
    def destacar_palavras(self):
        texto = self.text_input.get("1.0", tk.END)
        palavra = "computador"
        
        # Remover destaque anterior
        self.text_input.tag_remove("destaque", "1.0", tk.END)
        
        # Aplicar novo destaque
        start = "1.0"
        while True:
            start = self.text_input.search(palavra, start, stopindex=tk.END, nocase=1)
            if not start:
                break
            
            end = f"{start}+{len(palavra)}c"
            self.text_input.tag_add("destaque", start, end)
            start = end
        
        # Configurar estilo do destaque
        self.text_input.tag_config("destaque", background="yellow", foreground="black")
    
    def limpar_texto(self):
        self.text_input.delete("1.0", tk.END)
        self.contador_label.config(text="Nenhuma ocorrência encontrada ainda")
        self.resultados_text.config(state=tk.NORMAL)
        self.resultados_text.delete("1.0", tk.END)
        self.resultados_text.config(state=tk.DISABLED)
        self.text_input.tag_remove("destaque", "1.0", tk.END)
    
    def inserir_exemplo(self):
        self.limpar_texto()
        self.text_input.insert(tk.END, self.texto_exemplo)
        self.atualizar_em_tempo_real()


if __name__ == "__main__":
    root = tk.Tk()
    app = DetectorComputador(root)
    root.mainloop()