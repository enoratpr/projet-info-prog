import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

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
    # read the text file
#######
    #print(fichier.name)
    #line =f.read()
    #print(line)
    #fichier.close()
#######
    with open(fichier.name, 'r') as f:        
        content = f.readlines()
        line4 = content[3]
        data = line4.split(" ")
        
        nc = int(data[2])
        nl = int(data[4])
        print(nc, ' ', nl)
        
        nc_fin = nc + 4
        nl_fin = nl + nc + 4
        
        coo = []
        for line in range(4,nc_fin):
            line_content = content[line].split(" ")
            line_content_ok = list(filter(None,line_content))
            coo_line = []
            coo_line.append(line_content_ok[0])
            coo_line.append(line_content_ok[1])
            coo_line.append(line_content_ok[2])
            coo.append(coo_line)
        print(coo)
        

        liaisons = []
        for line in range(nc_fin,nl_fin):
            line_content = content[line].split(" ")
            line_content_ok = list(filter(None,line_content))
            liaisons_line = []
            liaisons_line.append(line_content_ok[0])
            liaisons_line.append(line_content_ok[1])
            liaisons_line.append(line_content_ok[2])
            liaisons.append(liaisons_line)
        print(liaisons)


# open file button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=open_mol_file
)
#position et taille du bouton open a file
open_button.grid(column=0, row=1, sticky='w', padx=10, pady=10)

root.mainloop()





    

    

