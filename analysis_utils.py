import os

def get_number(prompt_text):
    while True:
        number = input(prompt_text) 
        try:
            return float(number)
        except ValueError:
            print(f"Erro: Digite um número.")
            
def read_file(file_name):
    retry = True
    while retry:
        os.system('cls')
        file_path = input(f"Digite o caminho do arquivo {file_name} ou arraste para cá: ")
        try:
            with open(file_path, "r") as file:
                lines = [line.split() for line in file.readlines()]
                return lines
        except FileNotFoundError:
            input(f"Erro na leitura. Verifique o diretório.\n"
                  f"Pressione Enter para tentar novamente...")
                
def filter_wires():
    result = []
    wires = read_file("wires")
    if wires:
        key_word = "Pin"
        for line in wires:
            if len(line) > 0 and key_word in line:
                wire_color = line[2]
                wire_from = " ".join(line[4:7])
                wire_to =  line[9] if "Term" in line else " ".join(line[9:12])
                wire_type = f"Pin to {line[8]}"
                wire_wiring = wire_from + " <> " + wire_to
                wire_info = {
                    "Pin": wire_from,
                    "Wire_To": wire_to,
                    "Wire_Color": wire_color,
                    "Wiring": wire_wiring,
                    "Wire_Type": wire_type
                }
                result.append(wire_info)
    result.pop(0)
    return result

def filter_inserts():
    result = []
    inserts = read_file("inserts")
    key_words_list = ["Pin", "mil", "Transfer"] # Palavras chaves para serem buscadas em cada linha
    for line in inserts:
        node_info = {}
        if len(line) > 0:
            key_word = next((key_word for key_word in (key_words_list) if key_word in line), None)
            if key_word:
                node_coordinate = " ".join(line[0:3])
                node_probe_size = ""
                match key_word:
                    case "Pin":
                        node_name = line[-1] if line[-1] != key_word else "!undefined!"
                    case "mil":
                        word_oz_index = next((i for i, word in enumerate(line) if word == "oz"))
                        word_mil_index = next((i for i, word in enumerate(line) if word == "mil"))
                        node_name = line[word_oz_index + 1]
                        node_probe_size = line[word_mil_index - 1]
                    case "Transfer":
                        node_name = "TRANSFER"
                node_info = {
                    "Node_Name": node_name,
                    "Node_Coordinate": node_coordinate,
                    "Probe_Size": node_probe_size if node_probe_size else "!undefined!"
                }
                result.append(node_info)
    return result

def filter_pinslong():
    pinslong = read_file("pinslong")
    pinslong_filtered = [node[1].replace('"', "") for node in pinslong if len(node) > 0 and node[0]=="nodes"]
    return pinslong_filtered

def filter_shortsplate():
    shortsplate = read_file("shortsplate")
    shortsplate_filtered = [node[1].replace('"', "") for node in shortsplate if len(node) > 0 and node[0]=="nodes"]
    return shortsplate_filtered