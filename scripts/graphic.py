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
For example
graphic("Z", [1, 0, 2], [["H", "X"], ["H"], ["X"]])
return this:
1: ──H──X─┤     
0: ──H────┤     
2: ──X────┤  <Z>
"""
async def graphic(axis, start_conditions, gates):
    start_conditions = [str(i) for i in start_conditions]
    gates = [[await short_gate(j) for j in i] for i in gates]

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

    for i in range(len(start_conditions)):
        text += f"{start_conditions[i]}: "
        for j in range(len(gates[i])):
            text += f"{empty_symbol}{gates[i][j]}"
        text += f"{end_symbol}\n"
    text = text[:-1]
    text += f"  <{axis}>"
    return text