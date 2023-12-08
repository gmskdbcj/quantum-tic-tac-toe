import pennylane as qml

from scripts.names_string_convertation import short_gate


async def quant(axis: str, basis_state, gates, last_result=None):
    for i in range(3):
        gates[i] = [await short_gate(j) for j in gates[i]]

    dev = qml.device("default.qubit", wires=3, shots=1)

    def norm_z(i):
        i = round(float(i))
        if i == -1:
            return "1"
        elif i == 1:
            return "0"
        else:
            raise TypeError

    def norm_x(i):
        i = round(float(i))
        if i == -1:
            return "-"
        elif i == 1:
            return "+"
        else:
            raise TypeError

    def norm_y(i):
        i = round(float(i))
        if i == 1:
            return "i"
        elif i == -1:
            return "-i"
        else:
            raise TypeError


    @qml.qnode(dev)
    def my_circuit(op):
        # State preparation
        for i in range(3):
            if basis_state[i] == "1":
                qml.PauliX(wires=i)
            elif basis_state[i] == "i":
                qml.Hadamard(wires=i)
                qml.S(wires=i)
            elif basis_state[i] == "-i":
                qml.PauliX(wires=i)
                qml.Hadamard(wires=i)
                qml.S(wires=i)
            elif basis_state[i] == "+":
                qml.Hadamard(wires=i)
            elif basis_state[i] == "-":
                qml.PauliX(wires=i)
                qml.Hadamard(wires=i)
            elif basis_state[i] == "0" or basis_state[i] == 0:
                pass
            else:
                raise TypeError()

        # Program
        for i in range(3):
            for j in gates[i]:
                gate = j.upper()
                if gate == "X":
                    qml.PauliX(wires=i)
                elif gate == "Y":
                    qml.PauliY(wires=i)
                elif gate == "Z":
                    qml.PauliZ(wires=i)
                elif gate == "H":
                    qml.Hadamard(wires=i)
                elif gate == "S":
                    qml.S(wires=i)
                else:
                    raise TypeError()
        opers = {
            "X": qml.PauliX,
            "Y": qml.PauliY,
            "Z": qml.PauliZ
        }
        return [qml.expval(opers[op](i)) for i in range(3)]

    # Measurment
    a = axis.upper()
    op={
        "X":norm_x,
        "Y":norm_y,
        "Z":norm_z
    }
    measurment = my_circuit(a)
    measurment = [op[a](i) for i in measurment]
    return measurment
