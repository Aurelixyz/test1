import tkinter as tk
from tkinter import ttk, messagebox
from config_db import create_connection, SQL


class PrzypisywanieMixin:

    def display_user_assets(self, user_id):
        conn = create_connection()
        cursor = conn.cursor()

        # Czyszczenie starych danych
        if hasattr(self, 'tabela_user_laptopy'):
            self.tabela_user_laptopy.delete(*self.tabela_user_laptopy.get_children())
        if hasattr(self, 'tabela_user_monitory'):
            self.tabela_user_monitory.delete(*self.tabela_user_monitory.get_children())
        if hasattr(self, 'tabela_user_telefony'):
            self.tabela_user_telefony.delete(*self.tabela_user_telefony.get_children())
        if hasattr(self, 'tabela_user_sluchawki'):
            self.tabela_user_sluchawki.delete(*self.tabela_user_sluchawki.get_children())
        if hasattr(self, 'tabela_user_karty_sim'):
            self.tabela_user_karty_sim.delete(*self.tabela_user_karty_sim.get_children())
        if hasattr(self, 'tabela_user_router'):
            self.tabela_user_router.delete(*self.tabela_user_router.get_children())
        if hasattr(self, 'tabela_user_myszki'):
            self.tabela_user_myszki.delete(*self.tabela_user_myszki.get_children())
        if hasattr(self, 'tabela_user_klawiatury'):
            self.tabela_user_klawiatury.delete(*self.tabela_user_klawiatury.get_children())

        # Laptopy
        try:
            cursor.execute(SQL['select_msprzet_laptopy_ce93a11f'], (user_id,))
            for row in cursor.fetchall():
                self.tabela_user_laptopy.insert('', tk.END,
                                                values=[str(v).strip() if v is not None else '' for v in row])
        except Exception:
            pass

        # Monitory
        try:
            cursor.execute(SQL['select_msprzet_monitory_69723938'], (user_id,))
            for row in cursor.fetchall():
                self.tabela_user_monitory.insert('', tk.END,
                                                 values=[str(v).strip() if v is not None else '' for v in row])
        except Exception:
            pass

        # Telefony
        try:
            cursor.execute(SQL['select_msprzet_telefony_62ef32ff'], (user_id,))
            for row in cursor.fetchall():
                self.tabela_user_telefony.insert('', tk.END,
                                                 values=[str(v).strip() if v is not None else '' for v in row])
        except Exception:
            pass

        # Słuchawki
        try:
            cursor.execute(SQL['select_msprzet_sluchawki_4f429425'], (user_id,))
            for row in cursor.fetchall():
                self.tabela_user_sluchawki.insert('', tk.END,
                                                  values=[str(v).strip() if v is not None else '' for v in row])
        except Exception:
            pass

        # Karty SIM
        try:
            cursor.execute(SQL['select_msprzet_karty_sim_48f030cc'], (user_id,))
            for row in cursor.fetchall():
                self.tabela_user_karty_sim.insert('', tk.END,
                                                  values=[str(v).strip() if v is not None else '' for v in row])
        except Exception:
            pass

        # Routery
        try:
            cursor.execute(SQL['select_msprzet_router_eeda9249'], (user_id,))
            for row in cursor.fetchall():
                self.tabela_user_router.insert('', tk.END,
                                               values=[str(v).strip() if v is not None else '' for v in row])
        except Exception:
            pass

        # Myszki
        try:
            cursor.execute(SQL['select_msprzet_myszki_a7b46c56'], (user_id,))
            for row in cursor.fetchall():
                self.tabela_user_myszki.insert('', tk.END,
                                               values=[str(v).strip() if v is not None else '' for v in row])
        except Exception:
            pass

        # Klawiatury
        try:
            cursor.execute(SQL['select_msprzet_klawiatury_28c225c2'], (user_id,))
            for row in cursor.fetchall():
                self.tabela_user_klawiatury.insert('', tk.END,
                                                   values=[str(v).strip() if v is not None else '' for v in row])
        except Exception:
            pass

        conn.close()

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