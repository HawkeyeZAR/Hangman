"""
Hangman Game created using python.

Created by Jack Ackermann
"""

from tkinter import Tk, ttk, Frame, FALSE, Canvas, Button, Entry, StringVar, \
     Label, messagebox
import random


class HangMan(Frame):
    def centre_window(self):
        '''
        Create frame size and center frame to the middle of the screen
        '''
        w = 320
        h = 580
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def __init__(self, parent, *args, **kwargs):
        '''
        Initialize variables and widgets
        '''
        Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.root.title('  HangMan  - Python3')
        self.centre_window()
        self.grid(column=0, row=0, sticky='nsew',  padx=0,  pady=0)
        # list of variables used
        self.word_list = []
        self.random_word = ''
        self.hash_string = ''
        self.guess_counter = 0
        self.guessed_letters = ''
        # Load the screen widgets onto canvas
        self.create_word_list()
        self.load_widgets()

    def load_widgets(self):
        ''' All widgets go under here '''
        self.canvas = Canvas(self, width=316, height=520, background='cyan2')
        self.canvas.grid(column=0, row=0)
        # create word_entry widget
        self.word = StringVar()
        self.word_entry = Entry(self, textvariable=self.word, state='readonly')
        self.word_entry.config(justify='center', width=16, font='Times 14 bold')
        self.word_entry.grid(column=0, row=1)
        # The current guess letter section
        self.guess_var = StringVar()
        self.guess_entry = Entry(self, textvariable=self.guess_var)
        self.guess_entry.config(state='readonly',  width=2, justify='center')
        self.guess_entry.grid(column=0, row=1, sticky='E', padx=55)
        self.guess_entry.bind('<Return>', self.check_guess)
        # The used letters section from all guesses
        self.used_char = StringVar()
        self.guessed_entry = Entry(self, textvariable=self.used_char,
                                   state='readonly')
        self.guessed_entry.config(justify='center', width=16,
                                  font="Times 14 bold")
        self.guessed_entry.grid(column=0, row=2)
        # create Labels
        self.word_label = Label(self, text='Hashed Word: ')
        self.word_label.grid(column=0, row=1, sticky='W')
        # create button Widgets
        self.check = Button(self, text='Check ', command=self.check_guess)
        self.check.config(state='disabled')
        self.check.grid(column=0, row=1, sticky='E')
        self.start = Button(self, text='  Start  ', command=self.start_game)
        self.start.grid(column=0, row=2, sticky='SW')
        self.exit_btn = Button(self, text='  Exit  ', command=self.on_exit)
        self.exit_btn.grid(column=0, row=2, sticky='SE')

    def start_game(self):
        '''
        Starts the game or starts a new game when round is over
        Make sure canvas is cleared when new round starts.
        Enable guess button and entry widget.
        Set random word and hashed word and length
        '''
        self.canvas.delete("all")
        self.guess_counter = 0
        self.guess_entry.config(state='normal')
        self.check.config(state='normal')
        self.random_word = random.choice(self.word_list).strip()
        self.hash_string = len(self.random_word) * '#'
        self.word.set(self.hash_string)
        self.hashes_left = self.hash_string.count('#')
        self.used_char.set('')
        self.guessed_letters = ''
        self.guess_var.set('')

    def draw_body_parts(self):
        ''' Draw body part for every failed guess attempt '''
        if self.guess_counter == 1:
            self.gallow()
        elif self.guess_counter == 2:
            self.body()
        elif self.guess_counter == 3:
            self.left_leg()
            self.left_foot()
        elif self.guess_counter == 4:
            self.right_leg()
            self.right_foot()
        elif self.guess_counter == 5:
            self.left_arm()
            self.left_hand()
        elif self.guess_counter == 6:
            self.right_arm()
            self.right_hand()
        elif self.guess_counter == 7:
            self.head()
            self.canvas.create_text(150, 290, text='Game\nOver!',
                                    fill='red', font='Bold 56')
            # Disables Guess button and entry field if game over
            self.guess_entry.config(state='readonly')
            self.check.config(state='disabled')

    def validate_guess(self, guess):
        '''
        Check if Guess is in the word
        If guess is not in word, increase guess_counter
        Then call the draw_body_parts function
        Update the original hash string to include correct letters
        Check if player wins
        '''
        tmp_str = ''
        count_hash = self.hash_string.count('#')
        for r, h in zip(self.random_word, self.hash_string):
            if r == guess:
                tmp_str += guess
                # if final letter was guessed correctly, you win
                if count_hash == 1:
                    self.canvas.create_text(150, 290, text='You Win',
                                    fill='red', font='Bold 56')
            else:
                tmp_str += h
        if count_hash == tmp_str.count('#'):
            self.guess_counter += 1
            self.draw_body_parts()
        self.word.set(tmp_str)
        self.hash_string = self.word.get()

    def check_guess(self, event=None):
        ''' Checks to see if the entered guess is valid '''
        guess = self.guess_entry.get()
        if len(guess) > 1:
            msg = "You can only guess one letter at a time, please retry"
            messagebox.showinfo('Too many letters', msg)
        else:
            if guess.isalpha() is True:
                self.guessed_letters += guess
                self.validate_guess(guess)
            else:
                messagebox.showinfo('Not a letter', 'Only letters allowed')
        self.used_char.set(self.guessed_letters)

    def create_word_list(self):
        ''' Creates a list of words from a dictionery file '''
        with open('words.txt', "r") as file:
            data = file.readlines()
            for d in data:
                self.word_list.append(d)

    def gallow(self):
        ''' Draws the gallow onto the screen '''
        gallow_coord = [[75, 28, 75, 518],
                        [200, 28, 200, 115],
                        [72, 25, 203, 25],
                        [20, 515, 270, 515],
                        [178, 25, 75, 128]]
        for g in gallow_coord:
            self.canvas.create_line(g, fill="black", width='6')

    def head(self):
        ''' Draws the head onto the screen '''
        head_coord = [[160, 110, 240, 212]]
        head_coord2 = [[198, 212, 198, 240],
                       [202, 212, 202, 240],
                       [176, 145, 195, 145],
                       [207, 145, 225, 145],
                       [216, 135, 216, 154],
                       [185, 135, 185, 154],
                       [185, 180, 216, 180]]
        for h in head_coord:
            self.canvas.create_oval(h, fill="lime", outline="blue", width='2')
        for h in head_coord2:
            self.canvas.create_line(h, fill="black", width='6')

    def body(self):
        ''' Draws the body onto the screen '''
        self.canvas.create_oval(140, 240, 260, 420, fill="lime",
                                outline="blue", width='2')

    def left_arm(self):
        ''' Draws the left_arm onto the screen '''
        self.canvas.create_line(175, 265, 135, 370, fill="black", width='6')

    def right_arm(self):
        ''' Draws right_arm onto the screen '''
        self.canvas.create_line(225, 265, 265, 370, fill="black", width='6')

    def left_leg(self):
        ''' Draws the left_leg onto the screen '''
        self.canvas.create_line(180, 400, 180, 485, fill="black", width='6')

    def right_leg(self):
        ''' Draws the right_leg onto the screen '''
        self.canvas.create_line(220, 400, 220, 485, fill="black", width='6')

    def left_hand(self):
        ''' Draws the left_hand onto the screen '''
        self.canvas.create_line(115, 365, 137, 370, fill="black", width='6')

    def right_hand(self):
        ''' Draws the right_hand onto the screen '''
        self.canvas.create_line(265, 367, 280, 360, fill="black", width='6')

    def left_foot(self):
        ''' Draws the left_foot onto the screen '''
        self.canvas.create_line(160, 485, 183, 485, fill="black", width='6')

    def right_foot(self):
        ''' Draws the right_foot onto the screen '''
        self.canvas.create_line(217, 485, 240, 485, fill="black", width='6')

    # Exit the program. Linked to the Exit Button
    def on_exit(self):
        self.root.destroy()


def main():
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    HangMan(root)
    root.mainloop()

if __name__ == '__main__':
    main()
