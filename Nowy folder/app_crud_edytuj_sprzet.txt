import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from config_db import create_connection, SQL


class EdytujSprzetMixin:
    def action4(self, section):
        self.save_filter_values(section)
        selected_items = None
        if section == 'LAPTOPY':
            selected_items = self.tabela.selection()
        elif section == 'MONITORY':
            selected_items = self.tabela_monitory.selection()
        elif section == 'TELEFONY':
            selected_items = self.tabela_telefony.selection()
        elif section == 'SŁUCHAWKI':
            selected_items = self.tabela_sluchawki.selection()
        elif section == 'KARTY SIM':
            selected_items = self.tabela_karty_sim.selection()
        elif section == 'ROUTER':
            selected_items = self.tabela_router.selection()
        elif section == 'MYSZKI':
            selected_items = self.tabela_myszki.selection()
        elif section == 'KLAWIATURY':
            selected_items = self.tabela_klawiatury.selection()
        elif section == 'KONTA UŻYTKOWNIKÓW':
            selected_items = self.tabela_konta.selection()

        if not selected_items:
            messagebox.showinfo('Błąd', 'Nie wybrano żadnego rekordu do edycji.')
        elif len(selected_items) > 1:
            messagebox.showinfo('Błąd', 'Wybierz tylko jeden rekord do edycji.')
        else:
            record_id = None
            if section == 'LAPTOPY':
                record_id = self.tabela.item(selected_items[0])['values'][-1]
                self.edit_record_window_laptopy(record_id)
            elif section == 'MONITORY':
                record_id = self.tabela_monitory.item(selected_items[0])['values'][-1]
                self.edit_record_window_monitory(record_id)
            elif section == 'TELEFONY':
                record_id = self.tabela_telefony.item(selected_items[0])['values'][-1]
                self.edit_record_window_telefony(record_id)
            elif section == 'SŁUCHAWKI':
                record_id = self.tabela_sluchawki.item(selected_items[0])['values'][-1]
                self.edit_record_window_sluchawki(record_id)
            elif section == 'KARTY SIM':
                record_id = self.tabela_karty_sim.item(selected_items[0])['values'][-1]
                self.edit_record_window_karty_sim(record_id)
            elif section == 'ROUTER':
                record_id = self.tabela_router.item(selected_items[0])['values'][-1]
                self.edit_record_window_router(record_id)
            elif section == 'MYSZKI':
                record_id = self.tabela_myszki.item(selected_items[0])['values'][-1]
                self.edit_record_window_myszki(record_id)
            elif section == 'KLAWIATURY':
                record_id = self.tabela_klawiatury.item(selected_items[0])['values'][-1]
                self.edit_record_window_klawiatury(record_id)
            elif section == 'KONTA UŻYTKOWNIKÓW':
                record_id = self.tabela_konta.item(selected_items[0])['values'][-1]
                self.edytuj_konto_uzytkownika(record_id)

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

    def edit_record_window_laptopy(self, record_id, section='LAPTOPY'):
        edit_window = tk.Toplevel(self)
        edit_window.geometry('600x500')
        edit_window.title(f'Edytuj rekord ({section})')
        edit_window.transient(self)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(SQL['select_msprzet_statusy_c423c854'])
        status_values = [row[0] for row in cursor.fetchall()]
        conn.close()

        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_laptopy_4fc7a6c3']
        cursor.execute(query, (record_id,))
        row = cursor.fetchone()

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(SQL['select_msprzet_model_laptopa_db2d6e8e'])
        model_laptopa_values = [row[0] for row in cursor.fetchall()]
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
            elif label_text == 'MODEL':
                entry = tk.StringVar(edit_window)
                entry.set(row[i])
                entry_dropdown = tk.OptionMenu(edit_window, entry, *model_laptopa_values)
                entry_dropdown.grid(row=i, column=1, padx=10, pady=5)
                entries[label_text] = entry
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
            cursor.execute(SQL['select_msprzet_laptopy_8ca8f72d'],
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

    def edit_record_window_monitory(self, record_id, section='MONITORY'):
        edit_window = tk.Toplevel(self)
        edit_window.geometry('600x450')
        edit_window.title(f'Edytuj rekord monitora ({section})')
        edit_window.transient(self)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(SQL['select_msprzet_statusy_c423c854'])
        status_values = [row[0] for row in cursor.fetchall()]
        conn.close()

        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_monitory_ec1a5c29']
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
                entry = tk.Text(edit_window, height=5, width=45, font='Helvetica 10')
                entry.grid(row=i, column=1, padx=10, pady=10)
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

    def edit_record_window_telefony(self, record_id, section='TELEFONY'):
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
        query = SQL['select_msprzet_telefony_e6c7d487']
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
                entries[label_text] = entry
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

    def edit_record_window_sluchawki(self, record_id, section='SŁUCHAWKI'):
        edit_window = tk.Toplevel(self)
        edit_window.geometry('600x450')
        edit_window.title(f'Edytuj rekord słuchawki ({section})')
        edit_window.transient(self)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(SQL['select_msprzet_statusy_c423c854'])
        status_values = [row[0] for row in cursor.fetchall()]
        conn.close()

        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_sluchawki_fbd4ec49']
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
            cursor.execute(SQL['select_msprzet_sluchawki_e5692280'], (new_values['NR SERYJNY'], record_id))
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