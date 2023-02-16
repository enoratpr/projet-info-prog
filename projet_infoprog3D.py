import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Root window
root = tk.Tk()
root.title('coordonnées de la molécule')
root.resizable(False, False)
root.geometry('550x250')

# Text editor
text = tk.Text(root, height=12)
text.grid(column=0, row=0, sticky='nsew')


def open_mol_file():
    # file type
    filetypes = (
        ('text files', '*.mol'),
        ('All files', '*.*')
    )
    # show the open file dialog
    fichier = fd.askopenfile(filetypes=filetypes)
#######
    # read the text file
    #print(fichier.name)
    #line =f.read()
    #print(line)
    #fichier.close()
#######

    
    with open(fichier.name, 'r') as f:        
        content = f.readlines()
        line4 = content[3]
        data = line4.split(" ")
        data_ok = list(filter(None,data)) #j'utilise la fonction filter ici aussi pour que ça fonctionne à tous les coups
        
        nc = int(data_ok[0])
        nl = int(data_ok[1])

        print(nc," ",nl) #verif
        
        nc_fin = nc + 4
        nl_fin = nl + nc + 4

        #extraction des coordonnées
        coo = []
        for line in range(4,nc_fin):
            line_content = content[line].split(" ")
            line_content_ok = list(filter(None,line_content))
            coo_line = []
            coo_line.append(line_content_ok[0])
            coo_line.append(line_content_ok[1])
            coo_line.append(line_content_ok[2])
            coo.append(coo_line)
        print(coo) #verif

        #extraction des liaisons
        liaisons = []
        for line in range(nc_fin,nl_fin):
            line_content = content[line].split(" ")
            line_content_ok = list(filter(None,line_content))
            liaison_line = []
            liaison_line.append(line_content_ok[0])
            liaison_line.append(line_content_ok[1])
            liaison_line.append(line_content_ok[2])
            liaisons.append(liaison_line)
        print(liaisons) #verif
        
        # Convertir les coordonnées en un tableau NumPy
        coordinates_array = np.array(coo, dtype=float)

        # Créer une figure 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Tracer les atomes
        ax.scatter(coordinates_array[:, 0], coordinates_array[:, 1], coordinates_array[:, 2], s=100)

        # Tracer les liaisons
        for liaison in liaisons:
            # Récupérer les indices des deux atomes liés
            atom1_index = int(liaison[0]) - 1
            atom2_index = int(liaison[1]) - 1

            # Récupérer les coordonnées des deux atomes
            atom1_coord = coordinates_array[atom1_index]
            atom2_coord = coordinates_array[atom2_index]

            # Déterminer le type de liaison
            bond_type = int(liaison[2])*5

            # Tracer la liaison avec la fonction plot()
            ax.plot([atom1_coord[0], atom2_coord[0]], [atom1_coord[1], atom2_coord[1]], [atom1_coord[2], atom2_coord[2]], '-', linewidth=bond_type, color="red")


        # Ajouter les labels pour chaque axe
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Afficher la figure
        plt.show()




# open file button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=open_mol_file
)
#position et taille du bouton open a file
open_button.grid(column=0, row=1, sticky='w', padx=10, pady=10)


root.mainloop()

