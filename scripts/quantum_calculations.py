import pennylane as qml


async def quant(axis: str, basis_state, gates):
    dev = qml.device("default.qubit", wires=3, )

    @qml.qnode(dev)
    def my_circuit():
        # State preparation
        for i in range(3):
            if basis_state[i] == 1:
                qml.PauliX(wires=i)
            elif basis_state[i] == -1:
                qml.PauliZ(wires=i)
            elif basis_state[i] == 0:
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
                else:
                    raise TypeError()

        # Measurment
        a = axis.upper()
        if a == "X":
            return [qml.expval(qml.PauliX(i)) for i in range(3)]
        elif a == "Y":
            return [qml.expval(qml.PauliY(i)) for i in range(3)]
        elif a == "Z":
            return [qml.expval(qml.PauliZ(i)) for i in range(3)]
        else:
            raise TypeError()

    measurment = my_circuit()
    return [round(float(i)) for i in measurment]
