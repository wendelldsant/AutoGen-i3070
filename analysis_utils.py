import io_utils as io

def wires_filtered():
    result = []
    wires = io.read_file(file_type="wires")
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

def inserts_filtered():
    result = []
    inserts = io.read_file(file_type="inserts") 
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
        

pinslong_path = "./test_examples/pinslong_shannon_48"
shortsplate_path = "./test_examples/shortsplate"