import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageSequence
import os
import shutil
import random
from datetime import datetime
import time
import emoji

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Reddit Image Sorter")
        self.state('zoomed')
        self.configure(bg='#f0f0f0')
        self.subreddits = self.lire_subreddits()
        
        # Modification pour pointer vers le dossier python-tri-photo
        script_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Script directory: {script_dir}")  # Debug
        # On utilise le nom exact du dossier avec la bonne casse
        self.source_dir = script_dir  # On utilise directement le dossier du script
        print(f"Source directory: {self.source_dir}")  # Debug
        
        self.creer_interface()
        self.images = []
        self.current_gif = None
        self.gif_frames = []
        self.current_frame = 0
        
        # Chargement différé des images
        self.after(1, self.charger_images_initiales)

    def charger_images_initiales(self):
        print(f"Searching for images in: {self.source_dir}")  # Debug
        self.images = [file for file in os.listdir(self.source_dir) 
                      if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        print(f"Images trouvées : {len(self.images)}")  # Debug
        if self.images:
            print(f"First image found: {self.images[0]}")  # Debug
            self.afficher_image()

    def lire_subreddits(self):
        # Lecture et organisation des subreddits depuis le fichier texte
        categories = []
        current_category = None
        subreddits = []
        
        with open("subreddit_list.txt", "r", encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    if line.startswith("[CATEGORY]"):
                        if current_category:
                            categories.append((current_category, subreddits))
                            subreddits = []
                        current_category = line[9:]  # Enlever le préfixe [CATEGORY]
                    elif line:
                        subreddits.append(line)
                        
        if current_category and subreddits:
            categories.append((current_category, subreddits))
            
        return categories

    def creer_interface(self):
        # Frame gauche 
        self.frame_gauche = tk.Frame(self, bg='#ffffff', relief=tk.RIDGE, bd=2)
        self.frame_gauche.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

        # Titre pour la liste des subreddits
        tk.Label(self.frame_gauche, text="Available subreddits", 
                font=('Helvetica', 12, 'bold'), bg='#ffffff').pack(pady=10)

        # Frame pour les checkboxes avec scrollbar
        checkbox_frame = tk.Frame(self.frame_gauche, bg='#ffffff')
        checkbox_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(checkbox_frame, bg='#ffffff')
        scrollbar = tk.Scrollbar(checkbox_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')

        # Modification de l'affichage des subreddits
        self.subreddit_vars = {}
        for category, subreddits in self.subreddits:
            # Titre de catégorie avec emoji en couleur
            category_label = tk.Label(scrollable_frame, 
                                    text=category,
                                    bg='#ffffff',
                                    font=('TkDefaultFont', 16, 'bold'))  # Changement de police et taille
            category_label.pack(anchor='w', pady=(10,5))
            
            # Subreddits de la catégorie
            for subreddit in subreddits:
                var = tk.BooleanVar()
                chk = tk.Checkbutton(scrollable_frame, text=subreddit, 
                                   variable=var, bg='#ffffff', 
                                   font=('Helvetica', 10))
                chk.pack(anchor='w', pady=2)
                self.subreddit_vars[subreddit] = var

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bouton de sélection du dossier source
        self.bouton_selectionner_dossier = tk.Button(
            self.frame_gauche,
            text="Change source folder",
            command=self.selectionner_dossier,
            bg='#4CAF50',
            fg='white',
            font=('Helvetica', 10),
            relief=tk.RAISED,
            padx=10,
            pady=5
        )
        self.bouton_selectionner_dossier.pack(pady=20)

        # Frame droite 
        self.frame_droite = tk.Frame(self, bg='#ffffff', relief=tk.RIDGE, bd=2)
        self.frame_droite.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Canvas avec bordure
        self.canvas = tk.Canvas(
            self.frame_droite,
            width=800,
            height=600,
            bg='#ffffff',
            relief=tk.SUNKEN,
            bd=2
        )
        self.canvas.pack(pady=10)

        # Ajout des labels pour le nom et le poids du fichier
        self.filename_label = tk.Label(
            self.frame_droite,
            text="",
            bg='#ffffff',
            font=('Helvetica', 10)
        )
        self.filename_label.pack()

        self.filesize_label = tk.Label(
            self.frame_droite,
            text="",
            bg='#ffffff',
            font=('Helvetica', 10)
        )
        self.filesize_label.pack()

        # Bouton de tri
        self.bouton_trier = tk.Button(
            self.frame_droite,
            text="Sort images",
            command=self.trier_images,
            bg='#2196F3',
            fg='white',
            font=('Helvetica', 10, 'bold'),
            relief=tk.RAISED,
            padx=20,
            pady=10
        )
        self.bouton_trier.pack(pady=20)

    def selectionner_dossier(self):
        nouveau_dossier = filedialog.askdirectory(title="Sélectionner le dossier source")
        if nouveau_dossier:  # Seulement si un nouveau dossier est sélectionné
            self.source_dir = nouveau_dossier
            self.images = [file for file in os.listdir(self.source_dir) 
                         if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
            self.afficher_image()

    def afficher_image(self):
        # Affiche une image aléatoire du dossier sélectionné
        # Gère à la fois les images statiques et les GIFs
        if not self.images:
            messagebox.showinfo("Info", "No images available in selected folder.")
            return

        image_path = os.path.join(self.source_dir, random.choice(self.images))
        
        # Mise à jour des labels nom et taille
        self.filename_label.config(text=os.path.basename(image_path))
        filesize = os.path.getsize(image_path) / (1024 * 1024)  # Conversion en Mo
        self.filesize_label.config(text=f"{filesize:.2f} MB")

        # Gestion des GIF
        if image_path.lower().endswith('.gif'):
            self.gif_frames = []
            gif = Image.open(image_path)
            
            for frame in ImageSequence.Iterator(gif):
                frame = frame.resize((600, 400), Image.LANCZOS)
                self.gif_frames.append(ImageTk.PhotoImage(frame))
            
            self.current_frame = 0
            self.current_gif = image_path
            self.update_gif_frame()
        else:
            self.current_gif = None
            image = Image.open(image_path)
            image = image.resize((600, 400), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def update_gif_frame(self):
        # Met à jour l'animation des GIFs frame par frame
        if self.current_gif and self.gif_frames:
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, 
                                   image=self.gif_frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
            self.after(100, self.update_gif_frame)

    def trier_images(self):
        # Trie les images vers les dossiers des subreddits sélectionnés
        # Renomme les fichiers avec le format : nom_[subreddit]_date
        selected_subreddits = [subreddit for subreddit, var in self.subreddit_vars.items() 
                              if var.get()]
        if not selected_subreddits:
            messagebox.showwarning("Avertissement", 
                                 "Veuillez sélectionner au moins un subreddit.")
            return

        if len(selected_subreddits) > len(self.images):
            messagebox.showwarning("Avertissement", 
                                 "Pas assez d'images pour le nombre de subreddits sélectionnés.")
            return

        random.shuffle(self.images)
        date_str = datetime.now().strftime("%y %m %d")
        
        for subreddit in selected_subreddits:
            image_name = self.images.pop()
            base_name, ext = os.path.splitext(image_name)
            new_name = f"{base_name}_[{subreddit}]_{date_str}{ext}"
            
            image_path = os.path.join(self.source_dir, image_name)
            target_dir = os.path.join("Content", subreddit)
            os.makedirs(target_dir, exist_ok=True)
            shutil.move(image_path, os.path.join(target_dir, new_name))

        self.afficher_image()
        
        # Afficher "Fini" et fermer après 1.3 secondes
        finish_window = tk.Toplevel(self)
        finish_window.geometry("200x100")
        finish_window.title("Terminé")
        tk.Label(finish_window, text="Fini!", 
                font=('Helvetica', 16, 'bold')).pack(expand=True)
        self.after(1300, lambda: [finish_window.destroy(), self.destroy()])

if __name__ == "__main__":
    app = Application()
    app.mainloop()