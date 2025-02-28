example_trace = "../test_examples/trace_shannon_48"

def display_options(prompt_text, options_list):
    print(prompt_text)
    options = [f'({i+1}) {option}' for i, option in enumerate(options_list)]
    options_numbers = (i+1 for i in range(len(options)))
    for formatted_option in options:
        print(formatted_option)
    return options_numbers
    
def read_file(file_path):
    retry = True
    while retry:
        # file_path = input(f"Digite o caminho do arquivo {file_type} ou arraste para cá: ")
        try:
            with open(file_path, "r") as file:
                lines = [line.split() for line in file.readlines()]
                return lines
        except FileNotFoundError:
            input(f"Erro na leitura. Verifique o diretório.")
        
def get_number(prompt_text):
    while True:
        number = input(prompt_text) 
        try:
            return float(number)
        except ValueError:
            print(f"Erro: Digite um número.")
        
