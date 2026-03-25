import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
from config_db import create_connection, SQL


class EdytujUzytkownikMixin:

    def edit_user_record_specific(self):
        selected_items_laptops = self.laptop_tree.selection() if self.laptop_tree else []
        selected_items_monitors = self.monitor_tree.selection() if self.monitor_tree else []
        selected_items_phones = self.phone_tree.selection() if self.phone_tree else []
        selected_items_sluchawki = self.sluchawki_tree.selection() if self.sluchawki_tree else []
        selected_items_karty_sim = self.karty_sim_tree.selection() if self.karty_sim_tree else []
        selected_items_router = self.router_tree.selection() if self.router_tree else []
        selected_items_myszki = self.myszki_tree.selection() if self.myszki_tree else []
        selected_items_klawiatury = self.klawiatury_tree.selection() if self.klawiatury_tree else []

        num_selected_laptops = len(selected_items_laptops)
        num_selected_monitors = len(selected_items_monitors)
        num_selected_phones = len(selected_items_phones)
        num_selected_sluchawki = len(selected_items_sluchawki)
        num_selected_karty_sim = len(selected_items_karty_sim)
        num_selected_router = len(selected_items_router)
        num_selected_myszki = len(selected_items_myszki)
        num_selected_klawiatury = len(selected_items_klawiatury)

        if num_selected_laptops == 0 and num_selected_monitors == 0 and (num_selected_phones == 0) and (
                num_selected_sluchawki == 0) and (num_selected_karty_sim == 0) and (num_selected_router == 0) and (
                num_selected_myszki == 0) and (num_selected_klawiatury == 0):
            messagebox.showinfo('Błąd', 'Nie wybrano żadnego rekordu do edycji.')
            return

        if num_selected_laptops + num_selected_monitors + num_selected_phones + num_selected_sluchawki + num_selected_karty_sim + num_selected_router + num_selected_myszki + num_selected_klawiatury > 1:
            messagebox.showinfo('Błąd',
                                'Możesz edytować tylko jeden rekord naraz. Wybierz tylko jeden rekord do edycji.')
            if self.laptop_tree:
                for item in selected_items_laptops:
                    self.laptop_tree.selection_remove(item)
            if self.monitor_tree:
                for item in selected_items_monitors:
                    self.monitor_tree.selection_remove(item)
            if self.phone_tree:
                for item in selected_items_phones:
                    self.phone_tree.selection_remove(item)
            if self.sluchawki_tree:
                for item in selected_items_sluchawki:
                    self.sluchawki_tree.selection_remove(item)
            if self.karty_sim_tree:
                for item in selected_items_karty_sim:
                    self.karty_sim_tree.selection_remove(item)
            if self.router_tree:
                for item in selected_items_router:
                    self.router_tree.selection_remove(item)
            if self.myszki_tree:
                for item in selected_items_myszki:
                    self.myszki_tree.selection_remove(item)
            if self.klawiatury_tree:
                for item in selected_items_klawiatury:
                    self.klawiatury_tree.selection_remove(item)
            return

        if num_selected_laptops == 1:
            record_id = self.laptop_tree.item(selected_items_laptops[0])['values'][-1]
            user_id = self.laptop_tree.item(selected_items_laptops[0])['values'][-2]
            self.edit_record_window_laptopy_uzytkownik(record_id, user_id)
        elif num_selected_monitors == 1:
            record_id = self.monitor_tree.item(selected_items_monitors[0])['values'][-1]
            user_id = self.monitor_tree.item(selected_items_monitors[0])['values'][-2]
            self.edit_record_window_monitory_uzytkownik(record_id, user_id)
        elif num_selected_phones == 1:
            record_id = self.phone_tree.item(selected_items_phones[0])['values'][-1]
            user_id = self.phone_tree.item(selected_items_phones[0])['values'][-2]
            self.edit_record_window_telefony_uzytkownik(record_id, user_id)
        elif num_selected_sluchawki == 1:
            record_id = self.sluchawki_tree.item(selected_items_sluchawki[0])['values'][-1]
            user_id = self.sluchawki_tree.item(selected_items_sluchawki[0])['values'][-2]
            self.edit_record_window_sluchawki_uzytkownik(record_id, user_id)
        elif num_selected_karty_sim == 1:
            record_id = self.karty_sim_tree.item(selected_items_karty_sim[0])['values'][-1]
            user_id = self.karty_sim_tree.item(selected_items_karty_sim[0])['values'][-2]
            self.edit_record_window_karty_sim_uzytkownik(record_id, user_id)
        elif num_selected_router == 1:
            record_id = self.router_tree.item(selected_items_router[0])['values'][-1]
            user_id = self.router_tree.item(selected_items_router[0])['values'][-2]
            self.edit_record_window_router_uzytkownik(record_id, user_id)
        elif num_selected_myszki == 1:
            record_id = self.myszki_tree.item(selected_items_myszki[0])['values'][-1]
            user_id = self.myszki_tree.item(selected_items_myszki[0])['values'][-2]
            self.edit_record_window_myszki_uzytkownik(record_id, user_id)
        elif num_selected_klawiatury == 1:
            record_id = self.klawiatury_tree.item(selected_items_klawiatury[0])['values'][-1]
            user_id = self.klawiatury_tree.item(selected_items_klawiatury[0])['values'][-2]
            self.edit_record_window_klawiatury_uzytkownik(record_id, user_id)

    def edit_record_window_laptopy_uzytkownik(self, record_id, user_id, section='UŻYTKOWNIK'):
        edit_window = tk.Toplevel(self)
        edit_window.geometry('600x550')
        edit_window.title(f'Edytuj rekord  ({section})')
        edit_window.transient(self)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(SQL['select_msprzet_statusy_c423c854'])
        status_values = [row[0] for row in cursor.fetchall()]
        conn.close()
        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_laptopy_ac290dd3']
        cursor.execute(query, (record_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            messagebox.showerror('Błąd', 'Nie znaleziono rekordu o podanym ID.')
            edit_window.destroy()
            return
        labels = ['STATUS', 'IMIE', 'NAZWISKO', 'ID_UZYTKOWNIKA', 'NR SRODKA TRWALEGO', 'NAZWA LAPTOPA', 'NR SERYJNY',
                  'MODEL', 'NR SDJ', 'UWAGI']
        entries = {}
        self.ID_UZYTKOWNIKA_entry = None
        self.IMIE_entry = None
        self.NAZWISKO_entry = None
        row = [value if value is not None else '' for value in row]
        bold_font = tkFont.Font(weight='bold', size=8)
        for i, label_text in enumerate(labels):
            tk.Label(edit_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            if label_text == 'STATUS':
                entry = tk.StringVar(edit_window)
                entry.set(row[i])
                entry_dropdown = tk.OptionMenu(edit_window, entry, *status_values)
                entry_dropdown.grid(row=i, column=1, padx=10, pady=5)
                entry_dropdown.config(font=bold_font)
            elif label_text == 'IMIE':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.IMIE_entry = entry
            elif label_text == 'NAZWISKO':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.NAZWISKO_entry = entry
            elif label_text == 'ID_UZYTKOWNIKA':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.ID_UZYTKOWNIKA_entry = entry
            elif label_text == 'UWAGI':
                entry = tk.Text(edit_window, height=5, width=40, font='Helvetica 10')
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entries[label_text] = entry
            else:
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
            entries[label_text] = entry

        def save_changes():
            new_values = {}
            for label_text, entry in entries.items():
                if label_text in ['IMIE', 'NAZWISKO']:
                    continue
                if isinstance(entry, tk.Text):
                    new_values[label_text] = entry.get('1.0', tk.END).strip()
                elif isinstance(entry, tk.StringVar):
                    new_values[label_text] = entry.get()
                else:
                    new_values[label_text] = entry.get()
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute(SQL['select_msprzet_laptopy_0cf809da'],
                           (new_values['NR SRODKA TRWALEGO'], new_values['NR SERYJNY'], record_id))
            count = cursor.fetchone()[0]
            if count > 0:
                messagebox.showerror('Błąd',
                                     'Laptop o podanym numerze środka trwałego lub numerze seryjnym już istnieje.')
                conn.close()
                return
            set_params = ', '.join((f'[{key}] = ?' for key in new_values.keys()))
            update_values = tuple(new_values.values()) + (record_id,)
            update_query = SQL['update_msprzet_laptopy_501ca15d'].format(**locals())
            cursor.execute(update_query, update_values)
            conn.commit()
            conn.close()
            edit_window.destroy()
            for widget in self.frames['UŻYTKOWNIK'].winfo_children():
                widget.destroy()
            self.display_user_assets(user_id=user_id)

        save_button = tk.Button(edit_window, text='Zapisz zmiany', command=save_changes)
        save_button.grid(row=len(labels) + 1, column=0, padx=10, pady=10)
        wyszukaj_uzytkownika = tk.Button(edit_window, text='Wyszukaj UŻYTKOWNIKa',
                                         command=lambda: self.search_user_w_sprzecie(edit_window))
        wyszukaj_uzytkownika.grid(row=len(labels) + 1, column=1, padx=10, pady=10)
        odpisanie_UŻYTKOWNIKa = tk.Button(edit_window, text='Odpisz UŻYTKOWNIKa',
                                          command=lambda: self.odpisz_uzytkownika(entries['ID_UZYTKOWNIKA']))
        odpisanie_UŻYTKOWNIKa.grid(row=len(labels) + 1, column=2, padx=10, pady=10)
        edit_window.update_idletasks()
        width = edit_window.winfo_width()
        height = edit_window.winfo_height()
        x_offset = (edit_window.winfo_screenwidth() - width) // 2
        y_offset = (edit_window.winfo_screenheight() - height) // 2
        edit_window.geometry(f'+{x_offset}+{y_offset}')
        edit_window.focus_set()

    def edit_record_window_monitory_uzytkownik(self, record_id, user_id, section='UŻYTKOWNIK'):
        edit_window = tk.Toplevel(self)
        edit_window.geometry('600x550')
        edit_window.title(f'Edytuj rekord monitora ({section})')
        edit_window.transient(self)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(SQL['select_msprzet_statusy_c423c854'])
        status_values = [row[0] for row in cursor.fetchall()]
        conn.close()
        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_monitory_630c3b70']
        cursor.execute(query, (record_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            messagebox.showerror('Błąd', 'Nie znaleziono rekordu o podanym ID.')
            edit_window.destroy()
            return
        labels = ['STATUS', 'IMIE', 'NAZWISKO', 'ID_UZYTKOWNIKA', 'NR SERYJNY', 'MODEL', 'NR SDJ', 'UWAGI']
        entries = {}
        self.ID_UZYTKOWNIKA_entry = None
        self.IMIE_entry = None
        self.NAZWISKO_entry = None
        row = [value if value is not None else '' for value in row]
        bold_font = tkFont.Font(weight='bold', size=8)
        for i, label_text in enumerate(labels):
            tk.Label(edit_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            if label_text == 'STATUS':
                entry = tk.StringVar(edit_window)
                entry.set(row[i])
                entry_dropdown = tk.OptionMenu(edit_window, entry, *status_values)
                entry_dropdown.grid(row=i, column=1, padx=10, pady=5)
                entry_dropdown.config(font=bold_font)
            elif label_text == 'IMIE':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.IMIE_entry = entry
            elif label_text == 'NAZWISKO':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.NAZWISKO_entry = entry
            elif label_text == 'ID_UZYTKOWNIKA':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.ID_UZYTKOWNIKA_entry = entry
            elif label_text == 'UWAGI':
                entry = tk.Text(edit_window, height=5, width=40, font='Helvetica 10')
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entries[label_text] = entry
            else:
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
            entries[label_text] = entry

        def save_changes():
            new_values = {}
            for label_text, entry in entries.items():
                if label_text in ['IMIE', 'NAZWISKO']:
                    continue
                if isinstance(entry, tk.Text):
                    new_values[label_text] = entry.get('1.0', tk.END).strip()
                elif isinstance(entry, tk.StringVar):
                    new_values[label_text] = entry.get()
                else:
                    new_values[label_text] = entry.get()
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute(SQL['select_msprzet_monitory_296146a1'], (new_values['NR SERYJNY'], record_id))
            count = cursor.fetchone()[0]
            if count > 0:
                messagebox.showerror('Błąd', 'Monitor o podanym numerze seryjnym już istnieje.')
                conn.close()
                return
            set_params = ', '.join((f'[{key}] = ?' for key in new_values.keys()))
            update_values = tuple(new_values.values()) + (record_id,)
            update_query = SQL['update_msprzet_monitory_5050a48b'].format(**locals())
            cursor.execute(update_query, update_values)
            conn.commit()
            conn.close()
            edit_window.destroy()
            for widget in self.frames['UŻYTKOWNIK'].winfo_children():
                widget.destroy()
            self.display_user_assets(user_id=user_id)

        save_button = tk.Button(edit_window, text='Zapisz zmiany', command=save_changes)
        save_button.grid(row=len(labels) + 1, column=0, padx=10, pady=10)
        wyszukaj_uzytkownika = tk.Button(edit_window, text='Wyszukaj UŻYTKOWNIKa',
                                         command=lambda: self.search_user_w_sprzecie(edit_window))
        wyszukaj_uzytkownika.grid(row=len(labels) + 1, column=1, padx=10, pady=10)
        odpisanie_UŻYTKOWNIKa = tk.Button(edit_window, text='Odpisz UŻYTKOWNIKa',
                                          command=lambda: self.odpisz_uzytkownika(entries['ID_UZYTKOWNIKA']))
        odpisanie_UŻYTKOWNIKa.grid(row=len(labels) + 1, column=2, padx=10, pady=10)
        edit_window.update_idletasks()
        width = edit_window.winfo_width()
        height = edit_window.winfo_height()
        x_offset = (edit_window.winfo_screenwidth() - width) // 2
        y_offset = (edit_window.winfo_screenheight() - height) // 2
        edit_window.geometry(f'+{x_offset}+{y_offset}')
        edit_window.focus_set()

    def edit_record_window_telefony_uzytkownik(self, record_id, user_id, section='UŻYTKOWNIK'):
        edit_window = tk.Toplevel(self)
        edit_window.geometry('700x650')
        edit_window.title(f'Edytuj rekord telefonu ({section})')
        edit_window.transient(self)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(SQL['select_msprzet_statusy_c423c854'])
        status_values = [row[0] for row in cursor.fetchall()]
        conn.close()
        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_telefony_56c4e8c0']
        cursor.execute(query, (record_id,))
        row = cursor.fetchone()
        conn.close()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(SQL['select_msprzet_model_telefonu_5e4ba938'])
        model_telefonu_values = [row[0] for row in cursor.fetchall()]
        conn.close()
        if not row:
            messagebox.showerror('Błąd', 'Nie znaleziono rekordu o podanym ID.')
            edit_window.destroy()
            return
        labels = ['STATUS', 'IMIE', 'NAZWISKO', 'ID_UZYTKOWNIKA', 'IMEI', 'LADOWARKA', 'KABEL USB C',
                  'LADOWARKA INDUKCYJNA', 'PRZEJSCIOWKA DO TELEFONU', 'ETUI', 'NR TELEFONU', 'MODEL', 'NR SDJ', 'UWAGI']
        entries = {}
        self.ID_UZYTKOWNIKA_entry = None
        self.IMIE_entry = None
        self.NAZWISKO_entry = None
        row = [value if value is not None else '' for value in row]
        bold_font = tkFont.Font(weight='bold', size=8)
        for i, label_text in enumerate(labels):
            tk.Label(edit_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            if label_text == 'STATUS':
                entry = tk.StringVar(edit_window)
                entry.set(row[i])
                entry_dropdown = tk.OptionMenu(edit_window, entry, *status_values)
                entry_dropdown.grid(row=i, column=1, padx=10, pady=5)
                entry_dropdown.config(font=bold_font)
            elif label_text == 'IMIE':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.IMIE_entry = entry
            elif label_text == 'NAZWISKO':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.NAZWISKO_entry = entry
            elif label_text == 'ID_UZYTKOWNIKA':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.ID_UZYTKOWNIKA_entry = entry
            elif label_text == 'MODEL':
                entry = tk.StringVar(edit_window)
                entry.set(row[i])
                entry_dropdown = tk.OptionMenu(edit_window, entry, *model_telefonu_values)
                entry_dropdown.grid(row=i, column=1, padx=10, pady=5)
                entries[label_text] = entry
            elif label_text == 'UWAGI':
                entry = tk.Text(edit_window, height=5, width=40, font='Helvetica 10')
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entries[label_text] = entry
            elif label_text in ['LADOWARKA', 'KABEL USB C', 'LADOWARKA INDUKCYJNA', 'PRZEJSCIOWKA DO TELEFONU', 'ETUI']:
                entry = tk.IntVar(value=int(row[i]))
                checkbox = tk.Checkbutton(edit_window, variable=entry)
                checkbox.grid(row=i, column=1, padx=10, pady=5)
                entries[label_text] = entry
            else:
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
            entries[label_text] = entry

        def save_changes():
            new_values = {}
            for label_text, entry in entries.items():
                if label_text in ['IMIE', 'NAZWISKO']:
                    continue
                if isinstance(entry, tk.Text):
                    new_values[label_text] = entry.get('1.0', tk.END).strip()
                elif isinstance(entry, tk.StringVar):
                    new_values[label_text] = entry.get()
                elif isinstance(entry, tk.IntVar):
                    new_values[label_text] = entry.get()
                else:
                    new_values[label_text] = entry.get()
            nr_telefonu = new_values.get('NR TELEFONU', '')
            if nr_telefonu != '0' and (not nr_telefonu.isdigit() or len(nr_telefonu) != 9):
                messagebox.showerror('Błąd', 'Numer telefonu musi zawierać dokładnie 9 cyfr, jeśli jest podany.')
                return
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute(SQL['select_msprzet_telefony_12deb8ee'],
                           (new_values['IMEI'], new_values['NR TELEFONU'], record_id))
            count = cursor.fetchone()[0]
            if count > 0:
                messagebox.showerror('Błąd', 'Telefon o podanym numerze IMEI lub numerze telefonu już istnieje.')
                conn.close()
                return
            set_params = ', '.join((f'[{key}] = ?' for key in new_values.keys()))
            update_values = tuple(new_values.values()) + (record_id,)
            update_query = SQL['update_msprzet_telefony_97c35fcb'].format(**locals())
            cursor.execute(update_query, update_values)
            conn.commit()
            conn.close()
            edit_window.destroy()
            for widget in self.frames['UŻYTKOWNIK'].winfo_children():
                widget.destroy()
            self.display_user_assets(user_id=user_id)

        save_button = tk.Button(edit_window, text='Zapisz zmiany', command=save_changes)
        save_button.grid(row=len(labels) + 1, column=0, padx=10, pady=10)
        wyszukaj_uzytkownika = tk.Button(edit_window, text='Wyszukaj UŻYTKOWNIKa',
                                         command=lambda: self.search_user_w_sprzecie(edit_window))
        wyszukaj_uzytkownika.grid(row=len(labels) + 1, column=1, padx=10, pady=10)
        odpisanie_UŻYTKOWNIKa = tk.Button(edit_window, text='Odpisz UŻYTKOWNIKa',
                                          command=lambda: self.odpisz_uzytkownika(entries['ID_UZYTKOWNIKA']))
        odpisanie_UŻYTKOWNIKa.grid(row=len(labels) + 1, column=2, padx=10, pady=10)
        edit_window.update_idletasks()
        width = edit_window.winfo_width()
        height = edit_window.winfo_height()
        x_offset = (edit_window.winfo_screenwidth() - width) // 2
        y_offset = (edit_window.winfo_screenheight() - height) // 2
        edit_window.geometry(f'+{x_offset}+{y_offset}')
        edit_window.focus_set()

    def edit_record_window_sluchawki_uzytkownik(self, record_id, user_id, section='UŻYTKOWNIK'):
        edit_window = tk.Toplevel(self)
        edit_window.geometry('600x500')
        edit_window.title(f'Edytuj rekord słuchawek ({section})')
        edit_window.transient(self)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(SQL['select_msprzet_statusy_c423c854'])
        status_values = [row[0] for row in cursor.fetchall()]
        conn.close()
        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_sluchawki_521589e1']
        cursor.execute(query, (record_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            messagebox.showerror('Błąd', 'Nie znaleziono rekordu o podanym ID.')
            edit_window.destroy()
            return
        labels = ['STATUS', 'IMIE', 'NAZWISKO', 'ID_UZYTKOWNIKA', 'NR SERYJNY', 'MODEL', 'NR SDJ', 'UWAGI']
        entries = {}
        self.ID_UZYTKOWNIKA_entry = None
        self.IMIE_entry = None
        self.NAZWISKO_entry = None
        row = [value if value is not None else '' for value in row]
        bold_font = tkFont.Font(weight='bold', size=8)
        for i, label_text in enumerate(labels):
            tk.Label(edit_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            if label_text == 'STATUS':
                entry = tk.StringVar(edit_window)
                entry.set(row[i])
                entry_dropdown = tk.OptionMenu(edit_window, entry, *status_values)
                entry_dropdown.grid(row=i, column=1, padx=10, pady=5)
                entry_dropdown.config(font=bold_font)
            elif label_text == 'IMIE':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.IMIE_entry = entry
            elif label_text == 'NAZWISKO':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.NAZWISKO_entry = entry
            elif label_text == 'ID_UZYTKOWNIKA':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.ID_UZYTKOWNIKA_entry = entry
            elif label_text == 'UWAGI':
                entry = tk.Text(edit_window, height=5, width=40, font='Helvetica 10')
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entries[label_text] = entry
            else:
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
            entries[label_text] = entry

        def save_changes():
            new_values = {}
            for label_text, entry in entries.items():
                if label_text in ['IMIE', 'NAZWISKO']:
                    continue
                if isinstance(entry, tk.Text):
                    new_values[label_text] = entry.get('1.0', tk.END).strip()
                elif isinstance(entry, tk.StringVar):
                    new_values[label_text] = entry.get()
                else:
                    new_values[label_text] = entry.get()
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute(SQL['select_msprzet_sluchawki_917c2313'], (new_values['NR SERYJNY'], record_id))
            count = cursor.fetchone()[0]
            if count > 0:
                messagebox.showerror('Błąd', 'Słuchawki o podanym numerze seryjnym już istnieją.')
                conn.close()
                return
            set_params = ', '.join((f'[{key}] = ?' for key in new_values.keys()))
            update_values = tuple(new_values.values()) + (record_id,)
            update_query = SQL['update_msprzet_sluchawki_1906e900'].format(**locals())
            cursor.execute(update_query, update_values)
            conn.commit()
            conn.close()
            edit_window.destroy()
            for widget in self.frames['UŻYTKOWNIK'].winfo_children():
                widget.destroy()
            self.display_user_assets(user_id=user_id)

        save_button = tk.Button(edit_window, text='Zapisz zmiany', command=save_changes)
        save_button.grid(row=len(labels) + 1, column=0, padx=10, pady=10)
        wyszukaj_uzytkownika = tk.Button(edit_window, text='Wyszukaj UŻYTKOWNIKa',
                                         command=lambda: self.search_user_w_sprzecie(edit_window))
        wyszukaj_uzytkownika.grid(row=len(labels) + 1, column=1, padx=10, pady=10)
        odpisanie_UŻYTKOWNIKa = tk.Button(edit_window, text='Odpisz UŻYTKOWNIKa',
                                          command=lambda: self.odpisz_uzytkownika(entries['ID_UZYTKOWNIKA']))
        odpisanie_UŻYTKOWNIKa.grid(row=len(labels) + 1, column=2, padx=10, pady=10)
        edit_window.update_idletasks()
        width = edit_window.winfo_width()
        height = edit_window.winfo_height()
        x_offset = (edit_window.winfo_screenwidth() - width) // 2
        y_offset = (edit_window.winfo_screenheight() - height) // 2
        edit_window.geometry(f'+{x_offset}+{y_offset}')
        edit_window.focus_set()

    def edit_record_window_karty_sim_uzytkownik(self, record_id, user_id, section='UŻYTKOWNIK'):
        edit_window = tk.Toplevel(self)
        edit_window.geometry('600x550')
        edit_window.title(f'Edytuj rekord karty sim ({section})')
        edit_window.transient(self)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(SQL['select_msprzet_statusy_c423c854'])
        status_values = [row[0] for row in cursor.fetchall()]
        cursor.execute(SQL['select_msprzet_operatorzy_komorkowi_9fbcfa7d'])
        operator_values = [row[0] for row in cursor.fetchall()]
        conn.close()
        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_karty_sim_771d0545']
        cursor.execute(query, (record_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            messagebox.showerror('Błąd', 'Nie znaleziono rekordu o podanym ID.')
            edit_window.destroy()
            return
        labels = ['STATUS', 'IMIE', 'NAZWISKO', 'ID_UZYTKOWNIKA', 'NR TELEFONU', 'NR SIM', 'OPERATOR', 'NR SDJ',
                  'UWAGI']
        entries = {}
        self.ID_UZYTKOWNIKA_entry = None
        self.IMIE_entry = None
        self.NAZWISKO_entry = None
        row = [value if value is not None else '' for value in row]
        bold_font = tkFont.Font(weight='bold', size=8)
        for i, label_text in enumerate(labels):
            tk.Label(edit_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            if label_text == 'STATUS':
                entry = tk.StringVar(edit_window)
                entry.set(row[i])
                entry_dropdown = tk.OptionMenu(edit_window, entry, *status_values)
                entry_dropdown.grid(row=i, column=1, padx=10, pady=5)
                entry_dropdown.config(font=bold_font)
            elif label_text == 'IMIE':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.IMIE_entry = entry
            elif label_text == 'NAZWISKO':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.NAZWISKO_entry = entry
            elif label_text == 'OPERATOR':
                entry = tk.StringVar(edit_window)
                entry.set(row[i])
                entry_dropdown = tk.OptionMenu(edit_window, entry, *operator_values)
                entry_dropdown.grid(row=i, column=1, padx=10, pady=5)
            elif label_text == 'ID_UZYTKOWNIKA':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.ID_UZYTKOWNIKA_entry = entry
            elif label_text == 'UWAGI':
                entry = tk.Text(edit_window, height=5, width=40, font='Helvetica 10')
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entries[label_text] = entry
            else:
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
            entries[label_text] = entry

        def save_changes():
            new_values = {}
            for label_text, entry in entries.items():
                if label_text in ['IMIE', 'NAZWISKO']:
                    continue
                if isinstance(entry, tk.Text):
                    new_values[label_text] = entry.get('1.0', tk.END).strip()
                elif isinstance(entry, tk.StringVar):
                    new_values[label_text] = entry.get()
                else:
                    new_values[label_text] = entry.get()
            nr_telefonu = new_values.get('NR TELEFONU', '')
            if nr_telefonu != '0' and (not nr_telefonu.isdigit() or len(nr_telefonu) != 9):
                messagebox.showerror('Błąd', 'Numer telefonu musi zawierać dokładnie 9 cyfr, jeśli jest podany.')
                return
            sim = new_values.get('NR SIM', '')
            if sim and (not sim.isdigit()):
                messagebox.showerror('Błąd', 'NR SIM może zawierać tylko cyfry.')
                return
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute(SQL['select_msprzet_karty_sim_a6d6b363'],
                           (new_values['NR TELEFONU'], new_values['NR SIM'], record_id))
            count = cursor.fetchone()[0]
            if count > 0:
                messagebox.showerror('Błąd', 'Karta SIM o podanym numerze telefonu lub numerze SIM już istnieje.')
                conn.close()
                return
            set_params = ', '.join((f'[{key}] = ?' for key in new_values.keys()))
            update_values = tuple(new_values.values()) + (record_id,)
            update_query = SQL['update_msprzet_karty_sim_e6486a17'].format(**locals())
            cursor.execute(update_query, update_values)
            conn.commit()
            conn.close()
            edit_window.destroy()
            for widget in self.frames['UŻYTKOWNIK'].winfo_children():
                widget.destroy()
            self.display_user_assets(user_id=user_id)

        save_button = tk.Button(edit_window, text='Zapisz zmiany', command=save_changes)
        save_button.grid(row=len(labels) + 1, column=0, padx=10, pady=10)
        wyszukaj_uzytkownika = tk.Button(edit_window, text='Wyszukaj UŻYTKOWNIKa',
                                         command=lambda: self.search_user_w_sprzecie(edit_window))
        wyszukaj_uzytkownika.grid(row=len(labels) + 1, column=1, padx=10, pady=10)
        odpisanie_UŻYTKOWNIKa = tk.Button(edit_window, text='Odpisz UŻYTKOWNIKa',
                                          command=lambda: self.odpisz_uzytkownika(entries['ID_UZYTKOWNIKA']))
        odpisanie_UŻYTKOWNIKa.grid(row=len(labels) + 1, column=2, padx=10, pady=10)
        edit_window.update_idletasks()
        width = edit_window.winfo_width()
        height = edit_window.winfo_height()
        x_offset = (edit_window.winfo_screenwidth() - width) // 2
        y_offset = (edit_window.winfo_screenheight() - height) // 2
        edit_window.geometry(f'+{x_offset}+{y_offset}')
        edit_window.focus_set()

    def edit_record_window_router_uzytkownik(self, record_id, user_id, section='UŻYTKOWNIK'):
        edit_window = tk.Toplevel(self)
        edit_window.geometry('600x450')
        edit_window.title(f'Edytuj rekord routera ({section})')
        edit_window.transient(self)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(SQL['select_msprzet_statusy_c423c854'])
        status_values = [row[0] for row in cursor.fetchall()]
        cursor.execute(SQL['select_msprzet_operatorzy_komorkowi_9fbcfa7d'])
        operator_values = [row[0] for row in cursor.fetchall()]
        conn.close()
        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_router_c9bed672']
        cursor.execute(query, (record_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            messagebox.showerror('Błąd', 'Nie znaleziono rekordu o podanym ID.')
            edit_window.destroy()
            return
        labels = ['STATUS', 'IMIE', 'NAZWISKO', 'ID_UZYTKOWNIKA', 'IMEI', 'NR TELEFONU', 'NR SIM', 'OPERATOR', 'NR SDJ',
                  'UWAGI']
        entries = {}
        self.ID_UZYTKOWNIKA_entry = None
        self.IMIE_entry = None
        self.NAZWISKO_entry = None
        row = [value if value is not None else '' for value in row]
        bold_font = tkFont.Font(weight='bold', size=8)
        for i, label_text in enumerate(labels):
            tk.Label(edit_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            if label_text == 'STATUS':
                entry = tk.StringVar(edit_window)
                entry.set(row[i])
                entry_dropdown = tk.OptionMenu(edit_window, entry, *status_values)
                entry_dropdown.grid(row=i, column=1, padx=10, pady=5)
                entry_dropdown.config(font=bold_font)
            elif label_text == 'IMIE':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.IMIE_entry = entry
            elif label_text == 'NAZWISKO':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.NAZWISKO_entry = entry
            elif label_text == 'OPERATOR':
                entry = tk.StringVar(edit_window)
                entry.set(row[i])
                entry_dropdown = tk.OptionMenu(edit_window, entry, *operator_values)
                entry_dropdown.grid(row=i, column=1, padx=10, pady=5)
            elif label_text == 'ID_UZYTKOWNIKA':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.ID_UZYTKOWNIKA_entry = entry
            elif label_text == 'UWAGI':
                entry = tk.Text(edit_window, height=5, width=40, font='Helvetica 10')
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entries[label_text] = entry
            else:
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
            entries[label_text] = entry

        def save_changes():
            new_values = {}
            for label_text, entry in entries.items():
                if label_text in ['IMIE', 'NAZWISKO']:
                    continue
                if isinstance(entry, tk.Text):
                    new_values[label_text] = entry.get('1.0', tk.END).strip()
                elif isinstance(entry, tk.StringVar):
                    new_values[label_text] = entry.get()
                else:
                    new_values[label_text] = entry.get()
            nr_telefonu = new_values.get('NR TELEFONU', '')
            if nr_telefonu != '0' and (not nr_telefonu.isdigit() or len(nr_telefonu) != 9):
                messagebox.showerror('Błąd', 'Numer telefonu musi zawierać dokładnie 9 cyfr, jeśli jest podany.')
                return
            sim = new_values.get('NR SIM', '')
            if sim and (not sim.isdigit()):
                messagebox.showerror('Błąd', 'NR SIM może zawierać tylko cyfry.')
                return
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute(SQL['select_msprzet_router_784d6f21'],
                           (new_values['IMEI'], new_values['NR TELEFONU'], new_values['NR SIM'], record_id))
            count = cursor.fetchone()[0]
            if count > 0:
                messagebox.showerror('Błąd',
                                     'Router o podanym numerze IMEI, numerze telefonu lub numerze SIM już istnieje.')
                conn.close()
                return
            set_params = ', '.join((f'[{key}] = ?' for key in new_values.keys()))
            update_values = tuple(new_values.values()) + (record_id,)
            update_query = SQL['update_msprzet_router_7f24dbc4'].format(**locals())
            cursor.execute(update_query, update_values)
            conn.commit()
            conn.close()
            edit_window.destroy()
            for widget in self.frames['UŻYTKOWNIK'].winfo_children():
                widget.destroy()
            self.display_user_assets(user_id=user_id)

        save_button = tk.Button(edit_window, text='Zapisz zmiany', command=save_changes)
        save_button.grid(row=len(labels) + 1, column=0, padx=10, pady=10)
        wyszukaj_uzytkownika = tk.Button(edit_window, text='Wyszukaj UŻYTKOWNIKa',
                                         command=lambda: self.search_user_w_sprzecie(edit_window))
        wyszukaj_uzytkownika.grid(row=len(labels) + 1, column=1, padx=10, pady=10)
        odpisanie_UŻYTKOWNIKa = tk.Button(edit_window, text='Odpisz UŻYTKOWNIKa',
                                          command=lambda: self.odpisz_uzytkownika(entries['ID_UZYTKOWNIKA']))
        odpisanie_UŻYTKOWNIKa.grid(row=len(labels) + 1, column=2, padx=10, pady=10)
        edit_window.update_idletasks()
        width = edit_window.winfo_width()
        height = edit_window.winfo_height()
        x_offset = (edit_window.winfo_screenwidth() - width) // 2
        y_offset = (edit_window.winfo_screenheight() - height) // 2
        edit_window.geometry(f'+{x_offset}+{y_offset}')
        edit_window.focus_set()

    def edit_record_window_myszki_uzytkownik(self, record_id, user_id, section='MYSZKI'):
        edit_window = tk.Toplevel(self)
        edit_window.geometry('600x500')
        edit_window.title(f'Edytuj rekord myszki ({section})')
        edit_window.transient(self)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(SQL['select_msprzet_statusy_c423c854'])
        status_values = [row[0] for row in cursor.fetchall()]
        conn.close()
        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_myszki_88108181']
        cursor.execute(query, (record_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            messagebox.showerror('Błąd', 'Nie znaleziono rekordu o podanym ID.')
            edit_window.destroy()
            return
        labels = ['STATUS', 'IMIE', 'NAZWISKO', 'ID_UZYTKOWNIKA', 'NR SDJ', 'UWAGI']
        entries = {}
        self.ID_UZYTKOWNIKA_entry = None
        self.IMIE_entry = None
        self.NAZWISKO_entry = None
        row = [value if value is not None else '' for value in row]
        bold_font = tkFont.Font(weight='bold', size=8)
        for i, label_text in enumerate(labels):
            tk.Label(edit_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            if label_text == 'STATUS':
                entry = tk.StringVar(edit_window)
                entry.set(row[i])
                entry_dropdown = tk.OptionMenu(edit_window, entry, *status_values)
                entry_dropdown.grid(row=i, column=1, padx=10, pady=5)
                entry_dropdown.config(font=bold_font)
            elif label_text == 'IMIE':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.IMIE_entry = entry
            elif label_text == 'NAZWISKO':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.NAZWISKO_entry = entry
            elif label_text == 'ID_UZYTKOWNIKA':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.ID_UZYTKOWNIKA_entry = entry
            elif label_text == 'UWAGI':
                entry = tk.Text(edit_window, height=5, width=40, font='Helvetica 10')
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entries[label_text] = entry
            else:
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
            entries[label_text] = entry

        def save_changes():
            new_values = {}
            for label_text, entry in entries.items():
                if label_text in ['IMIE', 'NAZWISKO']:
                    continue
                if isinstance(entry, tk.Text):
                    new_values[label_text] = entry.get('1.0', tk.END).strip()
                elif isinstance(entry, tk.StringVar):
                    new_values[label_text] = entry.get()
                else:
                    new_values[label_text] = entry.get()
            conn = create_connection()
            cursor = conn.cursor()
            set_params = ', '.join((f'[{key}] = ?' for key in new_values.keys()))
            update_values = tuple(new_values.values()) + (record_id,)
            update_query = SQL['update_msprzet_myszki_28ea7bf2'].format(**locals())
            cursor.execute(update_query, update_values)
            conn.commit()
            conn.close()
            edit_window.destroy()
            for widget in self.frames['UŻYTKOWNIK'].winfo_children():
                widget.destroy()
            self.display_user_assets(user_id=user_id)

        save_button = tk.Button(edit_window, text='Zapisz zmiany', command=save_changes)
        save_button.grid(row=len(labels) + 1, column=0, padx=10, pady=10)
        wyszukaj_uzytkownika = tk.Button(edit_window, text='Wyszukaj UŻYTKOWNIKa',
                                         command=lambda: self.search_user_w_sprzecie(edit_window))
        wyszukaj_uzytkownika.grid(row=len(labels) + 1, column=1, padx=10, pady=10)
        odpisanie_UŻYTKOWNIKa = tk.Button(edit_window, text='Odpisz UŻYTKOWNIKa',
                                          command=lambda: self.odpisz_uzytkownika(entries['ID_UZYTKOWNIKA']))
        odpisanie_UŻYTKOWNIKa.grid(row=len(labels) + 1, column=2, padx=10, pady=10)
        edit_window.update_idletasks()
        width = edit_window.winfo_width()
        height = edit_window.winfo_height()
        x_offset = (edit_window.winfo_screenwidth() - width) // 2
        y_offset = (edit_window.winfo_screenheight() - height) // 2
        edit_window.geometry(f'+{x_offset}+{y_offset}')
        edit_window.focus_set()

    def edit_record_window_klawiatury_uzytkownik(self, record_id, user_id, section='KLAWIATURY'):
        edit_window = tk.Toplevel(self)
        edit_window.geometry('600x500')
        edit_window.title(f'Edytuj rekord klawiatury ({section})')
        edit_window.transient(self)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(SQL['select_msprzet_statusy_c423c854'])
        status_values = [row[0] for row in cursor.fetchall()]
        conn.close()
        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_klawiatury_b5121e75']
        cursor.execute(query, (record_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            messagebox.showerror('Błąd', 'Nie znaleziono rekordu o podanym ID.')
            edit_window.destroy()
            return
        labels = ['STATUS', 'IMIE', 'NAZWISKO', 'ID_UZYTKOWNIKA', 'NR SDJ', 'UWAGI']
        entries = {}
        self.ID_UZYTKOWNIKA_entry = None
        self.IMIE_entry = None
        self.NAZWISKO_entry = None
        row = [value if value is not None else '' for value in row]
        bold_font = tkFont.Font(weight='bold', size=8)
        for i, label_text in enumerate(labels):
            tk.Label(edit_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            if label_text == 'STATUS':
                entry = tk.StringVar(edit_window)
                entry.set(row[i])
                entry_dropdown = tk.OptionMenu(edit_window, entry, *status_values)
                entry_dropdown.grid(row=i, column=1, padx=10, pady=5)
                entry_dropdown.config(font=bold_font)
            elif label_text == 'IMIE':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.IMIE_entry = entry
            elif label_text == 'NAZWISKO':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.NAZWISKO_entry = entry
            elif label_text == 'ID_UZYTKOWNIKA':
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entry.config(state='readonly')
                self.ID_UZYTKOWNIKA_entry = entry
            elif label_text == 'UWAGI':
                entry = tk.Text(edit_window, height=5, width=40, font='Helvetica 10')
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
                entries[label_text] = entry
            else:
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
            entries[label_text] = entry

        def save_changes():
            new_values = {}
            for label_text, entry in entries.items():
                if label_text in ['IMIE', 'NAZWISKO']:
                    continue
                if isinstance(entry, tk.Text):
                    new_values[label_text] = entry.get('1.0', tk.END).strip()
                elif isinstance(entry, tk.StringVar):
                    new_values[label_text] = entry.get()
                else:
                    new_values[label_text] = entry.get()
            conn = create_connection()
            cursor = conn.cursor()
            set_params = ', '.join((f'[{key}] = ?' for key in new_values.keys()))
            update_values = tuple(new_values.values()) + (record_id,)
            update_query = SQL['update_msprzet_klawiatury_528ff4cb'].format(**locals())
            cursor.execute(update_query, update_values)
            conn.commit()
            conn.close()
            edit_window.destroy()
            for widget in self.frames['UŻYTKOWNIK'].winfo_children():
                widget.destroy()
            self.display_user_assets(user_id=user_id)

        save_button = tk.Button(edit_window, text='Zapisz zmiany', command=save_changes)
        save_button.grid(row=len(labels) + 1, column=0, padx=10, pady=10)
        wyszukaj_uzytkownika = tk.Button(edit_window, text='Wyszukaj UŻYTKOWNIKa',
                                         command=lambda: self.search_user_w_sprzecie(edit_window))
        wyszukaj_uzytkownika.grid(row=len(labels) + 1, column=1, padx=10, pady=10)
        odpisanie_UŻYTKOWNIKa = tk.Button(edit_window, text='Odpisz UŻYTKOWNIKa',
                                          command=lambda: self.odpisz_uzytkownika(entries['ID_UZYTKOWNIKA']))
        odpisanie_UŻYTKOWNIKa.grid(row=len(labels) + 1, column=2, padx=10, pady=10)
        edit_window.update_idletasks()
        width = edit_window.winfo_width()
        height = edit_window.winfo_height()
        x_offset = (edit_window.winfo_screenwidth() - width) // 2
        y_offset = (edit_window.winfo_screenheight() - height) // 2
        edit_window.geometry(f'+{x_offset}+{y_offset}')
        edit_window.focus_set()