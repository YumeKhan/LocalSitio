import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from dados_locacoes import locacoes  # Importando os dados de locações

# Função para atualizar as cidades com base no estado selecionado
def update_cidades(event):
    estado = combo_estado.get()
    if estado == "Minas Gerais":
        combo_cidade['values'] = [
            "Belo Horizonte", "Nova Lima", "Ouro Preto", "Tiradentes", "Lavras",
            "Pouso Alegre", "Divinópolis", "Sete Lagoas", "João Monlevade",
            "São João del-Rei", "Varginha", "Itajubá", "Formiga", "Santa Rita do Sapucaí",
            "Muriae", "Maria da Fé"
        ]
        combo_cidade.current(0)
    elif estado == "São Paulo":
        combo_cidade['values'] = [
            "São Paulo", "Campinas", "Santos", "Sorocaba", "São Bernardo do Campo",
            "Ribeirão Preto", "São José dos Campos", "Bauru", "Guarulhos", "Osasco",
            "Jundiaí", "Itapevi", "Piracicaba", "Indaiatuba"
        ]
        combo_cidade.current(0)
    elif estado == "Rio de Janeiro":
        combo_cidade['values'] = [
            "Rio de Janeiro", "Niterói", "Cabo Frio", "Petrópolis", "Angra dos Reis",
            "Volta Redonda", "Macaé", "Duque de Caxias", "Itaperuna", "Nova Friburgo"
        ]
        combo_cidade.current(0)
    else:
        combo_cidade['values'] = []
        combo_cidade.set("")

# Função para buscar as locações nos dados importados
def search_properties():
    estado = combo_estado.get().strip()
    cidade = combo_cidade.get().strip()
    tipo = combo_tipo.get().strip()

    detalhes = []
    if var_piscina.get():
        detalhes.append("piscina")
    if var_quadra_volei.get():
        detalhes.append("quadra de vôlei")
    if var_futebol.get():
        detalhes.append("campo de futebol")
    if var_churrasqueira.get():
        detalhes.append("churrasqueira")
    if var_area_lazer.get():
        detalhes.append("área de lazer")

    if not cidade or not tipo or not estado:
        messagebox.showwarning("Aviso", "Por favor, informe a cidade, o tipo de imóvel e o estado.")
        return

    filtered_results = filter_properties(estado, cidade, tipo, detalhes)
    display_results(filtered_results)

# Função para filtrar as propriedades de acordo com os critérios fornecidos
def filter_properties(estado, cidade, tipo, detalhes):
    results = []
    for locacao in locacoes:
        # Filtra pelo estado, cidade e tipo de imóvel
        if (
            estado.lower() == locacao["estado"].lower() and 
            cidade.lower() == locacao["cidade"].lower() and 
            tipo.lower() == locacao["tipo"].lower()
        ):
            # Verifica se a locação possui qualquer uma das características selecionadas
            if not detalhes or any(caracteristica.lower() in locacao["caracteristicas"] for caracteristica in detalhes):
                results.append(locacao)
    return results

# Função para exibir os resultados encontrados
def display_results(resultados):
    # Limpa os resultados anteriores
    for widget in frame_resultados.winfo_children():
        widget.destroy()

    if not resultados:
        messagebox.showinfo("Resultados", "Nenhuma propriedade encontrada com os critérios informados.")
        return

    for idx, item in enumerate(resultados, start=1):
        resultado_texto = f"{idx}. {item.get('tipo', 'Tipo não especificado')} em {item.get('cidade', 'Cidade não especificada')}\n"
        detalhes_texto = f"   Detalhes: {', '.join(item.get('caracteristicas', []))}\n"
        valor_texto = f"   Valor: R${item.get('valor', 'N/D'):.2f}\n"
        dias_texto = f"   Dias: {item.get('dias', 'N/D')}\n"

        resultado_label = tk.Label(frame_resultados, text=resultado_texto + detalhes_texto + valor_texto + dias_texto, bg="#e0f7fa", fg="#00796b", justify="left")
        resultado_label.pack(anchor="w")  # Alinha o texto à esquerda

# Layout principal da aplicação
root = tk.Tk()
root.title("LocaSitio - Pesquisa de Locação")
root.geometry("800x600")
root.configure(bg="#e0f7fa")

# Título
tk.Label(root, text="LocaSitio - Pesquisa de Locação de Imóveis", font=("Arial", 16, "bold"), bg="#e0f7fa", fg="#00796b").pack(pady=10)

# Área de busca
frame_search = tk.Frame(root, bg="#e0f7fa")
frame_search.pack(pady=20)

# Estado: ComboBox com seleções
tk.Label(frame_search, text="Estado:", bg="#e0f7fa", fg="#00796b", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
combo_estado = ttk.Combobox(frame_search, values=["Minas Gerais", "São Paulo", "Rio de Janeiro"], width=30)
combo_estado.grid(row=0, column=1, padx=10, pady=5)
combo_estado.bind("<<ComboboxSelected>>", update_cidades)

# Cidade: ComboBox com seleções, atualizada conforme o estado
tk.Label(frame_search, text="Cidade:", bg="#e0f7fa", fg="#00796b", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
combo_cidade = ttk.Combobox(frame_search, values=[], width=30)
combo_cidade.grid(row=1, column=1, padx=10, pady=5)

# Tipo de Imóvel: ComboBox com seleções
tk.Label(frame_search, text="Tipo de Imóvel:", bg="#e0f7fa", fg="#00796b", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
combo_tipo = ttk.Combobox(frame_search, values=["Casa", "Sítio", "Clube", "Fazenda"], width=30)
combo_tipo.grid(row=2, column=1, padx=10, pady=5)

# Características: Checkboxes para seleções separadas
tk.Label(frame_search, text="Características:", bg="#e0f7fa", fg="#00796b", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="e")

# Criação de variáveis para os Checkbuttons
var_piscina = tk.BooleanVar()
var_quadra_volei = tk.BooleanVar()
var_futebol = tk.BooleanVar()
var_churrasqueira = tk.BooleanVar()
var_area_lazer = tk.BooleanVar()

# Checkbuttons para selecionar características
tk.Checkbutton(frame_search, text="Piscina", variable=var_piscina).grid(row=3, column=1, padx=10, pady=5, sticky="w")
tk.Checkbutton(frame_search, text="Quadra de Vôlei", variable=var_quadra_volei).grid(row=4, column=1, padx=10, pady=5, sticky="w")
tk.Checkbutton(frame_search, text="Campo de Futebol", variable=var_futebol).grid(row=5, column=1, padx=10, pady=5, sticky="w")
tk.Checkbutton(frame_search, text="Churrasqueira", variable=var_churrasqueira).grid(row=6, column=1, padx=10, pady=5, sticky="w")
tk.Checkbutton(frame_search, text="Área de Lazer", variable=var_area_lazer).grid(row=7, column=1, padx=10, pady=5, sticky="w")

# Botão de busca
tk.Button(frame_search, text="Buscar", command=search_properties, bg="#00796b", fg="white", font=("Arial", 12)).grid(row=8, column=0, columnspan=2, pady=10)

# Área de resultados
tk.Label(root, text="Resultados:", font=("Arial", 14, "bold"), bg="#e0f7fa", fg="#00796b").pack(pady=5)
frame_resultados = tk.Frame(root, bg="#e0f7fa")
frame_resultados.pack(pady=10)

# Área de resultados com rolagem
resultados_frame = tk.Frame(root, bg="#e0f7fa")
resultados_frame.pack(pady=10, fill=tk.BOTH, expand=True)


# Criando um Canvas para a área de resultados
canvas = tk.Canvas(resultados_frame, bg="white")
scroll_y = tk.Scrollbar(resultados_frame, orient="vertical", command=canvas.yview)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

# Criar um frame interno para os resultados
frame_resultados = tk.Frame(canvas, bg="white")

# Configurar o canvas para que o frame_resultados seja uma parte dele
canvas.create_window((0, 0), window=frame_resultados, anchor="nw")

# Configurar a rolagem
canvas.configure(yscrollcommand=scroll_y.set)

# Função para atualizar a região do canvas quando o conteúdo mudar
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

# Conectar a função de configuração ao frame_resultados
frame_resultados.bind("<Configure>", on_frame_configure)

# Empacotar o canvas
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Inicializa o aplicativo
root.mainloop()