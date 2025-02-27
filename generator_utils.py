import analysis_utils as analysis

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