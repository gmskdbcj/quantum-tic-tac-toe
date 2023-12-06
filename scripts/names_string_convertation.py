async def short_gate(string: str):
    string = string.lower()
    if string == "hadamard" or string == "h":
        return "H"
    if string == "pauli_x" or string == "x":
        return "X"
    if string == "pauli_y" or string == "y":
        return "Y"
    if string == "pauli_z" or string == "z":
        return "Z"
    if string == "s_gate" or string == "s":
        return "S"
