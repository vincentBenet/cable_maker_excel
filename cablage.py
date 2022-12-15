import os
import sys
import openpyxl 
import graphviz

os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'

path_current = os.path.dirname(__file__)
path_excel = os.path.join(path_current, "cablage.xlsx")
path_graph = os.path.join(path_current, "build", "graph")
path_test = os.path.join(path_current, "test.png")

print(f"Openning file {path_excel}")

workbook = openpyxl.load_workbook(path_excel)

names_sheets = workbook.sheetnames

print(f"Sheets: {path_excel}")

# Recuperation des données du excel
data = {}
data_transformed = {}
for name_sheet in names_sheets:
    print(f"Reading sheet {name_sheet}")
    data[name_sheet] = {}
    data_transformed[name_sheet] = {}
    sheet = workbook[name_sheet]
    nb_rows = sheet.max_row
    nb_cols = sheet.max_column
    names_columns = [header.value for header in sheet[1]]
    for name_column in names_columns:
        data[name_sheet][name_column] = []
    for i_line in range(1, nb_rows):
        values = [line.value for line in sheet[i_line+1]]
        for i_value, value in enumerate(values):
            data[name_sheet][names_columns[i_value]].append(value)
    
    for i_nom, nom in enumerate(data[name_sheet]["Nom"]):
        data_transformed[name_sheet][nom] = {}
        for name_column in names_columns:
            data_transformed[name_sheet][nom][name_column] = data[name_sheet][name_column][i_nom]

# Create graph
graph = graphviz.Digraph(
    'G', 
    filename=path_graph, 
    format="svg",
    graph_attr={
        "rankdir": "BT",
    },
    node_attr={
        "shape": "plaintext",
    },
)
graph.attr(
    rank= "same",
)


# Create connectors nodes with pins
for i_node in range(len(data["Connecteurs"])-1):
    name_node = data["Connecteurs"]["Nom"][i_node]
    type_connecteur = data["Connecteurs"]["_Type connecteur"][i_node]
    
    connection = ""
    interface = ""
    connecteur = ""
    
    for connection_line in data_transformed["Connections"]:
        connecteurs = [
            data_transformed["Connections"][connection_line]["From Connecteur"],
            data_transformed["Connections"][connection_line]["To Connecteur"]
        ]
        if name_node in connecteurs:
            connection = data_transformed["Connections"][connection_line]["Nom"]
            if name_node == connecteurs[0]:
                interface = data_transformed["Connections"][connection_line]["Interface From"]
                connecteur = data_transformed["Connections"][connection_line]["From Connecteur"]
            if name_node == connecteurs[1]:
                interface = data_transformed["Connections"][connection_line]["Interface To"]
                connecteur = data_transformed["Connections"][connection_line]["To Connecteur"]
            break
    
    
    pins_connecteurs = {}
    for pin_connector in data_transformed["Fils"]:
        if data_transformed["Fils"][pin_connector]["_Connecteur"] != connecteur:
            continue
        name_pin_connector = data_transformed["Fils"][pin_connector]["_Pin"]
        type_pin_connector = data_transformed["Pins"][name_pin_connector]["_Type Pin"]
        
        pins_connecteurs[pin_connector] = {
            "Nom": pin_connector,
            "Label": data_transformed["Fils"][pin_connector]["Label"],
            "Couleur": data_transformed["Fils"][pin_connector]["Couleur"],
            "Numero": data_transformed["Pins"][name_pin_connector]["Numero"],
            "Position": data_transformed["Pins"][name_pin_connector]["Label"],
            "x_pos": data_transformed["Pins"][name_pin_connector]["x_pos"],
            "y_pos": data_transformed["Pins"][name_pin_connector]["y_pos"],
            "PinType": type_pin_connector,
            "Reference Fabricant": data_transformed["Types Pins"][type_pin_connector]["Reference Fabricant"],
            "Reference Interne": data_transformed["Types Pins"][type_pin_connector]["Reference Interne"],
            "Reference Interne": data_transformed["Types Pins"][type_pin_connector]["Reference Interne"],
        }
    
    graph.node(f"svg_{type_connecteur}", **{
        "label": "",
        "image": os.path.join(path_current, f"{type_connecteur}.svg"),
        "shape": "none",
    })    
    
    label = '{'+type_connecteur+'|{'
    for pin_connecteur in pins_connecteurs:
        subnode = str(pins_connecteurs[pin_connecteur]["Position"])
        label += f"{subnode}|"
        
        graph.edge(
            f"{name_node}:subnode", 
            f'interface_{name_node}',
            **{
                "color": pins_connecteurs[pin_connecteur]["Couleur"],
                "label": pins_connecteurs[pin_connecteur]["Label"]
            }
        )
        
    
        
    label = label[:-1]
    label +='}}' 
    tooltip = str(pins_connecteurs)
    
    print("_")
    print(f"Connecteur: {name_node}")
    print(f"Type connecteur: {type_connecteur}")
    
    graph.node(name_node, **{
        "xlabel": connecteur,
        "label": label,
        "tooltip": tooltip,
        'shape': 'record',
    })
    
    graph.node(f'interface_{name_node}', **{
        "label": interface,
    })
    
    
    graph.edge(
        f"svg_{type_connecteur}",
        name_node, **{
            "arrowhead": "none"
        }
    )
    
# Create interface nodes


# Create links


# SVG representation for connectors

for connection in data_transformed["Connections"]:
    graph.edge(
        f'interface_{data_transformed["Connections"][connection]["From Connecteur"]}', 
        f'interface_{data_transformed["Connections"][connection]["To Connecteur"]}'
    )
graph.view()
