import os
import generator_utils as gen
import verify_utils as verify    

def main():
    while True:
        os.system('cls')
        autogen_options = ("Probe Size Separator", "Power Nodes", "Shortslong")
        user_choice = verify.require_valid_option("Qual função deseja realizar hoje?", autogen_options)
        match user_choice:
            case "Probe Size Separator":
                probe_size = verify.require_valid_option("Digite o tamanho de agulha: ", ("39", "50", "75", "100"))
                file_name = f"size_separator_{probe_size}mils"
                file_content = gen.probe_size_separator(probe_size)
            case "Power Nodes":
                file_name = "power_nodes"
                file_content = gen.power_nodes()
            case "Shortslong":
                file_content = gen.shortslong()
        file = gen.create_file(file_name, file_content)
        
main()