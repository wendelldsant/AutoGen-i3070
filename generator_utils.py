import analysis_utils as analysis

def probe_size_separator(probe_size:str):
    result = []
    wires_filtered = analysis.filter_wires()
    inserts_filtered = analysis.filter_inserts()
    filtered_inserts_by_size = list(filter(lambda x: x["Probe_Size"] == probe_size, inserts_filtered))
    filtered_wires_by_probe = list(filter(lambda x: x["Wire_Type"] == "Pin to Prob", wires_filtered))
    for node_wires in filtered_wires_by_probe:
        for node_inserts in filtered_inserts_by_size:
            if node_wires['Wire_To'] == node_inserts['Node_Coordinate']:
                main_info = (f"Color: {node_wires["Wire_Color"]}", f"Wiring: {node_wires["Wiring"]}")
                result.append(main_info)
                continue
    return result

def power_nodes():
    result = []
    powers_list = analysis.read_file("powers_list")
    inserts_filtered = analysis.filter_inserts()
    tolerance = analysis.get_number("Digite a tolerância padrão: ")
    for line in powers_list:
        power = line[0]
        test_line = f'!test "{power}"  !NODE NOT FOUND'
        for node in inserts_filtered:
            if node["Node_Name"] == power:
                test_line = f'test "{power}"'
                break
        voltage = analysis.get_number(f"Digite o valor da tensão {power}: ")
        subtest = (
                    f'\nsubtest "{power}"\n'
                    f'  connect i to nodes "{power}"\n'
                    f'  connect l to nodes ground\n'
                    f'  detector dcv, expect {voltage}\n'
                    f'  measure  {voltage + tolerance:.2f}, {voltage - tolerance:.2f}\n'
                    f'end subtest\n'
                )
        test_info = {
            "Node_name": power,
            "Voltage": voltage,
            "Test": test_line, 
            "Subtest": subtest
            }
        result.append(test_info)
    result.sort(key = lambda power: power["Voltage"], reverse=True)
    test_lines = [power["Test"] for power in result]
    test_lines.append("\nend test")
    subtest_lines = [power["Subtest"] for power in result]
    power_nodes = test_lines + subtest_lines
    return power_nodes

def shortslong():
    pinslong_filtered = analysis.filter_pinslong()
    shortsplate_filtered = analysis.filter_shortsplate()
    result = [f'nodes "{node}"' for node in shortsplate_filtered if not node in pinslong_filtered]
    return result

def create_file(file_type, file_content):
    output_directory = input(f'Digite o caminho de saída do arquivo {file_type}: ')
    output_file = f"{output_directory}/{file_type}.txt"
    with open(output_file, "w") as file:
        for line in file_content:
            file.write(f"{line}\n")