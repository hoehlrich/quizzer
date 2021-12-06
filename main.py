from json.decoder import JSONDecodeError
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
import json

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
    
    @classmethod
    def export_dict(self):
        d = {}
        for i, question in enumerate(self.questions):
            d[i] = [question.class_acronym, question.teacher, question.unit_topic, question.question_type, question.question, question.question_answer, question.author]
        
        return d

    @classmethod
    def read_questions(self, _file):
        try:
            with open(_file, 'r') as questionfile:
                questions = json.load(questionfile)
        except json.decoder.JSONDecodeError or FileNotFoundError:
            questions = dict()
        
        for question in questions.values():
            Question(class_acronym=question[0], teacher=question[1], unit_topic=question[2], question_type=question[3], question=question[4], question_answer=question[5], author=question[6])
    
    @classmethod
    def write_questions(self, _file):
        d = self.export_dict()
        with open(_file, 'w') as questionfile:
            questionfile.write(json.dumps(d))


class Deck():
    decks = []

    def __init__(self, cards, name):
        try:
            self.cards = list(cards)
        except TypeError:
            self.cards = list()

        self.name = name
        Deck.decks.append(self)
    
    def add_card(self, card):
        self.cards.append(card)

    def del_deck(self):
        Deck.decks.remove(self)
        del self

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('960x540')
        self.title('quizzer')

        self.questions_file = 'questions.json'

        self.columnconfigure(0, weight=1)

        self.light_grey = '#D3D3D3'
        self.defaultbg = self.cget('bg')

        self.init_main_buttons()

        # self.mainframe
        self.mainframe = Frame(self)
        self.mainframe.pack(side=TOP, fill=BOTH)

        self.init_deck_screen()
    
    def init_main_buttons(self):
        # buttons
        buttons_frame = LabelFrame(self, height=20)
        buttons_frame.pack(side=TOP, fill=X)

        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(5, weight=1)

        btn_decks = Button(buttons_frame, text='Decks', bd=0, command=self.init_deck_screen)
        btn_decks.grid(row=0, column=2, padx=5, pady=5)

        btn_add = Button(buttons_frame, text='Add', bd=0, command=self.add_question)
        btn_add.grid(row=0, column=3, padx=5, pady=5)

        btn_save = Button(buttons_frame, text='Save', bd=0, command= lambda: Question.write_questions(self.questions_file))
        btn_save.grid(row=0, column=4, padx=5, pady=5)

        # btn hover effect
        buttons = [btn_decks, btn_add, btn_save]

        for btn in buttons:
            btn.bind("<Enter>", self.on_enter)
            btn.bind("<Leave>", self.on_leave)

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
            for i, deck in enumerate(Deck.decks):
                if i % 2 == 0:
                    bg = self.light_grey
                else:
                    bg = self.defaultbg

                deck_frame = Frame(self.mainframe, width=500, height=22, bg=bg)
                deck_frame.pack(side=TOP)

                deck_frame.columnconfigure(0, weight=2)
                deck_frame.columnconfigure(1, weight=1)
                deck_frame.columnconfigure(2, weight=1)

                deck_frame.grid_propagate(False)

                btn_deck = Button(deck_frame, text=deck.name, bd=0, bg=bg, command= lambda: self.init_question_screen(deck))
                btn_deck.grid(row=0, column=0, sticky=W)

                label_cards = Label(deck_frame, text=len(deck.cards), bg=bg)
                label_cards.grid(row=0, column=1, sticky=W)
        except:
            deck_frame = Frame(self.mainframe, width=500, height=22, bg=bg)
            deck_frame.pack(side=TOP)

            deck_frame.columnconfigure(0, weight=2)
            deck_frame.columnconfigure(1, weight=1)
            deck_frame.columnconfigure(2, weight=1)

            deck_frame.grid_propagate(False)

            btn_default = Button(deck_frame, text='Default', bd=0, bg=self.light_grey)
            btn_default.grid(row=0, column=0, sticky=W)
        
        # bottom buttons
        btn_frame = Frame(self.mainframe, width=300, height=24)
        btn_frame.pack(side=BOTTOM, anchor=S, padx=2, pady=2)

        Button(btn_frame, text='Create Deck', bg=self.light_grey).grid(row=0, column=0, padx=2, pady=2)
        Button(btn_frame, text='Import File', bg=self.light_grey, command=self.upload_file).grid(row=0, column=1, padx=2, pady=2)
        Button(btn_frame, text='Test', bg=self.light_grey).grid(row=0, column=2, padx=2, pady=2)


    def init_blank_screen(self):
        for widget in self.mainframe.winfo_children():
            widget.destroy()
    
    def init_question_screen(self, deck):
        def space_clicked(event):
            if question.get() == 'That was the last card!':
                self.init_deck_screen()

            if self.answer_showed == False:
                show_answer()
            else:
                try:
                    question_frame.winfo_children()[1].destroy()
                    
                    self.answer_showed = False
                    self.current_question = deck.cards[deck.cards.index(self.current_question) + 1]
                    question.set(self.current_question.question)
                except IndexError:
                    question.set('That was the last card!')
            

        
        def show_answer():
            try:
                Label(question_frame, text=self.current_question.question_answer).pack()
                self.answer_showed = True
            except TclError:
                pass

        for widget in self.mainframe.winfo_children():
            widget.destroy()

        question_frame = Frame(self.mainframe)
        question_frame.pack(side=TOP)

        self.bind('<space>', space_clicked)
        
        self.answer_showed = False
        self.current_question = deck.cards[0]
        
        question = StringVar()
        question.set(self.current_question.question)

        Label(question_frame, textvariable=question).pack()

            

    def on_enter(self, e):
        e.widget['foreground'] = 'grey'

    def on_leave(self, e):
        e.widget['foreground'] = 'black'

    def add_question(self):
        def add():
            question = Question(class_acronym=str(class_acronym.get()), teacher=str(teacher.get()), unit_topic=str(unit_topic.get()), question_type=str(self.adding_type), question=str(front_text.get()), question_answer=str(back_text.get()), author=str(author.get()))
            self.adding_to_deck.add_card(question)
            win.destroy()
            
        # win init and config
        win = Toplevel(self)

        win.title('Add')
        win.geometry('400x325')
        
        win.resizable(False, True)


        # upper_frame
        upper_frame = Frame(win, width=400, height=50)
        upper_frame.pack(side=TOP)

        upper_frame.grid_propagate(False)
        
        # StringVar init
        self.adding_type_text = StringVar()
        self.adding_type_text.set('Click to Set')

        self.adding_to_deck_text = StringVar()
        self.adding_to_deck_text.set('Click to Set')

        label_type = Label(upper_frame, text='Type', width=5)
        label_type.grid(row=0, column=0, padx=2, pady=2)

        btn_type = Button(upper_frame, textvariable=self.adding_type_text, width=20, bd=0, bg=self.light_grey, command=self.choose_type)
        btn_type.grid(row=0, column=1, padx=5, pady=5)

        label_deck = Label(upper_frame, text='Deck', width=5)
        label_deck.grid(row=0, column=2, padx=2, pady=2)

        btn_deck = Button(upper_frame, textvariable=self.adding_to_deck_text, width=19, bd=0, bg=self.light_grey, command=self.choose_deck)
        btn_deck.grid(row=0, column=3, padx=5, pady=5)

        # front_frame
        front_frame = Frame(win, width=400, height=100)
        front_frame.pack(side=TOP, padx=5, pady=5)

        front_frame.grid_propagate(False)
        
        front_text = StringVar()

        Label(front_frame, text='Front').pack(side=TOP, anchor=W, padx=2, pady=1)
        entry_front = Entry(front_frame, textvariable=front_text, width=62, background='white')
        entry_front.pack(side=TOP, fill=BOTH, padx=2, ipady=7)
        
        entry_front.focus_set()

        # back_frame
        back_frame = Frame(win, width=400, height=100)
        back_frame.pack(side=TOP, padx=5, pady=5)

        back_frame.grid_propagate(False)
        
        back_text = StringVar()
        
        Label(back_frame, text='Back').pack(side=TOP, anchor=W, padx=2, pady=1)
        entry_back = Entry(back_frame, textvariable=back_text, width=62, background='white')
        entry_back.pack(side=TOP, fill=BOTH, padx=2, ipady=7)

        # info_frame
        info_frame = Frame(win, width=400, height=100)
        info_frame.pack(side=TOP, padx=5, pady=5)

        info_frame.grid_propagate(False)

        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=1)
        info_frame.columnconfigure(2, weight=1)
        info_frame.columnconfigure(3, weight=1)

        class_acronym = StringVar()
        teacher = StringVar()
        unit_topic = StringVar()
        author = StringVar()

        Label(info_frame, text='Class').grid(row=0, column=0, padx=2, pady=2)
        Label(info_frame, text='Teacher').grid(row=0, column=1, padx=2, pady=2)
        Label(info_frame, text='Unit').grid(row=0, column=2, padx=2, pady=2)
        Label(info_frame, text='Author').grid(row=0, column=3, padx=2, pady=2)

        Entry(info_frame, textvariable=class_acronym).grid(row=1, column=0, padx=2, pady=2)
        Entry(info_frame, textvariable=teacher).grid(row=1, column=1, padx=2, pady=2)
        Entry(info_frame, textvariable=unit_topic).grid(row=1, column=2, padx=2, pady=2)
        Entry(info_frame, textvariable=author).grid(row=1, column=3, padx=2, pady=2)

        # buttons
        Button(win, text='Cancel', command=win.destroy).pack(side=RIGHT, anchor=S, padx=2, pady=2)
        Button(win, text='Add', command=add).pack(side=RIGHT, anchor=S, padx=2, pady=2)

    def choose_type(self):
        
        def choose(question_type):
            win.destroy()

            self.adding_type = question_type
            self.adding_type_text.set(question_type)

        win = Toplevel(self)

        win.title('Choose Type')
        win.geometry('300x245')
        win.resizable(False, False)
        
        button_frame = Frame(win)
        button_frame.pack(side=BOTTOM, fill=BOTH, padx=5, pady=5)

        btn_choose = Button(button_frame, text='Choose', bd=1, command= lambda: choose(list(Question.question_types.keys())[listbox.curselection()[0]]))
        btn_choose.grid(row=0, column=0, sticky=E, padx=5, pady=5)

        listbox_frame = Frame(win, height=225, bg='white')
        listbox_frame.pack(side=TOP, fill=BOTH, padx=5, pady=5)

        listbox = Listbox(listbox_frame, height=230)

        for i, question_type in enumerate(Question.question_types.keys()):
            listbox.insert(i, question_type)
        
        listbox.pack(side=TOP, fill=BOTH)

    def choose_deck(self):
        
        def choose(deck):
            win.destroy()
            self.adding_to_deck = deck

            self.adding_to_deck_text.set(deck.name)
        
        def add():
            
            def ok():
                Deck(None, deck_name.get())
                add_win.destroy()
                win.destroy()
                self.choose_deck()

            add_win = Toplevel(self)
            add_win.title('Add Deck')
            add_win.geometry('300x80')
            
            deck_name = StringVar()

            Label(add_win, text='New deck name:').pack(side=TOP, anchor=W, padx=2, pady=2)
            Entry(add_win, textvariable=deck_name, width=290).pack(side=TOP, anchor=W, padx=5, pady=2)
            Button(add_win, text='Cancel', command=add_win.destroy).pack(side=RIGHT, anchor=S, padx=2, pady=2)
            Button(add_win, text='Ok', command=ok).pack(side=RIGHT, anchor=S, padx=2, pady=2)

        win = Toplevel(self)

        win.title('Choose Deck')
        win.geometry('300x245')
        win.resizable(False, False)
        
        button_frame = Frame(win)
        button_frame.pack(side=BOTTOM, fill=BOTH, padx=5, pady=5)

        btn_add = Button(button_frame, text='Add', bd=1, command= add)
        btn_add.grid(row=0, column=1, sticky=E, padx=5, pady=5)

        btn_choose = Button(button_frame, text='Choose', bd=1, command= lambda: choose(Deck.decks[listbox.curselection()[0]]))
        btn_choose.grid(row=0, column=0, sticky=E, padx=5, pady=5)

        listbox_frame = Frame(win, height=225, bg='white')
        listbox_frame.pack(side=TOP, fill=BOTH, padx=5, pady=5)

        listbox = Listbox(listbox_frame, height=230)

        for i, deck in enumerate(Deck.decks):
            listbox.insert(i, deck.name)
        
        listbox.pack(side=TOP, fill=BOTH)

    def upload_file(self):
        filename = filedialog.askopenfilename()
        
        if '.json' in filename:
            Question.read_questions(filename)
        else:
            messagebox.showerror('Import Error', 'Invalid File.')

        

def main():
    Question.read_questions('questions.json')
    
    q1 = Question.questions[0]
    q2 = Question.questions[1]
    q3 = Question.questions[2]
    q4 = Question.questions[3]
    q5 = Question.questions[4]

    Deck([q1, q2, q3], 'test1')
    Deck([q1, q2, q3, q4], 'test2')
    Deck([q1, q2, q3, q4, q5], 'test3')

    app = App()
    mainloop()

    Question.write_questions('questions.json')
    

if __name__ == '__main__':
    main()