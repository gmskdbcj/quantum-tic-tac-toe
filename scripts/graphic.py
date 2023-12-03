async def short_gate(string: str):
    if string == "Hadamard":
        string = "H"
    if string == "Pauli_X":
        string = "X"
    if string == "Pauli_Y":
        string = "Y"
    if string == "Pauli_Z":
        string = "Z"
    return string

"""
For example:

graphic("Z", [1, 0, 2], [["H", "X"], ["H"], ["X"]])
return this:
1: ──H──X─┤     
0: ──H────┤     
2: ──X────┤  <Z>

graphic("Z", [1, 0, 1], [["H", "X"], ["H"], ["X"]], [0, 0, 1])
return this:
1: ──H──X─┤0
0: ──H────┤0
1: ──X────┤1  <Z>
"""
async def graphic(axis, basis_state, gates, measurments=None):
    basis_state = [str(i) for i in basis_state]
    gates = [[await short_gate(j) for j in i] for i in gates]
    if measurments != None:
        measurments = [str(i) for i in measurments]

    empty_symbol = "──"
    end_symbol = "─┤"
    empty_gate = "─"
    text = ""

    length = 0
    for i in gates:
        if len(i) > length:
            length = len(i)

    for i in range(len(gates)):
        while len(gates[i]) < length:
            gates[i].append(empty_gate)

    for i in range(len(basis_state)):
        text += f"{basis_state[i]}: "
        for j in range(len(gates[i])):
            text += f"{empty_symbol}{gates[i][j]}"
        text += end_symbol
        if measurments != None:
            text += measurments[i]
        text += f"\n"
    text = text[:-1]
    text += f"  <{axis}>"
    return text