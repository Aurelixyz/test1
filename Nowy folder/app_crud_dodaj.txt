import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from config_db import create_connection, SQL
from models_specs import FieldSpec


class DodajMixin:

    def _db_fetch_first_col(self, sql_key: str, params: tuple = ()) -> list:
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute(SQL[sql_key], params)
            return [r[0] for r in cur.fetchall()]
        except Exception as e:
            print(f'[ERROR] _db_fetch_first_col({sql_key}): {e}')
            return []
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def _center_window(self, win):
        win.update_idletasks()
        w = win.winfo_width()
        h = win.winfo_height()
        x = (win.winfo_screenwidth() - w) // 2
        y = (win.winfo_screenheight() - h) // 2
        win.geometry(f'+{x}+{y}')

    def _raise_dialog(self, win):
        try:
            win.lift()
            win.attributes('-topmost', True)
            win.attributes('-topmost', False)
            win.focus_force()
        except Exception:
            pass

    def _bind_scanner_entry(self, entry, scanned_entries: set, manual_clear: set, *, allow_ctrl: bool = True):
        def on_focus_in(event):
            widget = event.widget
            if widget in scanned_entries and widget not in manual_clear:
                return
            if widget in manual_clear:
                manual_clear.remove(widget)

        def on_key(event):
            widget = event.widget
            if allow_ctrl and event.state & 4 and (event.keysym.lower() in ('v', 'c', 'a')):
                if event.keysym.lower() == 'a':
                    try:
                        widget.select_range(0, tk.END)
                        return 'break'
                    except Exception:
                        return
                return
            if event.keysym == 'Tab':
                nxt = widget.tk_focusNext()
                while nxt and isinstance(nxt, (tk.Checkbutton, tk.Button, tk.Text)):
                    nxt = nxt.tk_focusNext()
                if nxt:
                    nxt.focus()
                return 'break'
            if widget in scanned_entries:
                return 'break'
            if event.char in ('\\r', '\\n'):
                if widget.get():
                    scanned_entries.add(widget)
                nxt = widget.tk_focusNext()
                while nxt and isinstance(nxt, (tk.Checkbutton, tk.Button, tk.Text)):
                    nxt = nxt.tk_focusNext()
                if nxt:
                    try:
                        if hasattr(nxt, 'get') and (not nxt.get()):
                            nxt.focus()
                    except Exception:
                        nxt.focus()
                return 'break'
            return

        def on_delete(event):
            widget = event.widget
            manual_clear.add(widget)
            if widget in scanned_entries:
                scanned_entries.remove(widget)
            try:
                widget.delete(0, tk.END)
            except Exception:
                pass

        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<Key>', on_key)
        entry.bind('<Delete>', on_delete)

    def _build_form(self, parent, fields: list, *, bold_font=None):
        entries = {}
        scanned_entries = set()
        manual_clear = set()
        bold_font = bold_font or tkFont.Font(weight='bold', size=8)
        for i, fs in enumerate(fields):
            tk.Label(parent, text=fs.label).grid(row=i, column=0, padx=10, pady=5, sticky='w')
            if fs.kind == 'dropdown':
                opts = self._db_fetch_first_col(fs.options_sql) if fs.options_sql else []
                var = tk.StringVar(parent)
                var.set(opts[0] if opts else str(fs.default))
                om = tk.OptionMenu(parent, var, *opts)
                om.grid(row=i, column=1, padx=10, pady=5, sticky='we')
                try:
                    om.config(font=bold_font)
                    menu = parent.nametowidget(om.menuname)
                    menu.config(font=bold_font)
                except Exception:
                    pass
                entries[fs.label] = var
            elif fs.kind == 'checkbox':
                var = tk.IntVar(value=int(fs.default) if str(fs.default).isdigit() else 0)
                tk.Checkbutton(parent, variable=var).grid(row=i, column=1, padx=10, pady=5, sticky='w')
                entries[fs.label] = var
            elif fs.kind == 'text':
                txt = tk.Text(parent, height=fs.height, width=fs.width, font='Helvetica 10')
                txt.grid(row=i, column=1, padx=10, pady=5, sticky='we')
                if fs.default:
                    txt.insert(tk.END, str(fs.default))
                entries[fs.label] = txt
            else:
                ent = tk.Entry(parent, width=fs.width)
                ent.grid(row=i, column=1, padx=10, pady=5, sticky='we')
                if fs.default not in (None, ''):
                    ent.insert(tk.END, str(fs.default))
                if fs.readonly:
                    ent.config(state='readonly')
                else:
                    self._bind_scanner_entry(ent, scanned_entries, manual_clear, allow_ctrl=True)
                entries[fs.label] = ent
        return entries

    def _collect_form_values(self, entries: dict) -> dict:
        out = {}
        for k, w in entries.items():
            if isinstance(w, tk.Text):
                out[k] = w.get('1.0', tk.END).strip()
            elif isinstance(w, tk.StringVar):
                out[k] = w.get()
            elif isinstance(w, tk.IntVar):
                out[k] = w.get()
            else:
                try:
                    out[k] = w.get()
                except Exception:
                    out[k] = ''
        return out

    def _insert_record_from_values(self, insert_sql_key: str, values: dict):
        columns = ', '.join((f'[{k}]' for k in values.keys()))
        placeholders = ', '.join(('?' for _ in values.values()))
        insert_query = SQL[insert_sql_key].format(**locals())
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(insert_query, tuple(values.values()))
        conn.commit()
        conn.close()

    def _open_add_dialog_generic(self, *, title: str, fields: list, insert_sql_key: str, duplicate_check=None,
                                 validate=None, after=None):
        win = tk.Toplevel(self)
        win.title(title)
        win.withdraw()
        win.transient(self)
        bold_font = tkFont.Font(weight='bold', size=8)
        entries = self._build_form(win, fields, bold_font=bold_font)

        def _save():
            values = self._collect_form_values(entries)
            if validate:
                msg = validate(values)
                if msg:
                    messagebox.showerror('Błąd', msg)
                    self._raise_dialog(win)
                    return
            if duplicate_check:
                msg = duplicate_check(values)
                if msg:
                    messagebox.showerror('Błąd', msg)
                    self._raise_dialog(win)
                    return
            try:
                self._insert_record_from_values(insert_sql_key, values)
            except Exception as e:
                messagebox.showerror('Błąd', str(e))
                self._raise_dialog(win)
                return
            try:
                if after:
                    after()
            finally:
                win.destroy()

        tk.Button(win, text='Dodaj', command=_save).grid(row=len(fields) + 1, columnspan=2, padx=10, pady=10)
        self._center_window(win)
        win.deiconify()

    def dodaj_laptopa(self):
        fields = [FieldSpec('STATUS', kind='dropdown', options_sql='select_msprzet_statusy_c423c854'),
                  FieldSpec('NR SRODKA TRWALEGO'), FieldSpec('NAZWA LAPTOPA'), FieldSpec('NR SERYJNY'),
                  FieldSpec('MODEL', kind='dropdown', options_sql='select_msprzet_model_laptopa_db2d6e8e'),
                  FieldSpec('NR SDJ'), FieldSpec('UWAGI')]

        def dup(values):
            try:
                conn = create_connection()
                cur = conn.cursor()
                cur.execute(SQL['select_msprzet_laptopy_ea167cbd'],
                            (values.get('NR SRODKA TRWALEGO', ''), values.get('NR SERYJNY', '')))
                count = cur.fetchone()[0]
                return 'Laptop o podanym numerze środka trwałego lub numerze seryjnym już istnieje.' if count > 0 else None
            except Exception as e:
                return str(e)
            finally:
                try:
                    conn.close()
                except Exception:
                    pass

        self._open_add_dialog_generic(title='Dodaj nowego laptopa', fields=fields,
                                      insert_sql_key='insert_into_msprzet_laptopy_44cbfd66', duplicate_check=dup,
                                      after=lambda: self.populate_frame_with_data('LAPTOPY'))

    def dodaj_monitor(self):
        fields = [FieldSpec('STATUS', kind='dropdown', options_sql='select_msprzet_statusy_c423c854'),
                  FieldSpec('NR SERYJNY'), FieldSpec('MODEL'), FieldSpec('NR SDJ'), FieldSpec('UWAGI')]

        def dup(values):
            try:
                conn = create_connection()
                cur = conn.cursor()
                cur.execute(SQL['select_msprzet_monitory_ae1ec956'], (values.get('NR SERYJNY', ''),))
                count = cur.fetchone()[0]
                return 'Monitor o podanym numerze seryjnym już istnieje.' if count > 0 else None
            except Exception as e:
                return str(e)
            finally:
                try:
                    conn.close()
                except Exception:
                    pass

        self._open_add_dialog_generic(title='Dodaj nowy monitor', fields=fields,
                                      insert_sql_key='insert_into_msprzet_monitory_832fcbbb', duplicate_check=dup,
                                      after=lambda: self.populate_frame_with_data('MONITORY'))

    def dodaj_telefon(self):
        fields = [FieldSpec('STATUS', kind='dropdown', options_sql='select_msprzet_statusy_c423c854'),
                  FieldSpec('IMEI'), FieldSpec('LADOWARKA', kind='checkbox', default=0),
                  FieldSpec('KABEL USB C', kind='checkbox', default=0),
                  FieldSpec('LADOWARKA INDUKCYJNA', kind='checkbox', default=0),
                  FieldSpec('PRZEJSCIOWKA DO TELEFONU', kind='checkbox', default=0),
                  FieldSpec('ETUI', kind='checkbox', default=0), FieldSpec('NR TELEFONU'),
                  FieldSpec('MODEL', kind='dropdown', options_sql='select_msprzet_model_telefonu_5e4ba938'),
                  FieldSpec('NR SDJ'), FieldSpec('UWAGI', kind='text', height=5, width=40)]

        def validate(values):
            nr = (values.get('NR TELEFONU') or '').strip()
            if nr and nr != '0' and (not nr.isdigit() or len(nr) != 9):
                return 'Numer telefonu musi zawierać dokładnie 9 cyfr, jeśli jest podany.'
            return None

        def dup(values):
            try:
                conn = create_connection()
                cur = conn.cursor()
                cur.execute(SQL['select_msprzet_telefony_642a4cb1'],
                            (values.get('IMEI', ''), values.get('NR TELEFONU', '')))
                count = cur.fetchone()[0]
                return 'Telefon o podanym numerze IMEI lub numerze telefonu już istnieje.' if count > 0 else None
            except Exception as e:
                return str(e)
            finally:
                try:
                    conn.close()
                except Exception:
                    pass

        self._open_add_dialog_generic(title='Dodaj nowy telefon', fields=fields,
                                      insert_sql_key='insert_into_msprzet_telefony_c2cfe8e8', validate=validate,
                                      duplicate_check=dup, after=lambda: self.populate_frame_with_data('TELEFONY'))

    def dodaj_sluchawki(self, section=None):
        fields = [FieldSpec('STATUS', kind='dropdown', options_sql='select_msprzet_statusy_c423c854'),
                  FieldSpec('NR SERYJNY'), FieldSpec('MODEL'), FieldSpec('NR SDJ'), FieldSpec('UWAGI')]

        def dup(values):
            try:
                conn = create_connection()
                cur = conn.cursor()
                cur.execute(SQL['select_msprzet_sluchawki_01af8b0f'], (values.get('NR SERYJNY', ''),))
                count = cur.fetchone()[0]
                return 'Słuchawki o podanym numerze seryjnym już istnieją.' if count > 0 else None
            except Exception as e:
                return str(e)
            finally:
                try:
                    conn.close()
                except Exception:
                    pass

        self._open_add_dialog_generic(title='Dodaj nowe słuchawki', fields=fields,
                                      insert_sql_key='insert_into_msprzet_sluchawki_265fd8fe', duplicate_check=dup,
                                      after=lambda: self.populate_frame_with_data('SŁUCHAWKI'))

    def dodaj_karty_sim(self, section=None):
        fields = [FieldSpec('STATUS', kind='dropdown', options_sql='select_msprzet_statusy_c423c854'),
                  FieldSpec('NR TELEFONU'), FieldSpec('NR SIM'),
                  FieldSpec('OPERATOR', kind='dropdown', options_sql='select_msprzet_operatorzy_komorkowi_9fbcfa7d'),
                  FieldSpec('NR SDJ'), FieldSpec('UWAGI')]

        def validate(values):
            nr = (values.get('NR TELEFONU') or '').strip()
            if nr and nr != '0' and (not nr.isdigit() or len(nr) != 9):
                return 'Numer telefonu musi zawierać dokładnie 9 cyfr, jeśli jest podany.'
            sim = (values.get('NR SIM') or '').strip()
            if sim and (not sim.isdigit()):
                return 'NR SIM może zawierać tylko cyfry.'
            return None

        def dup(values):
            try:
                conn = create_connection()
                cur = conn.cursor()
                cur.execute(SQL['select_msprzet_karty_sim_d61fd91e'],
                            (values.get('NR TELEFONU', ''), values.get('NR SIM', '')))
                count = cur.fetchone()[0]
                return 'Karta SIM o podanym numerze telefonu lub numerze SIM już istnieje.' if count > 0 else None
            except Exception as e:
                return str(e)
            finally:
                try:
                    conn.close()
                except Exception:
                    pass

        self._open_add_dialog_generic(title='Dodaj nowe karty SIM', fields=fields,
                                      insert_sql_key='insert_into_msprzet_karty_sim_9e0e1641', validate=validate,
                                      duplicate_check=dup, after=lambda: self.populate_frame_with_data('KARTY SIM'))

    def dodaj_router(self, section=None):
        fields = [FieldSpec('STATUS', kind='dropdown', options_sql='select_msprzet_statusy_c423c854'),
                  FieldSpec('IMEI'), FieldSpec('NR TELEFONU'), FieldSpec('NR SIM'),
                  FieldSpec('OPERATOR', kind='dropdown', options_sql='select_msprzet_operatorzy_komorkowi_9fbcfa7d'),
                  FieldSpec('NR SDJ'), FieldSpec('UWAGI')]

        def validate(values):
            nr = (values.get('NR TELEFONU') or '').strip()
            if nr and nr != '0' and (not nr.isdigit() or len(nr) != 9):
                return 'Numer telefonu musi zawierać dokładnie 9 cyfr, jeśli jest podany.'
            sim = (values.get('NR SIM') or '').strip()
            if sim and (not sim.isdigit()):
                return 'NR SIM może zawierać tylko cyfry.'
            return None

        def dup(values):
            try:
                conn = create_connection()
                cur = conn.cursor()
                cur.execute(SQL['select_msprzet_router_68f0c478'],
                            (values.get('IMEI', ''), values.get('NR TELEFONU', ''), values.get('NR SIM', '')))
                count = cur.fetchone()[0]
                return 'Router o podanym numerze IMEI, numerze telefonu lub numerze SIM już istnieje.' if count > 0 else None
            except Exception as e:
                return str(e)
            finally:
                try:
                    conn.close()
                except Exception:
                    pass

        self._open_add_dialog_generic(title='Dodaj nowy router', fields=fields,
                                      insert_sql_key='insert_into_msprzet_router_1a6ce9ad', validate=validate,
                                      duplicate_check=dup, after=lambda: self.populate_frame_with_data('ROUTER'))

    def dodaj_myszke(self, section=None):
        fields = [FieldSpec('STATUS', kind='dropdown', options_sql='select_msprzet_statusy_c423c854'),
                  FieldSpec('NR SDJ'), FieldSpec('UWAGI')]
        self._open_add_dialog_generic(title='Dodaj nowy myszkę', fields=fields,
                                      insert_sql_key='insert_into_msprzet_myszki_3e8653d7',
                                      after=lambda: self.populate_frame_with_data('MYSZKI'))

    def dodaj_klawiature(self, section=None):
        fields = [FieldSpec('STATUS', kind='dropdown', options_sql='select_msprzet_statusy_c423c854'),
                  FieldSpec('NR SDJ'), FieldSpec('UWAGI')]
        self._open_add_dialog_generic(title='Dodaj nowy klawiature', fields=fields,
                                      insert_sql_key='insert_into_msprzet_klawiatury_43ca08ff',
                                      after=lambda: self.populate_frame_with_data('KLAWIATURY'))

    def dodaj_konto_uzytkownika(self):
        add_window = tk.Toplevel(self)
        add_window.title('Dodaj nowe konto UŻYTKOWNIKa')
        add_window.transient(self)
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
        labels = ['NR KADROWY', 'IMIE', 'NAZWISKO', 'RODZAJ ZATRUDNIENIA', 'LOKALIZACJA']
        entries = {}
        for i, label_text in enumerate(labels):
            tk.Label(add_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            if label_text == 'RODZAJ ZATRUDNIENIA':
                entry = tk.StringVar(add_window)
                entry.set(status_zatrudnienie[0])
                entry_dropdown = tk.OptionMenu(add_window, entry, *status_zatrudnienie)
                entry_dropdown.grid(row=i, column=1, padx=10, pady=5)
            elif label_text == 'LOKALIZACJA':
                entry = tk.StringVar(add_window)
                entry.set(status_lokalizacja[0])
                entry_dropdown = tk.OptionMenu(add_window, entry, *status_lokalizacja)
                entry_dropdown.grid(row=i, column=1, padx=10, pady=5)
            else:
                tk.Label(add_window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
                entry = tk.Entry(add_window)
                entry.grid(row=i, column=1, padx=10, pady=5)
            entries[label_text] = entry

        def save_new_record():
            new_values = {label_text: entry.get() for label_text, entry in entries.items()}
            if 'NR KADROWY' in new_values and isinstance(new_values['NR KADROWY'], str):
                new_values['NR KADROWY'] = new_values['NR KADROWY'].replace(' ', '').upper()
            conn = create_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(SQL['select_msprzet_konta_uzytkownikow_8a3b0b44'], (new_values['NR KADROWY'],))
                count = cursor.fetchone()[0]
                if count > 0:
                    messagebox.showerror('Błąd', 'Konto już istnieje.')
                    add_window.lift()
                    add_window.attributes('-topmost', True)
                    add_window.attributes('-topmost', False)
                    add_window.focus_force()
                    return
                columns = ', '.join((f'[{key}]' for key in new_values.keys()))
                placeholders = ', '.join(('?' for _ in new_values.values()))
                insert_query = SQL['insert_into_msprzet_konta_uzytkownikow_b3dd419e'].format(**locals())
                cursor.execute(insert_query, tuple(new_values.values()))
                conn.commit()
                conn.close()
            except Exception as e:
                messagebox.showerror('Błąd', str(e))
                add_window.lift()
                add_window.attributes('-topmost', True)
                add_window.attributes('-topmost', False)
                add_window.focus_force()
            self.populate_frame_with_data('KONTA UŻYTKOWNIKÓW')
            add_window.destroy()

        save_button = tk.Button(add_window, text='Dodaj', command=save_new_record)
        save_button.grid(row=len(labels) + 1, columnspan=2, padx=10, pady=10)
        add_window.update_idletasks()
        width = add_window.winfo_width()
        height = add_window.winfo_height()
        x_offset = (add_window.winfo_screenwidth() - width) // 2
        y_offset = (add_window.winfo_screenheight() - height) // 2
        add_window.geometry(f'+{x_offset}+{y_offset}')