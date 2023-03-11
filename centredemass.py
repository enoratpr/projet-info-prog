# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 16:48:08 2023

@author: perso
"""

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



def open_mol_file():
    # file type
    filetypes = (
        ('text files', '*.mol'),
        ('All files', '*.*')
    )
    # show the open file dialog
    fichier = fd.askopenfile(filetypes=filetypes)


    
    with open(fichier.name, 'r') as f:        
        content = f.readlines()
        line4 = content[3]
        data = line4.split(" ")
        data_ok = list(filter(None,data)) #j'utilise la fonction filter ici aussi pour que ça fonctionne à tous les coups
        
        nc = int(data_ok[0])
        nl = int(data_ok[1])
        na = int(data_ok[0])

        print(nc," ",nl,"",na) #verif
        
        nc_fin = nc + 4
        nl_fin = nl + nc + 4
        na_fin = na + 4

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
        
        
        
        #extraction des atomes
        atom = []
        for line in range(4,na_fin):
            line_content = content[line].split(" ")
            line_content_ok = list(filter(None,line_content))
            atom_line = []
            atom_line.append(line_content_ok[3])
            atom.append(atom_line)
        print(atom) #verif    

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
        ax.scatter(coordinates_array[:, 0], coordinates_array[:, 1], \
                   coordinates_array[:, 2], s=600)
            
# [:, 0] première colonne du tableau numpy de la liste de coordonnées
# [:,0] correspond aux coordonnées en x
# [:,1] correspond aux y 
# [:,2] correspond aux z


        def center_of_mass(coordinates_array):
            massx = np.sum(coordinates_array[:,0])
            massy = np.sum(coordinates_array[:,1])
            massz = np.sum(coordinates_array[:,2])
            centrex = (massx)/nc 
            centrey = (massy)/nc 
            centrez =(massz)/nc
            L=[]
            L.append(centrex)
            L.append(centrey)
            L.append(centrez)
            print(L)
            
        
        

        # Tracer les liaisons
        for liaison in liaisons:
            # Récupérer les indices des deux atomes liés
            atom1_connectivite = int(liaison[0]) - 1
            atom2_connectivite = int(liaison[1]) - 1
#on enlève le  chiffre correspondant aux types de liaisons 
            # Récupérer les coordonnées des deux atomes reliés entre eux
            atom1_coord = coordinates_array[atom1_connectivite]
            atom2_coord = coordinates_array[atom2_connectivite]

            # Déterminer le type de liaison
            bond_type = int(liaison[2])*5 #grosseur de la liaison
#A faire :  grossir quand double liaison ou triple

#A faire : couleur atome et taille en fonction de l'atome faire pour ( C H O N )


            # Tracer la liaison avec la fonction plot()
            ax.plot([atom1_coord[0], atom2_coord[0]], [atom1_coord[1], \
            atom2_coord[1]], [atom1_coord[2], atom2_coord[2]], '-', \
            linewidth=bond_type, color="red")


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