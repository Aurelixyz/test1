import tkinter as tk
from tkinter import ttk, messagebox
from config_db import create_connection, SQL


class PrzypisywanieMixin:

    def display_user_assets(self, user_id):
        parent_frame = self.frames.get('UŻYTKOWNIK')
        if not parent_frame:
            return

        # 1. Czyszczenie ramki (usuwamy stary sprzęt poprzedniego pracownika)
        for widget in parent_frame.winfo_children():
            widget.destroy()

        # 2. Tworzymy Canvas z suwakiem (żeby wszystkie tabele ze sprzętem mogły się przewijać)
        canvas = tk.Canvas(parent_frame, bg='lightgray')
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='lightgray')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 3. Tworzymy ujednolicone zmienne na tabele
        self.laptop_tree = ttk.Treeview(scrollable_frame, show='headings')
        self.monitor_tree = ttk.Treeview(scrollable_frame, show='headings')
        self.phone_tree = ttk.Treeview(scrollable_frame, show='headings')
        self.sluchawki_tree = ttk.Treeview(scrollable_frame, show='headings')
        self.karty_sim_tree = ttk.Treeview(scrollable_frame, show='headings')
        self.router_tree = ttk.Treeview(scrollable_frame, show='headings')
        self.myszki_tree = ttk.Treeview(scrollable_frame, show='headings')
        self.klawiatury_tree = ttk.Treeview(scrollable_frame, show='headings')

        # 4. Pobieranie danych z użyciem funkcji z main.py
        user_equipment, column_descriptions, _, _ = self.get_user_equipment(user_id)

        tree_mapping = {
            'LAPTOPY': ('Laptopy', self.laptop_tree),
            'MONITORY': ('Monitory', self.monitor_tree),
            'TELEFONY': ('Telefony', self.phone_tree),
            'SŁUCHAWKI': ('Słuchawki', self.sluchawki_tree),
            'KARTY SIM': ('Karty SIM', self.karty_sim_tree),
            'ROUTER': ('Routery', self.router_tree),
            'MYSZKI': ('Myszki', self.myszki_tree),
            'KLAWIATURY': ('Klawiatury', self.klawiatury_tree)
        }

        # 5. Budowanie tabel na ekranie i ładowanie danych
        for section_key, (display_title, tree) in tree_mapping.items():
            data = user_equipment.get(section_key, [])
            columns = column_descriptions.get(section_key, [])

            if not columns:
                columns = ['ID', 'Brak danych w tej sekcji']
                data = []

            # Ustawianie kolumn
            tree['columns'] = columns
            for col in columns:
                tree.heading(col, text=col)
                # Ukrywamy techniczne kolumny, których nie musi widzieć użytkownik (np. ID w bazie)
                if col in ['ID_UZYTKOWNIKA', 'UWAGI', 'NR SDJ', 'ID']:
                    tree.column(col, width=0, stretch=tk.NO)
                else:
                    tree.column(col, width=150, anchor='center')

            # Wstawianie wierszy ze sprzętem
            for row in data:
                tree.insert('', tk.END, values=row)

            # Pakujemy nagłówek sprzętu i samą tabelę na ekran
            tk.Label(scrollable_frame, text=display_title, font='Helvetica 10 bold', bg='lightgray').pack(anchor='w',
                                                                                                          padx=10,
                                                                                                          pady=(10, 0))

            # Wysokość tabeli dostosowuje się do ilości sprzętu
            row_count = len(data)
            tree.config(height=max(1, min(row_count, 5)))
            tree.pack(fill='x', padx=10, pady=2)

            # Nasłuchiwanie kliknięć, by zaznaczać rekord
            tree.bind('<Button-1>', self.sterowanie_jednym_kliknieciem_w_sekcji_uzytkownik)

    def przypisz_laptopa_w_sekcji_uzytkownik(self, user_id):
        if not user_id:
            messagebox.showwarning('Uwaga', 'Brak wybranego użytkownika.')
            return

        assign_win = tk.Toplevel(self)
        assign_win.title('Przypisz Laptopa')
        assign_win.geometry('800x400')
        assign_win.transient(self)

        tree = ttk.Treeview(assign_win, columns=('ID', 'STATUS', 'Srodek Trwaly', 'Nazwa', 'SN', 'Model'),
                            show='headings')
        tree.heading('ID', text='ID')
        tree.heading('STATUS', text='STATUS')
        tree.heading('Srodek Trwaly', text='Nr Środka Trwałego')
        tree.heading('Nazwa', text='Nazwa')
        tree.heading('SN', text='Nr Seryjny')
        tree.heading('Model', text='Model')
        tree.pack(fill='both', expand=True, padx=10, pady=10)

        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(SQL['select_msprzet_laptopy_wolne'])
            for row in cursor.fetchall():
                tree.insert('', tk.END, values=row)
        except Exception as e:
            messagebox.showerror('Błąd bazy', f'Błąd pobierania wolnych laptopów:\n{e}')
        finally:
            conn.close()

        def on_assign():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning('Uwaga', 'Wybierz sprzęt do przypisania.')
                return

            laptop_id = tree.item(selected[0])['values'][0]

            conn = create_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(SQL['update_przypisz_laptopa'], (user_id, laptop_id))
                conn.commit()
                messagebox.showinfo('Sukces', 'Pomyślnie przypisano laptopa.')
                self.display_user_assets(user_id)
                if hasattr(self, 'populate_frame_with_data'):
                    self.populate_frame_with_data('LAPTOPY')
                assign_win.destroy()
            except Exception as e:
                messagebox.showerror('Błąd', f'Błąd podczas przypisywania:\n{e}')
            finally:
                conn.close()

        tk.Button(assign_win, text='Przypisz wybrane', command=on_assign).pack(pady=10)
        self._center_window(assign_win)

    def przypisz_monitor_w_sekcji_uzytkownik(self, user_id):
        if not user_id:
            messagebox.showwarning('Uwaga', 'Brak wybranego użytkownika.')
            return

        assign_win = tk.Toplevel(self)
        assign_win.title('Przypisz Monitor')
        assign_win.geometry('800x400')
        assign_win.transient(self)

        tree = ttk.Treeview(assign_win, columns=('ID', 'STATUS', 'SN', 'Model'), show='headings')
        tree.heading('ID', text='ID')
        tree.heading('STATUS', text='STATUS')
        tree.heading('SN', text='Nr Seryjny')
        tree.heading('Model', text='Model')
        tree.pack(fill='both', expand=True, padx=10, pady=10)

        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(SQL['select_msprzet_monitory_wolne'])
            for row in cursor.fetchall():
                tree.insert('', tk.END, values=row)
        except Exception as e:
            pass
        finally:
            conn.close()

        def on_assign():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning('Uwaga', 'Wybierz sprzęt do przypisania.')
                return

            sprzet_id = tree.item(selected[0])['values'][0]

            conn = create_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(SQL['update_przypisz_monitor'], (user_id, sprzet_id))
                conn.commit()
                messagebox.showinfo('Sukces', 'Pomyślnie przypisano monitor.')
                self.display_user_assets(user_id)
                if hasattr(self, 'populate_frame_with_data'):
                    self.populate_frame_with_data('MONITORY')
                assign_win.destroy()
            except Exception as e:
                messagebox.showerror('Błąd', f'Błąd podczas przypisywania:\n{e}')
            finally:
                conn.close()

        tk.Button(assign_win, text='Przypisz wybrane', command=on_assign).pack(pady=10)
        self._center_window(assign_win)

    def przypisz_telefon_w_sekcji_uzytkownik(self, user_id):
        if not user_id:
            messagebox.showwarning('Uwaga', 'Brak wybranego użytkownika.')
            return

        assign_win = tk.Toplevel(self)
        assign_win.title('Przypisz Telefon')
        assign_win.geometry('800x400')
        assign_win.transient(self)

        tree = ttk.Treeview(assign_win, columns=('ID', 'STATUS', 'IMEI', 'Numer', 'Model'), show='headings')
        tree.heading('ID', text='ID')
        tree.heading('STATUS', text='STATUS')
        tree.heading('IMEI', text='IMEI')
        tree.heading('Numer', text='Numer telefonu')
        tree.heading('Model', text='Model')
        tree.pack(fill='both', expand=True, padx=10, pady=10)

        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(SQL['select_msprzet_telefony_wolne'])
            for row in cursor.fetchall():
                tree.insert('', tk.END, values=row)
        except Exception:
            pass
        finally:
            conn.close()

        def on_assign():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning('Uwaga', 'Wybierz sprzęt do przypisania.')
                return

            sprzet_id = tree.item(selected[0])['values'][0]

            conn = create_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(SQL['update_przypisz_telefon'], (user_id, sprzet_id))
                conn.commit()
                messagebox.showinfo('Sukces', 'Pomyślnie przypisano telefon.')
                self.display_user_assets(user_id)
                if hasattr(self, 'populate_frame_with_data'):
                    self.populate_frame_with_data('TELEFONY')
                assign_win.destroy()
            except Exception as e:
                messagebox.showerror('Błąd', f'Błąd podczas przypisywania:\n{e}')
            finally:
                conn.close()

        tk.Button(assign_win, text='Przypisz wybrane', command=on_assign).pack(pady=10)
        self._center_window(assign_win)

    def przypisz_sluchawki_w_sekcji_uzytkownik(self, user_id):
        if not user_id: return
        assign_win = tk.Toplevel(self)
        assign_win.title('Przypisz Słuchawki')
        assign_win.geometry('800x400')
        assign_win.transient(self)
        tree = ttk.Treeview(assign_win, columns=('ID', 'STATUS', 'SN', 'Model'), show='headings')
        for col, txt in zip(tree['columns'], ('ID', 'STATUS', 'Nr Seryjny', 'Model')):
            tree.heading(col, text=txt)
        tree.pack(fill='both', expand=True, padx=10, pady=10)

        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(SQL['select_msprzet_sluchawki_wolne'])
            for row in cursor.fetchall(): tree.insert('', tk.END, values=row)
        except Exception:
            pass
        finally:
            conn.close()

        def on_assign():
            selected = tree.selection()
            if not selected: return
            sprzet_id = tree.item(selected[0])['values'][0]
            conn = create_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(SQL['update_przypisz_sluchawki'], (user_id, sprzet_id))
                conn.commit()
                self.display_user_assets(user_id)
                if hasattr(self, 'populate_frame_with_data'): self.populate_frame_with_data('SŁUCHAWKI')
                assign_win.destroy()
            except Exception:
                pass
            finally:
                conn.close()

        tk.Button(assign_win, text='Przypisz wybrane', command=on_assign).pack(pady=10)
        self._center_window(assign_win)

    def przypisz_karte_sim_w_sekcji_uzytkownik(self, user_id):
        if not user_id: return
        assign_win = tk.Toplevel(self)
        assign_win.title('Przypisz Kartę SIM')
        assign_win.geometry('800x400')
        assign_win.transient(self)
        tree = ttk.Treeview(assign_win, columns=('ID', 'STATUS', 'Numer', 'SIM', 'Operator'), show='headings')
        for col, txt in zip(tree['columns'], ('ID', 'STATUS', 'Numer telefonu', 'Nr SIM', 'Operator')):
            tree.heading(col, text=txt)
        tree.pack(fill='both', expand=True, padx=10, pady=10)

        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(SQL['select_msprzet_karty_sim_wolne'])
            for row in cursor.fetchall(): tree.insert('', tk.END, values=row)
        except Exception:
            pass
        finally:
            conn.close()

        def on_assign():
            selected = tree.selection()
            if not selected: return
            sprzet_id = tree.item(selected[0])['values'][0]
            conn = create_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(SQL['update_przypisz_karte_sim'], (user_id, sprzet_id))
                conn.commit()
                self.display_user_assets(user_id)
                if hasattr(self, 'populate_frame_with_data'): self.populate_frame_with_data('KARTY SIM')
                assign_win.destroy()
            except Exception:
                pass
            finally:
                conn.close()

        tk.Button(assign_win, text='Przypisz wybrane', command=on_assign).pack(pady=10)
        self._center_window(assign_win)

    def przypisz_router_w_sekcji_uzytkownik(self, user_id):
        if not user_id: return
        assign_win = tk.Toplevel(self)
        assign_win.title('Przypisz Router')
        assign_win.geometry('800x400')
        assign_win.transient(self)
        tree = ttk.Treeview(assign_win, columns=('ID', 'STATUS', 'IMEI', 'Numer', 'SIM', 'Operator'), show='headings')
        for col, txt in zip(tree['columns'], ('ID', 'STATUS', 'IMEI', 'Numer telefonu', 'Nr SIM', 'Operator')):
            tree.heading(col, text=txt)
        tree.pack(fill='both', expand=True, padx=10, pady=10)

        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(SQL['select_msprzet_router_wolne'])
            for row in cursor.fetchall(): tree.insert('', tk.END, values=row)
        except Exception:
            pass
        finally:
            conn.close()

        def on_assign():
            selected = tree.selection()
            if not selected: return
            sprzet_id = tree.item(selected[0])['values'][0]
            conn = create_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(SQL['update_przypisz_router'], (user_id, sprzet_id))
                conn.commit()
                self.display_user_assets(user_id)
                if hasattr(self, 'populate_frame_with_data'): self.populate_frame_with_data('ROUTER')
                assign_win.destroy()
            except Exception:
                pass
            finally:
                conn.close()

        tk.Button(assign_win, text='Przypisz wybrane', command=on_assign).pack(pady=10)
        self._center_window(assign_win)

    def przypisz_myszke_w_sekcji_uzytkownik(self, user_id):
        if not user_id: return
        assign_win = tk.Toplevel(self)
        assign_win.title('Przypisz Myszkę')
        assign_win.geometry('600x400')
        assign_win.transient(self)
        tree = ttk.Treeview(assign_win, columns=('ID', 'STATUS', 'Uwagi'), show='headings')
        for col, txt in zip(tree['columns'], ('ID', 'STATUS', 'Uwagi')):
            tree.heading(col, text=txt)
        tree.pack(fill='both', expand=True, padx=10, pady=10)

        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(SQL['select_msprzet_myszki_wolne'])
            for row in cursor.fetchall(): tree.insert('', tk.END, values=row)
        except Exception:
            pass
        finally:
            conn.close()

        def on_assign():
            selected = tree.selection()
            if not selected: return
            sprzet_id = tree.item(selected[0])['values'][0]
            conn = create_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(SQL['update_przypisz_myszke'], (user_id, sprzet_id))
                conn.commit()
                self.display_user_assets(user_id)
                if hasattr(self, 'populate_frame_with_data'): self.populate_frame_with_data('MYSZKI')
                assign_win.destroy()
            except Exception:
                pass
            finally:
                conn.close()

        tk.Button(assign_win, text='Przypisz wybrane', command=on_assign).pack(pady=10)
        self._center_window(assign_win)

    def przypisz_klawiature_w_sekcji_uzytkownik(self, user_id):
        if not user_id: return
        assign_win = tk.Toplevel(self)
        assign_win.title('Przypisz Klawiaturę')
        assign_win.geometry('600x400')
        assign_win.transient(self)
        tree = ttk.Treeview(assign_win, columns=('ID', 'STATUS', 'Uwagi'), show='headings')
        for col, txt in zip(tree['columns'], ('ID', 'STATUS', 'Uwagi')):
            tree.heading(col, text=txt)
        tree.pack(fill='both', expand=True, padx=10, pady=10)

        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(SQL['select_msprzet_klawiatury_wolne'])
            for row in cursor.fetchall(): tree.insert('', tk.END, values=row)
        except Exception:
            pass
        finally:
            conn.close()

        def on_assign():
            selected = tree.selection()
            if not selected: return
            sprzet_id = tree.item(selected[0])['values'][0]
            conn = create_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(SQL['update_przypisz_klawiature'], (user_id, sprzet_id))
                conn.commit()
                self.display_user_assets(user_id)
                if hasattr(self, 'populate_frame_with_data'): self.populate_frame_with_data('KLAWIATURY')
                assign_win.destroy()
            except Exception:
                pass
            finally:
                conn.close()

        tk.Button(assign_win, text='Przypisz wybrane', command=on_assign).pack(pady=10)
        self._center_window(assign_win)