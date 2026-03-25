import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from config_db import create_connection, SQL


class EdytujAkcesoriaMixin:

    def edit_record_window_karty_sim(self, record_id, section='KARTY SIM'):
        edit_window = tk.Toplevel(self)
        edit_window.geometry('600x450')
        edit_window.title(f'Edytuj rekord karty sim ({section})')
        edit_window.transient(self)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(SQL['select_msprzet_statusy_c423c854'])
        status_values = [row[0] for row in cursor.fetchall()]
        cursor.execute(SQL['select_msprzet_operatorzy_komorkowi_9fbcfa7d'])
        operator_values = [row[0] for row in cursor.fetchall()]
        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_karty_sim_4bb7f571']
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
        scanned_entries = set()
        manual_clear = set()
        bold_font = tkFont.Font(weight='bold', size=8)

        def on_focus_in(event):
            widget = event.widget
            if widget in scanned_entries and widget not in manual_clear:
                return
            if widget in manual_clear:
                manual_clear.remove(widget)

        def on_key(event):
            widget = event.widget
            if event.state & 4 and event.keysym.lower() in ('v', 'c', 'a'):
                if event.keysym.lower() == 'a':
                    widget.select_range(0, tk.END)
                    return 'break'
                return
            if event.keysym == 'Tab':
                next_widget = widget.tk_focusNext()
                while next_widget and (
                        isinstance(next_widget, tk.Checkbutton) or isinstance(next_widget, tk.Button) or isinstance(
                        next_widget, tk.Text)):
                    next_widget = next_widget.tk_focusNext()
                if next_widget:
                    next_widget.focus()
                return 'break'
            if widget in scanned_entries:
                if event.state & 4 and event.keysym.lower() in ('v', 'c', 'a'):
                    if event.keysym.lower() == 'a':
                        widget.select_range(0, tk.END)
                        return 'break'
                    return
                return 'break'
            if widget not in scanned_entries:
                if event.char in ('\r', '\n') or event.keysym == 'Tab':
                    if widget.get():
                        scanned_entries.add(widget)
                    next_widget = widget.tk_focusNext()
                    while next_widget and (
                            isinstance(next_widget, tk.Checkbutton) or isinstance(next_widget, tk.Button) or isinstance(
                            next_widget, tk.Text)):
                        next_widget = next_widget.tk_focusNext()
                    if next_widget:
                        if not next_widget.get():
                            next_widget.focus()
                    return 'break'
                if widget.get() == '':
                    widget.insert(tk.END, event.char)
                    return 'break'
            return

        def on_delete(event):
            widget = event.widget
            manual_clear.add(widget)
            if widget in scanned_entries:
                scanned_entries.remove(widget)
            widget.delete(0, tk.END)

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
                entry.bind('<FocusIn>', on_focus_in)
                entry.bind('<Key>', on_key)
                entry.bind('<Delete>', on_delete)
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
            self.populate_frame_with_data(section)
            edit_window.destroy()
            self.restore_filter_values(section)

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

    def edit_record_window_router(self, record_id, section='ROUTER'):
        edit_window = tk.Toplevel(self)
        edit_window.geometry('600x500')
        edit_window.title(f'Edytuj rekord router ({section})')
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
        query = SQL['select_msprzet_router_94561b1c']
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
        scanned_entries = set()
        manual_clear = set()
        bold_font = tkFont.Font(weight='bold', size=8)

        def on_focus_in(event):
            widget = event.widget
            if widget in scanned_entries and widget not in manual_clear:
                return
            if widget in manual_clear:
                manual_clear.remove(widget)

        def on_key(event):
            widget = event.widget
            if event.state & 4 and event.keysym.lower() in ('v', 'c', 'a'):
                if event.keysym.lower() == 'a':
                    widget.select_range(0, tk.END)
                    return 'break'
                return
            if event.keysym == 'Tab':
                next_widget = widget.tk_focusNext()
                while next_widget and (
                        isinstance(next_widget, tk.Checkbutton) or isinstance(next_widget, tk.Button) or isinstance(
                        next_widget, tk.Text)):
                    next_widget = next_widget.tk_focusNext()
                if next_widget:
                    next_widget.focus()
                return 'break'
            if widget in scanned_entries:
                if event.state & 4 and event.keysym.lower() in ('v', 'c', 'a'):
                    if event.keysym.lower() == 'a':
                        widget.select_range(0, tk.END)
                        return 'break'
                    return
                return 'break'
            if widget not in scanned_entries:
                if event.char in ('\r', '\n') or event.keysym == 'Tab':
                    if widget.get():
                        scanned_entries.add(widget)
                    next_widget = widget.tk_focusNext()
                    while next_widget and (
                            isinstance(next_widget, tk.Checkbutton) or isinstance(next_widget, tk.Button) or isinstance(
                            next_widget, tk.Text)):
                        next_widget = next_widget.tk_focusNext()
                    if next_widget:
                        if not next_widget.get():
                            next_widget.focus()
                    return 'break'
                if widget.get() == '':
                    widget.insert(tk.END, event.char)
                    return 'break'
            return

        def on_delete(event):
            widget = event.widget
            manual_clear.add(widget)
            if widget in scanned_entries:
                scanned_entries.remove(widget)
            widget.delete(0, tk.END)

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
                entry.bind('<FocusIn>', on_focus_in)
                entry.bind('<Key>', on_key)
                entry.bind('<Delete>', on_delete)
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
            cursor.execute(SQL['select_msprzet_router_5b0b0951'],
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
            self.populate_frame_with_data(section)
            edit_window.destroy()
            self.restore_filter_values(section)

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

    def edit_record_window_myszki(self, record_id, section='MYSZKI'):
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
        query = SQL['select_msprzet_myszki_114d7586']
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
        scanned_entries = set()
        manual_clear = set()
        bold_font = tkFont.Font(weight='bold', size=8)

        def on_focus_in(event):
            widget = event.widget
            if widget in scanned_entries and widget not in manual_clear:
                return
            if widget in manual_clear:
                manual_clear.remove(widget)

        def on_key(event):
            widget = event.widget
            if event.state & 4 and event.keysym.lower() in ('v', 'c', 'a'):
                if event.keysym.lower() == 'a':
                    widget.select_range(0, tk.END)
                    return 'break'
                return
            if event.keysym == 'Tab':
                next_widget = widget.tk_focusNext()
                while next_widget and (
                        isinstance(next_widget, tk.Checkbutton) or isinstance(next_widget, tk.Button) or isinstance(
                        next_widget, tk.Text)):
                    next_widget = next_widget.tk_focusNext()
                if next_widget:
                    next_widget.focus()
                return 'break'
            if widget in scanned_entries:
                if event.state & 4 and event.keysym.lower() in ('v', 'c', 'a'):
                    if event.keysym.lower() == 'a':
                        widget.select_range(0, tk.END)
                        return 'break'
                    return
                return 'break'
            if widget not in scanned_entries:
                if event.char in ('\r', '\n') or event.keysym == 'Tab':
                    if widget.get():
                        scanned_entries.add(widget)
                    next_widget = widget.tk_focusNext()
                    while next_widget and (
                            isinstance(next_widget, tk.Checkbutton) or isinstance(next_widget, tk.Button) or isinstance(
                            next_widget, tk.Text)):
                        next_widget = next_widget.tk_focusNext()
                    if next_widget:
                        if not next_widget.get():
                            next_widget.focus()
                    return 'break'
                if widget.get() == '':
                    widget.insert(tk.END, event.char)
                    return 'break'
            return

        def on_delete(event):
            widget = event.widget
            manual_clear.add(widget)
            if widget in scanned_entries:
                scanned_entries.remove(widget)
            widget.delete(0, tk.END)

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
                entry.bind('<FocusIn>', on_focus_in)
                entry.bind('<Key>', on_key)
                entry.bind('<Delete>', on_delete)
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
            self.populate_frame_with_data(section)
            edit_window.destroy()
            self.restore_filter_values(section)

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

    def edit_record_window_klawiatury(self, record_id, section='KLAWIATURY'):
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
        query = SQL['select_msprzet_klawiatury_4e96c1b4']
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
        scanned_entries = set()
        manual_clear = set()
        bold_font = tkFont.Font(weight='bold', size=8)

        def on_focus_in(event):
            widget = event.widget
            if widget in scanned_entries and widget not in manual_clear:
                return
            if widget in manual_clear:
                manual_clear.remove(widget)

        def on_key(event):
            widget = event.widget
            if event.keysym == 'Tab':
                next_widget = widget.tk_focusNext()
                while next_widget and (
                        isinstance(next_widget, tk.Checkbutton) or isinstance(next_widget, tk.Button) or isinstance(
                        next_widget, tk.Text)):
                    next_widget = next_widget.tk_focusNext()
                if next_widget:
                    next_widget.focus()
                return 'break'
            if widget in scanned_entries:
                return 'break'
            if widget not in scanned_entries:
                if event.char in ('\r', '\n') or event.keysym == 'Tab':
                    if widget.get():
                        scanned_entries.add(widget)
                    next_widget = widget.tk_focusNext()
                    while next_widget and (
                            isinstance(next_widget, tk.Checkbutton) or isinstance(next_widget, tk.Button) or isinstance(
                            next_widget, tk.Text)):
                        next_widget = next_widget.tk_focusNext()
                    if next_widget:
                        if not next_widget.get():
                            next_widget.focus()
                    return 'break'
                if widget.get() == '':
                    widget.insert(tk.END, event.char)
                    return 'break'
            return

        def on_delete(event):
            widget = event.widget
            manual_clear.add(widget)
            if widget in scanned_entries:
                scanned_entries.remove(widget)
            widget.delete(0, tk.END)

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
                entry.bind('<FocusIn>', on_focus_in)
                entry.bind('<Key>', on_key)
                entry.bind('<Delete>', on_delete)
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
            self.populate_frame_with_data(section)
            edit_window.destroy()
            self.restore_filter_values(section)

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

    def edytuj_konto_uzytkownika(self, record_id, section='KONTA UŻYTKOWNIKÓW'):
        edit_window = tk.Toplevel(self)
        edit_window.title('Edytuj rekord konta UŻYTKOWNIKa')

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(SQL['select_msprzet_statusy_rodzaj_zatrudnienia_b7dfaf9c'])
        status_zatrudnienie = [row[0] for row in cursor.fetchall()]
        conn.close()

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(SQL['select_msprzet_statusy_lokalizacja_fbf91e82'])
        status_lokalizacja = [row[0] for row in cursor.fetchall()]
        conn.close()

        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_konta_uzytkownikow_a1deca87']
        cursor.execute(query, (record_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            messagebox.showerror('Błąd', 'Nie znaleziono rekordu o podanym ID.')
            edit_window.destroy()
            return

        labels = ['NR KADROWY', 'IMIE', 'NAZWISKO', 'RODZAJ ZATRUDNIENIA', 'LOKALIZACJA']
        entries = {}
        for i, label_text in enumerate(labels):
            tk.Label(edit_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            if label_text == 'RODZAJ ZATRUDNIENIA':
                entry = tk.StringVar(edit_window)
                entry.set(row[i])
                entry_dropdown = tk.OptionMenu(edit_window, entry, *status_zatrudnienie)
                entry_dropdown.grid(row=i, column=1, padx=10, pady=5)
            elif label_text == 'LOKALIZACJA':
                entry = tk.StringVar(edit_window)
                entry.set(row[i])
                entry_dropdown = tk.OptionMenu(edit_window, entry, *status_lokalizacja)
                entry_dropdown.grid(row=i, column=1, padx=10, pady=5)
            else:
                entry = tk.Entry(edit_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.insert(tk.END, row[i])
            entries[label_text] = entry

        def save_changes():
            new_values = {label_text: entry.get() for label_text, entry in entries.items()}
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute(SQL['select_msprzet_konta_uzytkownikow_d32d8150'], (new_values['NR KADROWY'], record_id))
            count = cursor.fetchone()[0]
            conn.close()
            if count > 0:
                messagebox.showerror('Błąd', 'UŻYTKOWNIK o podanym numerze kadrowym już istnieje.')
                return

            conn = create_connection()
            cursor = conn.cursor()
            set_params = ', '.join((f'[{key}] = ?' for key in new_values.keys()))
            update_values = tuple(new_values.values()) + (record_id,)
            update_query = SQL['update_msprzet_konta_uzytkownikow_4c937bb8'].format(**locals())
            cursor.execute(update_query, update_values)
            conn.commit()
            conn.close()
            self.populate_frame_with_data('KONTA UŻYTKOWNIKÓW')
            edit_window.destroy()
            self.restore_filter_values(section)

        save_button = tk.Button(edit_window, text='Zapisz zmiany', command=save_changes)
        save_button.grid(row=len(labels) + 1, columnspan=2, padx=10, pady=10)
        edit_window.update_idletasks()
        width = edit_window.winfo_width()
        height = edit_window.winfo_height()
        x_offset = (edit_window.winfo_screenwidth() - width) // 2
        y_offset = (edit_window.winfo_screenheight() - height) // 2
        edit_window.geometry(f'+{x_offset}+{y_offset}')