import sys
import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import tkinter.font as tkFont
import pygetwindow as gw
import ctypes
import time
import inspect

try:
    import win32com.client as win32
except ImportError:
    win32 = None

# --- IMPORTY TWOICH NOWYCH MODUŁÓW ---
from config_db import create_connection, SQL, cfg_get, cfg_getbool
from models_specs import SECTION_SPECS, FieldSpec
from ui_dialogs import DialogsMixin
from app_crud_dodaj import DodajMixin
from app_crud_pobierz import PobierzMixin
from app_crud_usun import UsunMixin
from app_crud_edytuj_sprzet import EdytujSprzetMixin
from app_crud_edytuj_akcesoria import EdytujAkcesoriaMixin
from app_crud_edytuj_uzytkownik import EdytujUzytkownikMixin
from app_przypisywanie import PrzypisywanieMixin


# --- GŁÓWNA KLASA APLIKACJI ---
class Application(
    tk.Tk,
    DialogsMixin,
    DodajMixin,
    PobierzMixin,
    UsunMixin,
    EdytujSprzetMixin,
    EdytujAkcesoriaMixin,
    EdytujUzytkownikMixin,
    PrzypisywanieMixin
):
    def __init__(self):
        super().__init__()
        self.state('zoomed')
        self.title('mSprzęt v.2.0.1')
        self.geometry('1200x800')
        self.open_windows = []

        self.currently_selected_tree = None
        self.currently_selected_item = None
        self.result_count_var = {}

        if sys.platform.startswith('win'):
            try:
                self.iconbitmap('app.ico')
            except Exception:
                pass
        else:
            try:
                img = PhotoImage(file='app.png')
                self.iconphoto(True, img)
            except Exception:
                pass

        # Tworzenie interfejsu
        self.create_widgets()

        self.bind('<Insert>', self.search_user_function)
        self.bind('<Unmap>', self.on_minimize)
        self.bind('<Map>', self.on_restore)

    def update_result_count(self, section, table):
        try:
            n = len(table.get_children())
            if section in self.result_count_var:
                self.result_count_var[section].set(f'Wyniki: {n}')
        except Exception:
            pass

    def generuj_oswiadczenie_laptop(self):
        try:
            from document_generation_v2 import generuj_oswiadczenie_laptop as _gen
            return _gen(self, create_connection=create_connection, SQL=SQL)
        except ImportError:
            messagebox.showerror("Błąd", "Brak pliku document_generation_v2.py")

    def generuj_protokol_odbioru(self):
        try:
            from document_generation_v2 import generuj_protokol_odbioru as _gen
            return _gen(self, create_connection=create_connection, SQL=SQL)
        except ImportError:
            messagebox.showerror("Błąd", "Brak pliku document_generation_v2.py")

    def on_minimize(self, event):
        if self.state() == 'iconic':
            for window in self.open_windows:
                window.withdraw()

    def on_restore(self, event):
        for window in self.open_windows:
            window.deiconify()

    def search_user_function(self, event):
        self.show_frame('UŻYTKOWNIK')
        self.search_user()
        self.update_right_buttons('UŻYTKOWNIK')

    def copy_to_clipboard(self, value):
        self.clipboard_clear()
        self.clipboard_append(value)
        self.update()

    def create_context_menu(self, table):
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label='Kopiuj', command=lambda: self.copy_selected_item(table))
        return context_menu

    def copy_selected_item(self, table):
        selected_items = table.selection()
        if selected_items:
            headers = [table.heading(col)['text'] for col in table['columns']]
            headers_text = '\t'.join(headers)
            rows_text = ''
            for item in selected_items:
                item_values = table.item(item, 'values')
                values_text = '\t'.join(item_values)
                rows_text += values_text + '\n'
            full_text = headers_text + '\n' + rows_text
            self.copy_to_clipboard(full_text.strip())

    def show_context_menu(self, event, table):
        self.context_menu_event = event
        context_menu = self.create_context_menu(table)
        context_menu.post(event.x_root, event.y_root)

    def update_column_widths(self, table, section):
        column_widths = {
            'LAPTOPY': {'STATUS': 200, 'NR SRODKA TRWALEGO': 150, 'NAZWA LAPTOPA': 150, 'NR SERYJNY': 150, 'MODEL': 150,
                        'NR SDJ': 100, 'UWAGI': 250, 'NR KADROWY': 150, 'IMIE': 100, 'NAZWISKO': 100},
            'MONITORY': {'STATUS': 100, 'NR SERYJNY': 150, 'MODEL': 200, 'NR SDJ': 100, 'UWAGI': 250, 'NR KADROWY': 150,
                         'IMIE': 100, 'NAZWISKO': 100},
            'TELEFONY': {'STATUS': 100, 'IMEI': 150, 'LADOWARKA': 100, 'KABEL \nUSB C': 70,
                         'LADOWARKA \nINDUKCYJNA': 100, 'PRZEJSCIOWKA \nDO TELEFONU': 100, 'ETUI': 50,
                         'NR TELEFONU': 150, 'MODEL': 150, 'NR SDJ': 100, 'UWAGI': 250, 'NR KADROWY': 150, 'IMIE': 100,
                         'NAZWISKO': 100},
            'SŁUCHAWKI': {'STATUS': 100, 'NR SERYJNY': 150, 'MODEL': 200, 'NR SDJ': 100, 'UWAGI': 250,
                          'NR KADROWY': 150, 'IMIE': 100, 'NAZWISKO': 100},
            'KARTY SIM': {'STATUS': 100, 'NR TELEFONU': 150, 'NR SIM': 150, 'OPERATOR': 150, 'NR SDJ': 100,
                          'UWAGI': 250, 'NR KADROWY': 150, 'IMIE': 100, 'NAZWISKO': 100},
            'ROUTER': {'STATUS': 100, 'IMEI': 150, 'NR TELEFONU': 150, 'NR SIM': 150, 'OPERATOR': 150, 'NR SDJ': 100,
                       'UWAGI': 250, 'NR KADROWY': 150, 'IMIE': 100, 'NAZWISKO': 100},
            'MYSZKI': {'STATUS': 100, 'NR SDJ': 100, 'UWAGI': 250, 'NR KADROWY': 150, 'IMIE': 100, 'NAZWISKO': 100},
            'KLAWIATURY': {'STATUS': 100, 'NR SDJ': 100, 'UWAGI': 250, 'NR KADROWY': 150, 'IMIE': 100, 'NAZWISKO': 100},
            'KONTA UŻYTKOWNIKÓW': {'NR KADROWY': 150, 'IMIE': 100, 'NAZWISKO': 100, 'RODZAJ ZATRUDNIENIA': 150,
                                   'LOKALIZACJA': 150, 'ID_UZYTKOWNIKA': 100}
        }
        if section in column_widths:
            for col in table['columns']:
                if col in column_widths[section]:
                    table.column(col, width=column_widths[section][col], anchor='center')

    def create_widgets(self):
        self.top_frame = tk.Frame(self, bg='lightgray', width=800, height=100)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)
        buttons_top = ['UŻYTKOWNIK', 'LAPTOPY', 'MONITORY', 'TELEFONY', 'SŁUCHAWKI', 'KARTY SIM', 'ROUTER', 'MYSZKI',
                       'KLAWIATURY', 'KONTA UŻYTKOWNIKÓW']
        for btn_text in buttons_top:
            btn = tk.Button(self.top_frame, text=btn_text, command=lambda text=btn_text: self.show_frame(text))
            btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.search_user_frame = tk.Frame(self, bg='lightgray', width=800, height=50)
        self.search_user_frame.pack(side=tk.TOP, fill=tk.X)
        search_user_button = tk.Button(self.search_user_frame, text='Znajdź UŻYTKOWNIKa', command=self.search_user)
        search_user_button.grid(row=0, column=0, padx=10, pady=10)

        self.user_info_frame = tk.Frame(self.search_user_frame, bg='lightgray')
        self.user_info_frame.grid(row=0, column=1, padx=10, pady=10)
        self.user_labels = {}
        self.user_values = {}
        labels = ['NR KADROWY', 'IMIE', 'NAZWISKO', 'RODZAJ ZATRUDNIENIA', 'LOKALIZACJA', 'ID_UZYTKOWNIKA']
        for i, label_text in enumerate(labels):
            value_label = tk.Label(self.user_info_frame, text='', anchor='w', bg='lightgray', fg='red',
                                   font='Helvetica 11 bold')
            value_label.grid(row=0, column=i, padx=10)
            self.user_values[label_text] = value_label

        self.frames = {}
        for section in buttons_top:
            self.frames[section] = tk.Frame(self, width=600, height=500)
            self.frames[section].pack_propagate(0)

        self.right_frame = tk.Frame(self, bg='lightblue', width=160)
        self.right_frame.pack_propagate(False)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.right_canvas = tk.Canvas(self.right_frame, bg='lightblue', highlightthickness=0)
        self.right_scrollbar = ttk.Scrollbar(self.right_frame, orient='vertical', command=self.right_canvas.yview)
        self.right_scrollable_frame = tk.Frame(self.right_canvas, bg='lightblue')
        self.right_scrollable_frame.bind('<Configure>', lambda e: self.right_canvas.configure(
            scrollregion=self.right_canvas.bbox('all')))
        self.right_canvas.create_window((0, 0), window=self.right_scrollable_frame, anchor='nw')
        self.right_canvas.configure(yscrollcommand=self.right_scrollbar.set)
        self.right_canvas.pack(side='left', fill='y')
        self.right_scrollbar.pack(side='right', fill='y')

        # SLOWNIK BEZ NAWIASOW () NA KONCU FUNKCJI
        self.right_buttons = {
            'UŻYTKOWNIK': [
                ('EDYTUJ', self.edit_user_record_specific),
                ('WYŚLIJ MAIL', self.generate_user_email),
                ('PRZYPISZ LAPTOPA', self.przypisz_laptopa_w_sekcji_uzytkownik),
                ('PRZYPISZ MONITOR', self.przypisz_monitor_w_sekcji_uzytkownik),
                ('PRZYPISZ TELEFON', self.przypisz_telefon_w_sekcji_uzytkownik),
                ('PRZYPISZ SŁUCHAWKI', self.przypisz_sluchawki_w_sekcji_uzytkownik),
                ('PRZYPISZ KARTE SIM', self.przypisz_karte_sim_w_sekcji_uzytkownik),
                ('PRZYPISZ ROUTER', self.przypisz_router_w_sekcji_uzytkownik),
                ('PRZYPISZ MYSZKE', self.przypisz_myszke_w_sekcji_uzytkownik),
                ('PRZYPISZ KLAWIATURE', self.przypisz_klawiature_w_sekcji_uzytkownik)
            ],
            'LAPTOPY': [('DODAJ', self.action22), ('EDYTUJ', self.action4), (' USUŃ ', self.action5),
                        ('POBIERZ DANE', self.action6)],
            'MONITORY': [('DODAJ', self.action23), ('EDYTUJ', self.action24), (' USUŃ ', self.action25),
                         ('POBIERZ DANE', self.action26)],
            'TELEFONY': [('DODAJ', self.dodaj_telefon), ('EDYTUJ', self.action4), (' USUŃ ', self.usun_telefon),
                         ('POBIERZ DANE', self.action6)],
            'SŁUCHAWKI': [('DODAJ', self.dodaj_sluchawki), ('EDYTUJ', self.action4), ('USUŃ', self.usun_sluchawki),
                          ('POBIERZ DANE', self.action6)],
            'KARTY SIM': [('DODAJ', self.dodaj_karty_sim), ('EDYTUJ', self.action4), ('USUŃ', self.usun_karte_sim),
                          ('POBIERZ DANE', self.action6)],
            'ROUTER': [('DODAJ', self.dodaj_router), ('EDYTUJ', self.action4), ('USUŃ', self.usun_router),
                       ('POBIERZ DANE', self.action6)],
            'MYSZKI': [('DODAJ', self.dodaj_myszke), ('EDYTUJ', self.action4), ('USUŃ', self.usun_myszke),
                       ('POBIERZ DANE', self.action6)],
            'KLAWIATURY': [('DODAJ', self.dodaj_klawiature), ('EDYTUJ', self.action4), ('USUŃ', self.usun_klawiature),
                           ('POBIERZ DANE', self.action6)],
            'KONTA UŻYTKOWNIKÓW': [('DODAJ', self.action27), ('EDYTUJ', self.action4),
                                   (' USUŃ ', self.usun_konto_uzytkownika)]
        }

        self.current_section = None
        self.current_section_label = None
        self.update_right_buttons(buttons_top[0])

        self.tabela = ttk.Treeview(self.frames['LAPTOPY'],
                                   columns=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'NR SRODKA TRWALEGO',
                                            'NAZWA LAPTOPA', 'NR SERYJNY', 'MODEL', 'NR SDJ', 'UWAGI', 'ID'],
                                   show='headings')
        self.tabela.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frames['LAPTOPY'].rowconfigure(0, weight=1)
        self.frames['LAPTOPY'].columnconfigure(0, weight=1)

        self.tabela_monitory = ttk.Treeview(self.frames['MONITORY'],
                                            columns=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'NR SERYJNY', 'MODEL',
                                                     'NR SDJ', 'UWAGI', 'ID'], show='headings')
        self.tabela_monitory.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frames['MONITORY'].rowconfigure(0, weight=1)
        self.frames['MONITORY'].columnconfigure(0, weight=1)

        self.tabela_telefony = ttk.Treeview(self.frames['TELEFONY'],
                                            columns=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'IMEI', 'LADOWARKA',
                                                     'KABEL \nUSB C', 'LADOWARKA INDUKCYJNA',
                                                     'PRZEJSCIOWKA DO TELEFONU', 'ETUI', 'NR TELEFONU', 'MODEL',
                                                     'NR SDJ', 'UWAGI', 'ID'], show='headings')
        self.tabela_telefony.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frames['TELEFONY'].rowconfigure(0, weight=1)
        self.frames['TELEFONY'].columnconfigure(0, weight=1)

        self.tabela_sluchawki = ttk.Treeview(self.frames['SŁUCHAWKI'],
                                             columns=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'NR SERYJNY', 'MODEL',
                                                      'NR SDJ', 'UWAGI', 'ID'], show='headings')
        self.tabela_sluchawki.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frames['SŁUCHAWKI'].rowconfigure(0, weight=1)
        self.frames['SŁUCHAWKI'].columnconfigure(0, weight=1)

        self.tabela_karty_sim = ttk.Treeview(self.frames['KARTY SIM'],
                                             columns=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'NR TELEFONU',
                                                      'NR SIM', 'OPERATOR', 'NR SDJ', 'UWAGI', 'ID'], show='headings')
        self.tabela_karty_sim.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frames['KARTY SIM'].rowconfigure(0, weight=1)
        self.frames['KARTY SIM'].columnconfigure(0, weight=1)

        self.tabela_router = ttk.Treeview(self.frames['ROUTER'],
                                          columns=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'IMEI', 'NR TELEFONU',
                                                   'NR SIM', 'OPERATOR', 'NR SDJ', 'UWAGI', 'ID'], show='headings')
        self.tabela_router.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frames['ROUTER'].rowconfigure(0, weight=1)
        self.frames['ROUTER'].columnconfigure(0, weight=1)

        self.tabela_myszki = ttk.Treeview(self.frames['MYSZKI'],
                                          columns=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'NR SDJ', 'UWAGI', 'ID'],
                                          show='headings')
        self.tabela_myszki.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frames['MYSZKI'].rowconfigure(0, weight=1)
        self.frames['MYSZKI'].columnconfigure(0, weight=1)

        self.tabela_klawiatury = ttk.Treeview(self.frames['KLAWIATURY'],
                                              columns=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'NR SDJ', 'UWAGI',
                                                       'ID'], show='headings')
        self.tabela_klawiatury.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frames['KLAWIATURY'].rowconfigure(0, weight=1)
        self.frames['KLAWIATURY'].columnconfigure(0, weight=1)

        self.tabela_konta = ttk.Treeview(self.frames['KONTA UŻYTKOWNIKÓW'],
                                         columns=['NR KADROWY', 'IMIE', 'NAZWISKO', 'RODZAJ ZATRUDNIENIA',
                                                  'LOKALIZACJA', 'ID_UZYTKOWNIKA'], show='headings')
        self.tabela_konta.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frames['KONTA UŻYTKOWNIKÓW'].rowconfigure(0, weight=1)
        self.frames['KONTA UŻYTKOWNIKÓW'].columnconfigure(0, weight=1)

    def prevent_hide_item_selection(self, event):
        item_id = self.tabela.identify_row(event.y)
        if item_id and 'hide' in self.tabela.item(item_id, 'tags'):
            return 'break'

    def show_frame(self, section):
        if section == 'UŻYTKOWNIK':
            self.search_user_frame.pack(side=tk.TOP, fill=tk.X)
            self.reset_user_info()
        else:
            self.search_user_frame.pack_forget()
        self.current_section = section
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[section].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.populate_frame_with_data(section)

    def handle_keypress(self, event, section):
        if event.char.isprintable() or event.keysym == 'BackSpace':
            self.filter_data(event, section)

    def create_section_label(self, section):
        if self.current_section_label is not None:
            self.current_section_label.destroy()
        formatted_section = section.capitalize()
        self.current_section_label = tk.Label(self.top_frame, text=f'Jesteś w sekcji: {formatted_section} ',
                                              bg='lightgray', fg='dark green', font='Helvetica 11 bold')
        self.current_section_label.pack(side=tk.LEFT, padx=10, pady=10)

    def get_column_text_width(self, table, col):
        max_width = 0
        for item in table.get_children():
            text = table.set(item, col)
            max_width = max(max_width, self.measure_text_width(text))
        return max_width + 10

    def measure_text_width(self, text):
        font = ('Arial', 10)
        return tkFont.Font(font=font).measure(text)

    def user_has_laptop(self, ID_UZYTKOWNIKA: str) -> bool:
        if not ID_UZYTKOWNIKA:
            return False
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute(SQL.get('select_msprzet_laptopy_dea55878', ''), (ID_UZYTKOWNIKA,))
            row = cursor.fetchone()
            return row is not None
        except Exception:
            return False
        finally:
            try:
                conn.close()
            except:
                pass

    def update_right_buttons(self, section):
        for widget in self.right_scrollable_frame.winfo_children():
            widget.destroy()
        for i, (btn_text, action, *kwargs) in enumerate(self.right_buttons.get(section, [])):
            btn_options = kwargs[0] if kwargs else {}
            btn = tk.Button(self.right_scrollable_frame, text=btn_text,
                            command=lambda act=action, sec=section: self.execute_action(act, sec), **btn_options)
            btn.pack(padx=15, pady=10, fill='x')
        if section == 'UŻYTKOWNIK':
            IMIE = self.user_values['IMIE'].cget('text')
            NAZWISKO = self.user_values['NAZWISKO'].cget('text')
            nr_kadrowy = self.user_values['NR KADROWY'].cget('text')
            ID_UZYTKOWNIKA = self.user_values['ID_UZYTKOWNIKA'].cget('text')
            if IMIE and NAZWISKO and nr_kadrowy and ID_UZYTKOWNIKA:
                protokol_btn = tk.Button(self.right_scrollable_frame, text='Protokół odbioru', bg='#87CEFA',
                                         command=self.generuj_protokol_odbioru)
                protokol_btn.pack(padx=15, pady=10, fill='x')
                oswiadczenie_btn = tk.Button(self.right_scrollable_frame, text='Oświadczenie laptop', bg='#87CEFA',
                                             command=self.generuj_oswiadczenie_laptop)
                oswiadczenie_btn.pack(padx=15, pady=10, fill='x')

    def execute_action(self, action, section):
        action_name = getattr(action, '__name__', '')

        # 1. Obsługa przycisków PRZYPISZ w oknie użytkownika
        if action_name.startswith('przypisz_'):
            user_id = self.user_values['ID_UZYTKOWNIKA'].cget('text')
            if not user_id:
                messagebox.showwarning('Uwaga', 'Najpierw wyszukaj i wybierz użytkownika z listy!')
                return
            action(user_id)
            return

        # 2. Uniwersalna obsługa reszty (z wykorzystaniem inspect)
        sig = inspect.signature(action)
        params = list(sig.parameters.values())

        if len(params) > 0:
            action(section)
        else:
            action()

    def save_filter_values(self, section):
        if not hasattr(self, 'filter_entries_by_section'): return
        entries = self.filter_entries_by_section.get(section, {})
        self.saved_filters = {key: entry.get() for key, entry in entries.items()}

    def restore_filter_values(self, section):
        if hasattr(self, 'saved_filters') and hasattr(self, 'filter_entries_by_section'):
            entries = self.filter_entries_by_section.get(section, {})
            for key, value in self.saved_filters.items():
                if key in entries:
                    entries[key].delete(0, tk.END)
                    entries[key].insert(0, value)
            self.filter_data(None, section)

    def reset_user_info(self):
        labels = ['NR KADROWY', 'IMIE', 'NAZWISKO', 'RODZAJ ZATRUDNIENIA', 'LOKALIZACJA', 'ID_UZYTKOWNIKA']
        for i, label_text in enumerate(labels):
            if label_text in self.user_values:
                self.user_values[label_text].config(text=f'', fg='red')
        for widget in self.frames['UŻYTKOWNIK'].winfo_children():
            widget.destroy()

    def search_user(self):
        search_window = tk.Toplevel(self)
        search_window.title('Wyszukaj UŻYTKOWNIKa')
        labels = ['NR KADROWY', 'IMIE', 'NAZWISKO', 'RODZAJ ZATRUDNIENIA  ', 'LOKALIZACJA', 'ID_UZYTKOWNIKA']
        entries = {}
        for i, label_text in enumerate(labels):
            tk.Label(search_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(search_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.bind('<KeyRelease>', self.dynamic_search_users)
            entries[label_text] = entry
        user_tree = ttk.Treeview(search_window, columns=labels, show='headings')
        user_tree.grid(row=len(labels) + 1, columnspan=2, padx=10, pady=10)
        for label_text in labels:
            user_tree.heading(label_text, text=label_text)
            user_tree.column(label_text, anchor='center')
        self.user_tree = user_tree
        self.search_window_entries = entries

        def select_user():
            selected_item = user_tree.selection()
            if not selected_item:
                messagebox.showinfo('Błąd', 'Nie wybrano żadnego UŻYTKOWNIKa.')
                return
            user_data = user_tree.item(selected_item[0])['values']
            user_data = [str(value).strip("',() ") for value in user_data]
            actual_labels = ['NR KADROWY', 'IMIE', 'NAZWISKO', 'RODZAJ ZATRUDNIENIA', 'LOKALIZACJA', 'ID_UZYTKOWNIKA']
            for i, label_text in enumerate(actual_labels):
                self.user_values[label_text].config(text=user_data[i], fg='midnightblue')
            self.frames['UŻYTKOWNIK'].pack_forget()
            self.frames['UŻYTKOWNIK'] = tk.Frame(self, width=600, height=500)
            self.frames['UŻYTKOWNIK'].pack_propagate(0)
            self.frames['UŻYTKOWNIK'].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            try:
                user_id = int(user_data[-1])
            except ValueError:
                messagebox.showinfo('Błąd', 'ID UŻYTKOWNIKa nie jest poprawną liczbą.')
                return
            self.userid_ze_sprzetu(user_id)
            self.display_user_assets(user_id)
            self.update_right_buttons('UŻYTKOWNIK')
            self.create_section_label('UŻYTKOWNIK')
            search_window.destroy()

        select_button = tk.Button(search_window, text='Wybierz UŻYTKOWNIKa', command=select_user)
        select_button.grid(row=len(labels) + 2, columnspan=2, padx=10, pady=10)
        user_tree.bind('<Double-1>', lambda event: select_user())
        search_window.update_idletasks()
        width = search_window.winfo_width()
        height = search_window.winfo_height()
        x_offset = (search_window.winfo_screenwidth() - width) // 2
        y_offset = (search_window.winfo_screenheight() - height) // 2
        search_window.geometry(f'+{x_offset}+{y_offset}')

    def search_user_w_sprzecie(self, parent_window=None):
        search_window = tk.Toplevel(self)
        search_window.title('Wyszukaj UŻYTKOWNIKa')
        labels = ['NR KADROWY', 'IMIE', 'NAZWISKO', 'RODZAJ ZATRUDNIENIA', 'LOKALIZACJA', 'ID_UZYTKOWNIKA']
        entries = {}
        for i, label_text in enumerate(labels):
            tk.Label(search_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(search_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.bind('<KeyRelease>', self.dynamic_search_users)
            entries[label_text] = entry
        user_tree = ttk.Treeview(search_window, columns=labels, show='headings')
        user_tree.grid(row=len(labels) + 1, columnspan=2, padx=10, pady=10)
        for label_text in labels:
            user_tree.heading(label_text, text=label_text)
            user_tree.column(label_text, anchor='center')
        self.user_tree = user_tree
        self.search_window_entries = entries

        def select_user_w_sprzecie():
            selected_item = user_tree.selection()
            if not selected_item:
                messagebox.showinfo('Błąd', 'Nie wybrano żadnego UŻYTKOWNIKa.')
                return
            user_data = user_tree.item(selected_item[0])['values']
            user_data = [str(value).strip("',() ") for value in user_data]
            try:
                user_id = str(user_data[-1])
                IMIE = str(user_data[1])
                NAZWISKO = str(user_data[2])
            except ValueError:
                messagebox.showinfo('Błąd', 'ID UŻYTKOWNIKa nie jest poprawną liczbą.')
                return
            if hasattr(self, 'ID_UZYTKOWNIKA_entry') and self.ID_UZYTKOWNIKA_entry:
                self.ID_UZYTKOWNIKA_entry.config(state='normal')
                self.ID_UZYTKOWNIKA_entry.delete(0, tk.END)
                self.ID_UZYTKOWNIKA_entry.insert(0, user_id)
                self.ID_UZYTKOWNIKA_entry.config(state='readonly')
            if hasattr(self, 'IMIE_entry') and self.IMIE_entry:
                self.IMIE_entry.config(state='normal')
                self.IMIE_entry.delete(0, tk.END)
                self.IMIE_entry.insert(0, IMIE)
                self.IMIE_entry.config(state='readonly')
            if hasattr(self, 'NAZWISKO_entry') and self.NAZWISKO_entry:
                self.NAZWISKO_entry.config(state='normal')
                self.NAZWISKO_entry.delete(0, tk.END)
                self.NAZWISKO_entry.insert(0, NAZWISKO)
                self.NAZWISKO_entry.config(state='readonly')
            search_window.destroy()

        select_button = tk.Button(search_window, text='Pobierz ID UŻYTKOWNIKa', command=select_user_w_sprzecie)
        select_button.grid(row=len(labels) + 2, columnspan=2, padx=10, pady=10)
        user_tree.bind('<Double-1>', lambda event: select_user_w_sprzecie())
        search_window.update_idletasks()
        width = search_window.winfo_width()
        height = search_window.winfo_height()
        x_offset = (search_window.winfo_screenwidth() - width) // 2
        y_offset = (search_window.winfo_screenheight() - height) // 2
        search_window.geometry(f'+{x_offset}+{y_offset}')
        if parent_window:
            parent_window.wait_window(search_window)

    def userid_ze_sprzetu(self, user_id):
        return user_id

    def dynamic_search_users(self, event):
        search_values = {'[NR KADROWY]' if label_text == 'NR KADROWY' else label_text: entry.get() for label_text, entry
                         in self.search_window_entries.items()}
        query_conditions = ' AND '.join([f'{key} LIKE ?' for key in search_values.keys() if search_values[key]])
        query_values = [f'%{value}%' for value in search_values.values() if value]
        conn = create_connection()
        cursor = conn.cursor()
        query = SQL.get('select_msprzet_konta_uzytkownikow_a27f20d4', 'SELECT * FROM msprzet_KONTA_UZYTKOWNIKOW')
        if query_conditions:
            query += ' WHERE ' + query_conditions
        try:
            cursor.execute(query, query_values)
            self.user_tree.delete(*self.user_tree.get_children())
            for row in cursor:
                clean_row = [str(value).strip("',() ") for value in row]
                self.user_tree.insert('', tk.END, values=clean_row)
        except Exception:
            pass
        finally:
            conn.close()

    def update_table_height(self, table, row_count):
        row_height = 25
        max_height = 800
        table_height = min(row_count * row_height, max_height)
        table.config(height=table_height)

    def adjust_column_widths(self, tree, frame):
        total_columns = len(tree['columns'])
        frame_width = frame.winfo_width()
        if total_columns > 0:
            column_width = frame_width // total_columns
            for col in tree['columns']:
                tree.column(col, width=column_width)

    def sterowanie_jednym_kliknieciem_w_sekcji_uzytkownik(self, event):
        tree = event.widget
        clicked_item = tree.identify_row(event.y)
        if not clicked_item:
            return 'break'
        if self.currently_selected_item is None:
            tree.selection_set(clicked_item)
            self.currently_selected_tree = tree
            self.currently_selected_item = clicked_item
        else:
            if self.currently_selected_tree is not None and self.currently_selected_tree.winfo_exists():
                self.currently_selected_tree.selection_remove(self.currently_selected_item)
            tree.selection_set(clicked_item)
            self.currently_selected_tree = tree
            self.currently_selected_item = clicked_item
        return 'break'

    def get_user_equipment(self, user_id):
        conn = create_connection()
        cursor = conn.cursor()
        equipment_sections = ['LAPTOPY', 'MONITORY', 'TELEFONY', 'SŁUCHAWKI', 'KARTY SIM', 'ROUTER', 'MYSZKI',
                              'KLAWIATURY']
        user_equipment = {section: [] for section in equipment_sections}
        column_descriptions = {}

        queries = {
            'LAPTOPY': SQL.get('select_user_equipment_laptopy', ''),
            'MONITORY': SQL.get('select_user_equipment_monitory', ''),
            'TELEFONY': SQL.get('select_user_equipment_telefony', ''),
            'SŁUCHAWKI': SQL.get('select_user_equipment_sluchawki', ''),
            'KARTY SIM': SQL.get('select_user_equipment_karty_sim', ''),
            'ROUTER': SQL.get('select_user_equipment_router', ''),
            'MYSZKI': SQL.get('select_user_equipment_myszki', ''),
            'KLAWIATURY': SQL.get('select_user_equipment_klawiatury', '')
        }

        for section, query in queries.items():
            if not query: continue
            try:
                cursor.execute(query, (user_id,))
                rows = cursor.fetchall()
                if rows:
                    cleaned_rows = [[value if value is not None else '' for value in row] for row in rows]
                    user_equipment[section] = cleaned_rows
                    column_descriptions[section] = [column[0] for column in cursor.description]
            except Exception:
                pass

        try:
            cursor.execute(SQL.get('select_msprzet_laptopy_69ad31bd', ''),
                           (user_id, user_id, user_id, user_id, user_id, user_id, user_id, user_id))
            total_equipment = cursor.fetchone()[0]
        except Exception:
            total_equipment = 0

        try:
            cursor.execute(SQL.get('select_msprzet_konta_uzytkownikow_640f037d', ''), user_id)
            result = cursor.fetchone()
            przelozony = result[0] if result else ''
        except Exception:
            przelozony = ''

        conn.close()
        return (user_equipment, column_descriptions, total_equipment, przelozony)

    def generate_user_email(self):
        if not win32:
            messagebox.showerror('Błąd', 'Brak biblioteki pywin32.')
            return
        user_data = {label: value.cget('text') for label, value in self.user_values.items()}
        user_id = user_data.get('ID_UZYTKOWNIKA')
        if not user_id:
            messagebox.showerror('Błąd', 'Brak ID UŻYTKOWNIKa.')
            return
        table_data, column_descriptions, total_equipment, przelozony = self.get_user_equipment(user_id)
        if total_equipment == 0:
            messagebox.showinfo('Informacja', 'Brak sprzętów u UŻYTKOWNIKa')
            return
        columns_to_hide = {'ID_UZYTKOWNIKA', 'NR SDJ', 'UWAGI', 'STATUS', 'ID'}
        email_body = '\n            <style>\n                table {\n                    border: 1px solid black;\n                    border-collapse: collapse;\n                }\n                th, td {\n                    border: 1px solid black;\n                    padding: 5px;\n                    text-align: center;\n                    vertical-align: middle;\n                }\n                th {\n                    background-color: #f2f2f2;\n                }\n                .pogrubione-czerwone {\n                    color: red;\n                    font-weight: bold;\n                }\n            </style>\n\n            <h2>Cześć,</h2>\n            <h2>Prosimy o dopilnowanie zwrotu poniższego sprzętu.</h2>\n            <h2 class="pogrubione-czerwone">Przy odbiorze prośba o weryfikację zgodnie z poniższą listą.</h2>\n            <h2>Informacje o UŻYTKOWNIKu:</h2>\n            <ul>\n            '
        for key, value in user_data.items():
            email_body += f'<li><b>{key}:</b> {value}</li>'
        email_body += '</ul>'
        email_body += '<h2>Sprzęt:</h2>'
        for section, data in table_data.items():
            if (section == 'MYSZKI' or section == 'KLAWIATURY') and (not data or data[0][0] == 0):
                continue
            if data:
                headers = column_descriptions[section]
                filtered_headers = [header for header in headers if header not in columns_to_hide]
                filtered_data = [[row[headers.index(header)] for header in filtered_headers] for row in data]
                if section == 'TELEFONY':
                    for row in filtered_data:
                        for i, header in enumerate(filtered_headers):
                            if header == 'KABEL USB C' and row[i] == 1:
                                row[i] = '✓'
                            elif header == 'KABEL USB C' and row[i] == 0:
                                row[i] = ''
                            elif header == 'LADOWARKA' and row[i] == 1:
                                row[i] = '✓'
                            elif header == 'LADOWARKA' and row[i] == 0:
                                row[i] = ''
                            elif header == 'LADOWARKA INDUKCYJNA' and row[i] == 1:
                                row[i] = '✓'
                            elif header == 'LADOWARKA INDUKCYJNA' and row[i] == 0:
                                row[i] = ''
                            elif header == 'PRZEJSCIOWKA DO TELEFONU' and row[i] == 1:
                                row[i] = '✓'
                            elif header == 'PRZEJSCIOWKA DO TELEFONU' and row[i] == 0:
                                row[i] = ''
                            elif header == 'ETUI' and row[i] == 1:
                                row[i] = '✓'
                            elif header == 'ETUI' and row[i] == 0:
                                row[i] = ''
                table = '<table><tr>'
                for header in filtered_headers:
                    table += f'<th style="text-align: center; vertical-align: middle;">{header}</th>'
                table += '</tr>'
                for row in filtered_data:
                    table += '<tr>'
                    for cell in row:
                        table += f'<td style="text-align: center; vertical-align: middle;">{cell}</td>'
                    table += '</tr>'
                table += '</table>'
                email_body += f'<h3>{section}:</h3>{table}'
        self.send_email(email_body, user_data, przelozony)

    def send_email(self, email_body, user_data, przelozony):
        IMIE = user_data.get('IMIE', 'N/A')
        NAZWISKO = user_data.get('NAZWISKO', 'N/A')
        numer_kadrowy = user_data.get('NR KADROWY', 'N/A')
        subject = f'Informacje o sprzęcie: {IMIE} {NAZWISKO} {numer_kadrowy}'
        windows = gw.getWindowsWithTitle(subject)
        if windows:
            for win in windows:
                win.activate()
                hwnd = win._hWnd
                ctypes.windll.user32.SetForegroundWindow(hwnd)
                ctypes.windll.user32.SetFocus(hwnd)
                ctypes.windll.user32.BringWindowToTop(hwnd)
                ctypes.windll.user32.SetForegroundWindow(hwnd)
                ctypes.windll.user32.SetFocus(hwnd)
                time.sleep(0.1)
            return
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.Subject = subject
        mail.HTMLBody = email_body
        mail.Display()
        mail.To = f'{przelozony}'
        mail.CC = cfg_get('email', 'cc', fallback='')
        time.sleep(0.4)
        windows = gw.getWindowsWithTitle(subject)
        if windows:
            for win in windows:
                win.activate()
                hwnd = win._hWnd
                ctypes.windll.user32.SetForegroundWindow(hwnd)
                ctypes.windll.user32.SetFocus(hwnd)
                ctypes.windll.user32.BringWindowToTop(hwnd)
                ctypes.windll.user32.SetForegroundWindow(hwnd)
                ctypes.windll.user32.SetFocus(hwnd)
                time.sleep(0.1)
        else:
            print('Nie udało się znaleźć okna wiadomości.')

    def _get_section_spec(self, section: str):
        try:
            return SECTION_SPECS.get(section)
        except Exception:
            return None

    def _ensure_tree_style_if_needed(self, spec):
        if not spec or not getattr(spec, 'use_custom_style', False):
            return
        try:
            style = ttk.Style()
            style.configure('Custom.Treeview.Heading', padding=(1, 0, 0, 15))
            style.configure('Custom.Treeview', rowheight=25)
        except Exception:
            pass

    def _build_section_table(self, section: str, spec):
        filter_frame = tk.Frame(self.frames[section], bg='lightgray')
        filter_frame.pack(side=tk.TOP, fill=tk.X)
        self.result_count_var[section] = tk.StringVar(value='Wyniki: 0')
        tk.Label(filter_frame, textvariable=self.result_count_var[section], bg='lightgray', fg='black',
                 font='Helvetica 10 bold').grid(row=2, column=0, padx=5, pady=(0, 6), sticky='w')
        entries = {}
        for i, label in enumerate(spec.filter_labels):
            tk.Label(filter_frame, text=label).grid(row=0, column=i, padx=5, pady=5)
            ent = tk.Entry(filter_frame)
            ent.grid(row=1, column=i, padx=5, pady=5)
            ent.bind('<KeyRelease>', self.on_filter_change)
            entries[label] = ent
        if not hasattr(self, 'filter_entries_by_section'):
            self.filter_entries_by_section = {}
        self.filter_entries_by_section[section] = entries
        self._ensure_tree_style_if_needed(spec)
        tv_kwargs = {'style': 'Custom.Treeview'} if getattr(spec, 'use_custom_style', False) else {}
        tree = ttk.Treeview(self.frames[section], columns=spec.columns, show='headings', **tv_kwargs)
        vsb = ttk.Scrollbar(self.frames[section], orient=tk.VERTICAL, command=tree.yview)
        hsb = ttk.Scrollbar(self.frames[section], orient=tk.HORIZONTAL, command=tree.xview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        setattr(self, spec.tree_attr, tree)
        for col in spec.columns:
            tree.heading(col, text=col, anchor='center')
            if col in getattr(spec, 'hidden_columns', ()):
                tree.column(col, width=0, stretch=tk.NO)
        self.update_column_widths(tree, section)
        try:
            getattr(self, spec.fetch_method)()
        except Exception:
            pass
        self.update_result_count(section, tree)
        tree.bind('<Button-3>', lambda event, t=tree: self.show_context_menu(event, t))

    def populate_frame_with_data(self, section):
        for widget in self.frames[section].winfo_children():
            widget.destroy()
        self.create_section_label(section)
        self.update_right_buttons(section)
        if section == 'UŻYTKOWNIK':
            return
        spec = self._get_section_spec(section)
        if not spec:
            return
        self._build_section_table(section, spec)

    def _get_filter_entries_for_section(self, section: str):
        if hasattr(self, 'filter_entries_by_section'):
            return self.filter_entries_by_section.get(section, {})
        return {}

    def filter_data(self, event, section):
        spec = self._get_section_spec(section)
        if not spec:
            return
        tree = getattr(self, spec.tree_attr, None)
        if not tree:
            return
        filter_entries = self._get_filter_entries_for_section(section)
        original_data = getattr(self, spec.original_data_attr, None)
        if original_data is None:
            original_data = [(tree.item(i, 'text'), tree.item(i, 'values')) for i in tree.get_children()]
        filter_texts = {k: (e.get() or '').lower() for k, e in filter_entries.items()}
        if all((not v for v in filter_texts.values())):
            tree.delete(*tree.get_children())
            for t, vals in original_data:
                tree.insert('', tk.END, text=t, values=vals)
            self.update_result_count(section, tree)
            return
        col_map = spec.filter_col_map or {lbl: spec.columns.index(lbl) for lbl in spec.filter_labels if
                                          lbl in spec.columns}
        matched = []
        for t, vals in original_data:
            ok = True
            for lbl, needle in filter_texts.items():
                if not needle:
                    continue
                idx = col_map.get(lbl)
                if idx is None or idx >= len(vals):
                    ok = False
                    break
                if needle not in str(vals[idx]).lower():
                    ok = False
                    break
            if ok:
                matched.append((t, vals))
        tree.delete(*tree.get_children())
        for t, vals in matched:
            tree.insert('', tk.END, text=t, values=vals)
        self.update_result_count(section, tree)

    def on_filter_change(self, event):
        try:
            self.filter_data(event, self.current_section)
        except Exception:
            pass

    def action22(self, section):
        self.dodaj_laptopa()

    def action23(self, section):
        self.dodaj_monitor()

    def action24(self, section):
        self.save_filter_values(section)
        selected_items = self.tabela_monitory.selection()
        if not selected_items:
            messagebox.showinfo('Błąd', 'Nie wybrano żadnego rekordu do edycji.')
        elif len(selected_items) > 1:
            messagebox.showinfo('Błąd', 'Wybierz tylko jeden rekord do edycji.')
        else:
            record_id = self.tabela_monitory.item(selected_items[0])['values'][-1]
            self.edit_record_window_monitory(record_id)

    def action25(self, section):
        self.delete_record(section)

    def action26(self, section):
        self.populate_frame_with_data('MONITORY')

    def action27(self, section):
        if section == 'KONTA UŻYTKOWNIKÓW':
            self.dodaj_konto_uzytkownika()


if __name__ == '__main__':
    app = Application()
    app.mainloop()