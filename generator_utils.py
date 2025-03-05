import analysis_utils as analysis
import io_utils as io

def probe_size_separator(wires_path, inserts_path, probe_size):
    result = []
    wires = analysis.wires_filtered(wires_path)
    inserts = analysis.inserts_filtered(inserts_path)
    filtered_inserts_by_size = list(filter(lambda x: x["Probe_Size"] == probe_size, inserts))
    filtered_wires_by_probe = list(filter(lambda x: x["Wire_Type"] == "Pin to Prob", wires))
    for node_wires in filtered_wires_by_probe:
        for node_inserts in filtered_inserts_by_size:
            if node_wires['Wire_To'] == node_inserts['Node_Coordinate']:
                result.append(node_wires)
                continue
    return result

def power_nodes(powers_list_path, inserts_path):
    result = []
    powers_list = io.read_file(powers_list_path)
    inserts = analysis.inserts_filtered(inserts_path)
    tolerance = io.get_number("Digite a tolerância padrão: ")
    for line in powers_list:
        power = line[0]
        test_line = f'!test "{power}"  !NODE_NOT_FOUND'
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
            measure  {voltage + tolerance}, {voltage - tolerance}
        end subtest
        """
        test_info = (power, test_line, subtest)
        result.append(test_info)
    return result

power_list = "./test_examples/nodes_list_pwr_nodes"
inserts = "./test_examples/inserts_shannon_48"
    