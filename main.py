import os
import tkinter as tk
from PIL import Image, ImageTk

class MAMEApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple MAME Reader")
        self.root.configure(background='black')  # Set background to black
        
        self.roms_directory = r"C:\Users\dani alves\Downloads\mame\roms"
        
        self.games = self.get_game_list()
        self.selected_game_index = None  # Index of the currently selected game
        self.create_ui()

    def get_game_list(self):
        games = []
        for file in os.listdir(self.roms_directory):
            if file.endswith(".zip"):
                games.append(file[:-4])  # Remove ".zip" extension
        return games

    def create_ui(self):
        # Load and display logo image
        logo_image_path = r"ROMS\logo.jpg"  # Replace "logo.jpg" with the path to your logo image
        if os.path.exists(logo_image_path):
            logo_image = Image.open(logo_image_path)
            logo_image = logo_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            self.logo_label = tk.Label(self.root, image=self.logo_photo)
            self.logo_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.fade_in_logo()

    def fade_in_logo(self, alpha=0):
        if alpha < 1:
            alpha += 0.01
            # Generate hexadecimal color code
            color_code = f'#{int(alpha*255):02x}{int(alpha*255):02x}{int(alpha*255):02x}'
            self.logo_label.configure(bg=color_code)
            self.root.after(10, self.fade_in_logo, alpha)
        else:
            self.logo_label.destroy()
            self.show_game_images()  # Delay for 3000 milliseconds (3 seconds) before showing the images

    def show_game_images(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        # Construct the absolute path to the "ROMS" folder
        roms_directory = os.path.join(script_directory, "ROMS")
        image_width = 400  # Width of the image
        gap = 50  # Gap between images
        start_x = self.root.winfo_screenwidth() / 3  # Starting x-coordinate for the first image
        start_y = self.root.winfo_screenheight() / 4  # Starting y-coordinate for the first image
        y = 0  # Starting y-coordinate for the first image
    
    # Highlight the first image by default
        

        for i, game in enumerate(self.games):
            image_path = os.path.join(roms_directory, game + ".jpg")  # Assuming images are JPG format
            print(f"Checking image path for {game}: {image_path}")  # Debugging statement
            if os.path.exists(image_path):
                print(f"Image found for {game}")  # Debugging statement
                image = Image.open(image_path)
                image = image.resize((image_width, image.size[1]))  # Resize only width, keep height
                photo = ImageTk.PhotoImage(image)
                label = tk.Label(self.root, image=photo, bg='black', borderwidth=1, relief="solid", name=f"label{i}")
                print(label)  # Add unique name
                label.image = photo
            # Calculate position for each label
                x = start_x
                y += start_y
                label.place(x=x, y=y)
                label.bind("<Button-1>", lambda event, g=game: self.launch_game(g))  # Bind click event to launch game
                label.bind("<Enter>", lambda event, index=i: self.highlight_game(index))  # Highlight game on mouse hover
            else:
                print(f"Image not found for {game}. Skipping.")
        #self.highlight_game(0)

    def highlight_game(self, index):
        # Remove border from the previously selected game
        if self.selected_game_index is not None:
            previous_label = self.root.nametowidget(f".label{self.selected_game_index}")
            previous_label.config(borderwidth=0)

        # Highlight the currently selected game
        label = self.root.nametowidget(f".label{index}")
        label.config(borderwidth=1, relief="solid")

        self.selected_game_index = index
    
    def launch_game(self, game):
        rom_path = os.path.join(self.roms_directory, game + ".zip")
        command = 'mame -rompath "%s" %s' % (self.roms_directory, game)
        print(command)  # For debugging purposes
        os.system(command)


    def on_key_press(self, event):
        if event.keysym == "Return" and self.selected_game_index is not None:
            self.launch_game(self.games[self.selected_game_index])
        elif event.keysym == "Down":
            if self.selected_game_index is None:
                self.selected_game_index = 0
            elif self.selected_game_index < len(self.games) - 1:
                self.selected_game_index += 1
            self.highlight_game(self.selected_game_index)
        elif event.keysym == "Up":
            if self.selected_game_index is None:
                self.selected_game_index = len(self.games) - 1
            elif self.selected_game_index > 0:
                self.selected_game_index -= 1
            self.highlight_game(self.selected_game_index)

def main():
    root = tk.Tk()
    root.attributes('-fullscreen', True)  # Make the window full-screen
    app = MAMEApp(root)
    root.bind("<KeyPress>", app.on_key_press)  # Bind key press event
    root.mainloop()

if __name__ == "__main__":
    main()
