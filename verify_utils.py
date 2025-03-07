import os
import analysis_utils as analysis

def require_valid_option(prompt_text, options_tuple):
    while True:
        os.system('cls')
        print(prompt_text)
        [print(f'({i+1}) {option}') for i, option in enumerate(options_tuple)]
        user_choice = analysis.get_number("Digite a opção escolhida: ")
        options_numbers = [i+1 for i in range(len(options_tuple))]
        if not user_choice in options_numbers:
            input("Opção inválida. Pressione Enter para tentar novamente")
            continue
        return options_tuple[int(user_choice)-1]