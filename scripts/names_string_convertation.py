async def short_gate(string: str):
    string = string.lower()
    if string == "hadamard" or string == "h":
        string = "H"
    if string == "pauli_x" or string == "x":
        string = "X"
    if string == "pauli_y" or string == "y":
        string = "Y"
    if string == "pauli_z" or string == "z":
        string = "Z"
    return string
