def parseCkt(file):
    components = {}
    if file == "":
        raise FileNotFoundError("Please give the name of a valid SPICE file as input")
    try:
        with open(file, "r") as f:
            lines = f.readlines()
            parsing_circuit = False
            for line in lines:
                line = line.strip()
                if line.startswith(".circuit"):
                    parsing_circuit = True
                elif line.startswith(".end"):
                    parsing_circuit = False
                elif parsing_circuit and line:
                    line = line.split("#")[0]
                    parts = line.split()
                    if "dc" in parts:
                        parts.remove("dc")
                    if len(parts) >= 4 and parts[3].isnumeric():
                        components[parts[0]] = parts[1:]
                    else:
                        raise ValueError()
            return components
    except:
        raise TypeError("Please give the name of a valid SPICE file as input")

def createNode(components):
    nodes = {}
    for element in components:
        node1 = components[element][0]
        node2 = components[element][1]

        if node1 not in nodes:
            nodes[node1] = {}
        if node2 not in nodes:
            nodes[node2] = {}

    for pivot in nodes:
        for target in nodes:
            nodes[pivot][target] = {"elt": "", "value": 0.0}

    for element in components:
        node1 = components[element][0]
        node2 = components[element][1]
        nodes[node1][node2]["elt"] = element
        nodes[node1][node2]["value"] = float(components[element][2])

        return nodes

def createMatrix(nodes):
    nodes_order = sorted(nodes.keys())
    nodes_order.remove('GND')
    nodes_order.append('GND')
    print(nodes_order)
    matrix_order = len(nodes)
    print(matrix_order)
    

def evalSpice():
    file = "test_2.ckt"
    ckt = parseCkt(file)
    nodes = createNode(ckt)
    print(nodes)
    createMatrix(nodes)

evalSpice()
