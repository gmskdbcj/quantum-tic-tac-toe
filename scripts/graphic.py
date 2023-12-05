from scripts.names_string_convertation import short_gate

"""
For example:

graphic("Z", [1, 0, 2], [["H", "X"], ["H"], ["X"]])
return this:
1: ──H──X─┤     
0: ──H────┤     
2: ──X────┤  _Z_

graphic("Z", [1, 0, 1], [["H", "X"], ["H"], ["X"]], [0, 0, 1])
return this:
1: ──H──X─┤0
0: ──H────┤0
1: ──X────┤1  _Z_
"""
async def graphic(axis, basis_state, gates, measurments=None):
    basis_state = [str(i) for i in basis_state]
    gates = [[await short_gate(j) for j in i] for i in gates]
    if measurments != None and measurments != []:
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
        text += f"{basis_state[i].rjust(2)}: "
        for j in range(len(gates[i])):
            text += f"{empty_symbol}{gates[i][j].upper()}"
        text += end_symbol
        if measurments != None and measurments != []:
            text += measurments[i].rjust(2)
        text += f"\n"
    text = text[:-1]
    text += f"  _{axis}_"
    return "<code>" + text + "</code>"