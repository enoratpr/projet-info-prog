# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 20:22:53 2023

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
root.title('Coordonnées de la molécule')
root.resizable(False, False)
root.geometry('400x80')


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
        
        nc = int(data_ok[0]) # Nombre coordonées
        nl = int(data_ok[1]) # Nombre liaisons 
    

        print(nc," ",nl,"") #verif
        
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
        
        #extraction des atomes
        atom = []
        for line in range(4,nc_fin):
            line_content = content[line].split(" ")
            line_content_ok = list(filter(None,line_content))
            atom_line = []
            atom_line.append(line_content_ok[3])
            atom.append(atom_line[0])  
        print(atom)#verif 


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
        
        
  # Calculer le centre des atomes
        center = np.mean(coordinates_array, axis=0)

        # calcul de la translation nécessaire pour ramener le centre de masse à (0, 0, 0)
        translation = -center

        # translation des coordonnées
        translated_coordinates = coordinates_array + translation

        # vérification si la molécule possède un centre d'inversion
        has_inversion_center = True

        for coord in coordinates_array:
            inv_coord = -coord
            if not np.any((coordinates_array == inv_coord).all(axis=1)):
                has_inversion_center = False
                break

        if has_inversion_center:
            print("La molécule possède un centre d'inversion.")
        else:
            print("La molécule ne possède pas de centre d'inversion.")

        # Créer une figure 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Tracer les atomes
        #ax.scatter(coordinates_array[:, 0], coordinates_array[:, 1], \
                  # coordinates_array[:, 2], s=600)
            
        #Couleur atome 

        letters = ['C', 'H', 'N', 'O', 'S', 'Cl']
        x1 = coordinates_array[:,0]
        y1 = coordinates_array[:,1]
        z1 = coordinates_array[:,2]

        colors = {'O': 'red', 'H': 'white', 'N': 'blue', 'C': 'black', \
                  'S': 'yellow', 'Cl': 'green'}
        size = {'O': 1000, 'H': 300, 'N': 1500, 'C': 2000, 'S' : 1000, 'Cl': 750}
        
        atom_color_list=[]
        
        for i, letters in enumerate(atom):
                ax.scatter(x1[i], y1[i], z1[i], color=colors[letters], marker='o', s=size[letters])
                atom_color_list.append((letters, colors[letters]))

        print(atom_color_list)
        
          
        fig.set_facecolor('grey')
     
        
        #linéarité de la molécule 
        # initialiser une variable pour stocker si la molécule est linéaire ou non
        is_linear = False
        
        for i in range(len(coordinates_array)):
           for j in range(i+1, len(coordinates_array)):
        # calculer le produit scalaire entre les vecteurs i et j
            vector_i_dot_vector_j = np.dot(coordinates_array[i], coordinates_array[j])
            vect = int(vector_i_dot_vector_j)

        # stocker le produit scalaire linéaire s'il est trouvé
            if abs(vect) == 1:
                is_linear = True
                break
        
            if is_linear:  # sortir de la boucle externe si un produit scalaire linéaire 
            #a été trouvé
               break 
         
            # imprimer le résultat
        if is_linear:
            print("La molécule est linéaire ")
        else:
            print("La molécule n'est pas linéaire.")
            
        # Molécule plane      
        # Calculer les vecteurs de liaison entre les atomes
        vectors_array = np.diff(coordinates_array, axis=0)

        # Calculer le vecteur normal à la molécule
        normal_vector = np.cross(vectors_array[0], vectors_array[1])

       # Vérifier que tous les angles sont proches de 90 degrés
        is_planar = False
        for i in range(1, len(vectors_array)):
            angle = np.rad2deg(np.arccos(np.dot(vectors_array[i-1],vectors_array[i]) / \
                    (np.linalg.norm(vectors_array[i-1]) \
                    * np.linalg.norm(vectors_array[i]))))
            angle_verif = abs(angle - 90)
            if angle_verif==90:  # tolérance de 0.01 degré 
               is_planar = True
               break
            else : 
               is_planar = False

     # Afficher le résultat
        if is_planar:
            print("La molécule est plane.") 
        else:
            print("La molécule n'est pas plane.")
            
        
        # Ajouter les labels pour chaque axe
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

   
        plt.show()
        
            
        #Centre de masse 
        mean1 = np.mean(coordinates_array[:,0])
        mean2 = np.mean(coordinates_array[:,1])
        mean3 = np.mean(coordinates_array[:,2])
        x = mean1
        y = mean2
        z = mean3
        color = 'purple'
        ax.scatter(x, y, z, s=100, c=color, marker='o')
        plt.show()
        print(mean1, mean2, mean3)




# [:, 0] première colonne du tableau numpy de la liste de coordonnées
# [:,0] correspond aux coordonnées en x
# [:,1] correspond aux y 
# [:,2] correspond aux z

        # Tracer les liaisons
        for liaison in liaisons:
            # Récupérer les indices des deux atomes liés
            atom1_connectivite = int(liaison[0]) - 1
            atom2_connectivite = int(liaison[1]) - 1
#on enlève le  chiffre correspondant aux types de liaisons 
            # Récupérer les coordonnées des deux atomes reliés entre eux
            atom1_coord = coordinates_array[atom1_connectivite]
            atom2_coord = coordinates_array[atom2_connectivite]
            #tracer des liaisons simples, doubles et triples
            bond_type = int(liaison[2])
            
       
            if bond_type == 2 :
                ax.plot([atom1_coord[0], atom2_coord[0]], [atom1_coord[1]+0.05, \
                atom2_coord[1]+0.05], [atom1_coord[2], atom2_coord[2]], '-', \
                linewidth= 3, color="red")
                    
                ax.plot([atom1_coord[0], atom2_coord[0]], [atom1_coord[1]-0.05, \
                atom2_coord[1]-0.05], [atom1_coord[2],atom2_coord[2]], '-', linewidth= 3, color="red")
            
            
            elif bond_type == 3 :
                ax.plot([atom1_coord[0], atom2_coord[0]], [atom1_coord[1], \
                atom2_coord[1]], [atom1_coord[2], atom2_coord[2]], '-', \
                linewidth=3, color="red")
                    
                ax.plot([atom1_coord[0], atom2_coord[0]], [atom1_coord[1]-0.001, \
                atom2_coord[1]-0.001], [atom1_coord[2], atom2_coord[2]], '-', \
                linewidth=3, color="red") 
                    
                ax.plot([atom1_coord[0], atom2_coord[0]], [atom1_coord[1]+0.001, \
                atom2_coord[1]+0.001], [atom1_coord[2], atom2_coord[2]], '-', \
                linewidth=3, color="red")
                    
              
            
            else :
                ax.plot([atom1_coord[0], atom2_coord[0]], [atom1_coord[1], \
                atom2_coord[1]], [atom1_coord[2], atom2_coord[2]], '-', \
                linewidth=3, color="red")
                    
                
                    
        ax.set_box_aspect([1, 1, 1])
        ax.set_ylim(-1, 1)
                
        plt.show()




# open file button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=open_mol_file
)
#position et taille du bouton open a file
open_button.grid(column=0, row=1 , padx=10, pady=10)


root.mainloop()
