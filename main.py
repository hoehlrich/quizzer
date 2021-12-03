import tkinter as tk
from tkinter import *

class Question():
    questions = []
    
    class_acronyms = dict()
    teachers = dict()
    unit_topics = dict()
    question_types = dict()
    authors = dict()

    groups = ['class_acronyms', 'teachers', 'unit_topics', 'question_types', 'authors']

    def __init__(self, **kwargs):
        allowed_keys = ['class_acronym', 'teacher', 'unit_topic', 'question_type', 'question', 'question_answer', 'author']
        
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)
        Question.questions.append(self)

        self.question_num = len(Question.questions)
        self.add_question_to_groups()

    def add_question_to_groups(self):
        for k, v in self.__dict__.items():
            plural_k = k + 's'
            if plural_k in Question.groups:
                try:
                    if v not in eval(f"Question.{plural_k}['{v}']"):
                        exec(f"Question.{plural_k}['{v}'].append(self)")
                except:
                    exec(f"Question.{plural_k}['{v}'] = [self]")
                
    def del_question(self):
        Question.questions.remove(self)
        del self

    @classmethod
    def filter_by_attribute(self, **kwargs):
        filtered_questions = []
        
        for question in Question.questions:
            pass_check = True
            for k, v in kwargs.items():
                if getattr(question, k) != v:
                    pass_check = False

            if pass_check == True:
                filtered_questions.append(question)
                

        return filtered_questions

class Deck():
    decks = []

    def __init__(self, cards, name):
        self.cards = list(cards)
        self.name = name
        Deck.decks.append(self)

    def del_deck(self):
        Deck.decks.remove(self)
        del self

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('960x540')
        self.title('quizzer')

        self.columnconfigure(0, weight=1)

        self.light_grey = '#D3D3D3'

        # buttons
        buttons_frame = LabelFrame(self, height=20)
        buttons_frame.pack(side=TOP, fill=X)

        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(5, weight=1)

        btn_decks = Button(buttons_frame, text='Decks', bd=0)
        btn_decks.grid(row=0, column=2, padx=5, pady=5)

        btn_add = Button(buttons_frame, text='Add', bd=0)
        btn_add.grid(row=0, column=3, padx=5, pady=5)

        btn_clear = Button(buttons_frame, text='clear', bd=0)
        btn_clear.grid(row=0, column=4, padx=5, pady=5)

        # btn hover effect
        buttons = [btn_decks, btn_add, btn_clear]

        for btn in buttons:
            btn.bind("<Enter>", self.on_enter)
            btn.bind("<Leave>", self.on_leave)

        # self.mainframe
        self.mainframe = Frame(self)
        self.mainframe.pack(side=TOP)

        btn_decks['command'] = lambda: self.init_deck_screen()
        btn_clear['command'] = lambda: self.init_blank_screen()
        btn_add['command'] = lambda: self.add_question()
    
    def init_deck_screen(self):
        for widget in self.mainframe.winfo_children():
            widget.destroy()
        
        # decklabels
        decklabels_frame = Frame(self.mainframe, width=500, height=50)
        decklabels_frame.pack(side=TOP)

        decklabels_frame.columnconfigure(0, weight=2)
        decklabels_frame.columnconfigure(1, weight=1)
        decklabels_frame.columnconfigure(2, weight=1)

        decklabels_frame.grid_propagate(False)

        Label(decklabels_frame, text='Decks').grid(row=0, column=0, sticky=W, padx=5, pady=5)
        Label(decklabels_frame, text='Cards').grid(row=0, column=1, sticky=W, padx=5, pady=5)
        Label(decklabels_frame, text='inDev').grid(row=0, column=2, sticky=W, padx=5, pady=5)

        # decks
        try:
            for deck in Deck.decks:
                deck_frame = Frame(self.mainframe, width=500, height=22, bg=self.light_grey)
                deck_frame.pack(side=TOP)

                deck_frame.columnconfigure(0, weight=2)
                deck_frame.columnconfigure(1, weight=1)
                deck_frame.columnconfigure(2, weight=1)

                deck_frame.grid_propagate(False)

                btn_deck = Button(deck_frame, text=deck.name, bd=0, bg=self.light_grey, command= lambda: self.init_question_screen(deck))
                btn_deck.grid(row=0, column=0, sticky=W)

                label_cards = Label(deck_frame, text=len(deck.cards), bg=self.light_grey)
                label_cards.grid(row=0, column=1, sticky=W)
        except:
            deck_frame = Frame(self.mainframe, width=500, height=22, bg=self.light_grey)
            deck_frame.pack(side=TOP)

            deck_frame.columnconfigure(0, weight=2)
            deck_frame.columnconfigure(1, weight=1)
            deck_frame.columnconfigure(2, weight=1)

            deck_frame.grid_propagate(False)

            btn_default = Button(deck_frame, text='Default', bd=0, bg=self.light_grey)
            btn_default.grid(row=0, column=0, sticky=W)

    def init_blank_screen(self):
        for widget in self.mainframe.winfo_children():
            widget.destroy()
    
    def init_question_screen(self, deck):
        for widget in self.mainframe.winfo_children():
            widget.destroy()

    def on_enter(self, e):
        e.widget['foreground'] = 'grey'

    def on_leave(self, e):
        e.widget['foreground'] = 'black'

    def add_question(self):

        win = Toplevel(self)

        win.title('Add')
        win.geometry('400x325')

def main():
    q1 = Question(class_acronym='chem', techer='ferrando', unit_topic='periodic table', question_type='basic', question='H', question_answer='Hydrogen', author='Henry Oehlrich')
    q2 = Question(class_acronym='chem', techer='ferrando', unit_topic='periodic table', question_type='basic', question='He', question_answer='Helium', author='Henry Oehlrich')
    q3 = Question(class_acronym='chem', techer='ferrando', unit_topic='periodic table', question_type='basic', question='Li', question_answer='Lithium', author='Henry Oehlrich')
    q4 = Question(class_acronym='chem', techer='ferrando', unit_topic='periodic table', question_type='basic', question='Be', question_answer='Berrylium', author='Henry Oehlrich')
    q5 = Question(class_acronym='chem', techer='ferrando', unit_topic='periodic table', question_type='basic', question='B', question_answer='Boron', author='Henry Oehlrich')
    
    Deck([q1, q2, q3], 'test1')
    Deck([q1, q2, q3, q4], 'test2')
    Deck([q1, q2, q3, q4, q5], 'test3')

    app = App()
    mainloop()

if __name__ == '__main__':
    main()