import analysis_utils as analysis
import io_utils as io

def probe_size_separator(probe_size):
    result = []
    wires = analysis.wires_filtered()
    inserts = analysis.inserts_filtered()
    filtered_inserts_by_size = list(filter(lambda x: x["Probe_Size"] == probe_size, inserts))
    filtered_wires_by_probe = list(filter(lambda x: x["Wire_Type"] == "Pin to Prob", wires))
    for node_wires in filtered_wires_by_probe:
        for node_inserts in filtered_inserts_by_size:
            if node_wires['Wire_To'] == node_inserts['Node_Coordinate']:
                result.append(node_wires)
                continue
    return result

def power_nodes():
    result = []
    powers_list = io.read_file(file_type="powers_list")
    inserts = analysis.inserts_filtered()
    tolerance = io.get_number("Digite a tolerância padrão: ")
    for line in powers_list:
        power = line[0]
        test_line = f'!test "{power}"  !NODE NOT FOUND'
        for node in inserts:
            if node["Node_Name"] == power:
                test_line = f'test "{power}"'
                break
        voltage = io.get_number(f"Digite o valor da tensão {power}: ")
        subtest = f"""
        subtest "{power}"
            connect i to nodes "{power}"
            connect l to nodes ground
            detector dcv, expect {voltage}
            measure  {voltage + tolerance:.2f}, {voltage - tolerance:.2f}
        end subtest
        """
        test_info = {
            "Node_name": power,
            "Voltage": voltage,
            "Test": test_line, 
            "Subtest": subtest
            }
        result.append(test_info)
    return result

def shortslong():
    pinslong = io.read_file(file_type="pinslong")
    shortsplate = io.read_file(file_type="shortsplate")
    pinslong_filtered = [node[1].replace('"', "") for node in pinslong if len(node) > 0 and node[0]=="nodes"]
    shortsplate_filtered = [node[1].replace('"', "") for node in shortsplate if len(node) > 0 and node[0]=="nodes"]
    result = [f'nodes "{node}"' for node in shortsplate_filtered if not node in pinslong_filtered]
    return result