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
root.geometry('500x80')


def open_mol_file():
    # définir le type de fichiers
    filetypes = (('text files', '*.mol'), ('All files', '*.*'))
    # afficher la boîte de dialogue d'ouverture de fichier
    fichier = fd.askopenfile(filetypes=filetypes)

    
    with open(fichier.name, 'r') as f:        
        content = f.readlines()
        line4 = content[3]
        data = line4.split(" ")
        data_ok = list(filter(None,data)) #j'utilise la fonction filter ici aussi pour que ça fonctionne à tous les coups
        
        nc = int(data_ok[0]) # Nombre coordonées
        nl = int(data_ok[1]) # Nombre liaisons 
        
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
        
        
        #extraction des atomes
        atom = []
        for line in range(4,nc_fin):
            line_content = content[line].split(" ")
            line_content_ok = list(filter(None,line_content))
            atom_line = []
            atom_line.append(line_content_ok[3])
            atom.append(atom_line[0])  


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
            
            
        #une boîte cubique dans laquelle votre molécule se trouvera forcément en entier,
        #sans avoir de problème de liaison éclatée    
        x_min, y_min, z_min = np.min(coordinates_array, axis=0)
        x_max, y_max, z_max = np.max(coordinates_array, axis=0)
        
        # Trouver la plus grande valeur absolue parmi les valeurs min/max
        limit = max(abs(x_min), abs(x_max), abs(y_min), abs(y_max), abs(z_min), abs(z_max))
        # Multiplier par 1.1 ou 1.2 pour éviter de couper des atomes en deux sur la limite
        limit *= 1.2 
        
        # Créer une figure 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim([-limit, limit])
        ax.set_ylim([-limit, limit])
        ax.set_zlim([-limit, limit])

       
       #Couleur atome 

        letters = ['C', 'H', 'N', 'O', 'S', 'Cl']
        x1 = coordinates_array[:,0]
        y1 = coordinates_array[:,1]
        z1 = coordinates_array[:,2]

        colors = {'O': 'red', 'H': 'white', 'N': 'blue', 'C': 'black', \
                  'S': 'yellow', 'Cl': 'green'}
        size = {'O': 1000, 'H': 500, 'N': 1500, 'C': 2000, 'S' : 1000, 'Cl': 750}
        
        atom_color_list=[]
        
        for i, letters in enumerate(atom):
                ax.scatter(x1[i], y1[i], z1[i], color=colors[letters], marker='o', s=size[letters])
                atom_color_list.append((letters, colors[letters]))

        print(set(atom_color_list)) #permet à ce que la liste soit non redondante
        
          
        fig.set_facecolor('grey')
     
        
        #linéarité de la molécule 
        # initialiser une variable pour stocker si la molécule est linéaire ou non
        is_linear = False
        
        for i in range(len(coordinates_array)):
           for j in range(i+1, len(coordinates_array)):
        # calculer le produit scalaire entre les vecteurs i et j
            vi = coordinates_array[i] / (np.linalg.norm(coordinates_array[i]) + 1e-16) #le 1e-16 sert juste Ã  Ã©viter le cas oÃ¹ la norme serait nulle
            vj = coordinates_array[j] / (np.linalg.norm(coordinates_array[j]) + 1e-16) #mÃªme si normalement on l'a dÃ©jÃ  Ã©vitÃ© avec les continue plus haut
            vect = np.dot(vi, vj)
            #print(vect)
            
        # stocker le produit scalaire linéaire s'il est trouvé
            if abs(vect) == 1 or nc == 2:
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
            if nc > 2 : 
                # Molécule plane      
                
                # Calculer les vecteurs de liaison entre les atomes
                vectors_array = np.diff(coordinates_array, axis=0)
        
                # Calculer le vecteur normal à la molécule
                normal_vector = np.cross(vectors_array[0], vectors_array[1])
        
               
                # Vérifier que tous les vecteurs de liaison sont parallèles au vecteur normal
                
                is_planar = True
                tolerance = 1e-10
                for i in range(len(vectors_array)):
                    dot_product = np.dot(vectors_array[i], normal_vector)
                    if not np.isclose(dot_product, 0, atol=tolerance):
                        is_planar = False
                        break
                
            # Afficher le résultat
                if is_planar:
                    print("La molécule est plane.") 
                else:
                    print("La molécule n'est pas plane.")
            else :
                print("La molécule ne comporte que deux atomes, elle ne peut donc être plane")
                
        plt.show()
        
            
        #Centre de masse 
        # [:, 0] première colonne du tableau numpy de la liste de coordonnées
        # [:,0] correspond aux coordonnées en x
        # [:,1] correspond aux y 
        # [:,2] correspond aux z
        mean1 = np.mean(coordinates_array[:,0])
        mean2 = np.mean(coordinates_array[:,1])
        mean3 = np.mean(coordinates_array[:,2])
        x = mean1
        y = mean2
        z = mean3
        color = 'purple'
        ax.scatter(x, y, z, s=100, c=color, marker='o')
        plt.show()

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
            bond_type = int(liaison[2]) #le 3 ème élément de la liste liaison
            
       
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
                    
                ax.plot([atom1_coord[0], atom2_coord[0]], [atom1_coord[1]-0.08, \
                atom2_coord[1]-0.08], [atom1_coord[2], atom2_coord[2]], '-', \
                linewidth=3, color="red") 
                    
                ax.plot([atom1_coord[0], atom2_coord[0]], [atom1_coord[1]+0.08, \
                atom2_coord[1]+0.08], [atom1_coord[2], atom2_coord[2]], '-', \
                linewidth=3, color="red")                    
              
            
            else :
                ax.plot([atom1_coord[0], atom2_coord[0]], [atom1_coord[1], \
                atom2_coord[1]], [atom1_coord[2], atom2_coord[2]], '-', \
                linewidth=3, color="red")
                
        plt.show()




# crée un bouton pour avoir accès à nos fichiers
open_button = ttk.Button(root, text='Open a File', command=open_mol_file)
#position et taille du bouton open a file
open_button.grid(column=0, row=1 , padx=10, pady=10)


root.mainloop()
