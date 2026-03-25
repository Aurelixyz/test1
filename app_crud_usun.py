import tkinter as tk
from tkinter import messagebox
from config_db import create_connection, SQL


class UsunMixin:
    def action5(self, section):
        if section in ['LAPTOPY', 'MONITORY', 'TELEFONY', 'KONTA UŻYTKOWNIKÓW', 'KARTY SIM', 'ROUTER', 'MYSZKI',
                       'KLAWIATURY']:
            self.delete_record(section)

    def delete_record(self, section):
        if section == 'LAPTOPY':
            selected_items = self.tabela.selection()
            if not selected_items:
                messagebox.showinfo('Błąd', 'Nie wybrano żadnego rekordu do usunięcia.')
                return
            confirm = messagebox.askyesno('Potwierdzenie', 'Czy na pewno chcesz usunąć wybrane rekordy?')
            if not confirm:
                return
            conn = create_connection()
            cursor = conn.cursor()
            for item in selected_items:
                record_id = self.tabela.item(item)['values'][-1]
                delete_query = SQL['delete_from_msprzet_laptopy_b634aee7']
                cursor.execute(delete_query, (record_id,))
                conn.commit()
                self.tabela.delete(item)
            conn.close()
            messagebox.showinfo('Sukces', 'Rekordy zostały usunięte.')
            self.populate_frame_with_data(section)

        elif section == 'MONITORY':
            selected_items = self.tabela_monitory.selection()
            if not selected_items:
                messagebox.showinfo('Błąd', 'Nie wybrano żadnego rekordu do usunięcia.')
                return
            confirm = messagebox.askyesno('Potwierdzenie', 'Czy na pewno chcesz usunąć wybrane rekordy?')
            if not confirm:
                return
            conn = create_connection()
            cursor = conn.cursor()
            for item in selected_items:
                record_id = self.tabela_monitory.item(item)['values'][-1]
                delete_query = SQL['delete_from_msprzet_monitory_ad184ac2']
                cursor.execute(delete_query, (record_id,))
                conn.commit()
                self.tabela_monitory.delete(item)
            conn.close()
            messagebox.showinfo('Sukces', 'Rekordy zostały usunięte.')
            self.populate_frame_with_data(section)

        elif section == 'KONTA UŻYTKOWNIKÓW':
            selected_items = self.tabela_konta.selection()
            if not selected_items:
                messagebox.showinfo('Błąd', 'Nie wybrano żadnego rekordu do usunięcia.')
                return
            confirm = messagebox.askyesno('Potwierdzenie', 'Czy na pewno chcesz usunąć wybrane rekordy?')
            if not confirm:
                return
            conn = create_connection()
            cursor = conn.cursor()
            for item in selected_items:
                record_id = self.tabela_konta.item(item)['values'][-1]
                delete_query = SQL['delete_from_msprzet_konta_uzytkownikow_72e7ae23']
                cursor.execute(delete_query, (record_id,))
                conn.commit()
                self.tabela_konta.delete(item)
            conn.close()
            messagebox.showinfo('Sukces', 'Rekordy zostały usunięte.')
            self.populate_frame_with_data(section)

    def usun_konto_uzytkownika(self):
        selected_items = self.tabela_konta.selection()
        if not selected_items:
            messagebox.showinfo('Błąd', 'Nie wybrano żadnego rekordu do usunięcia.')
            return
        if len(selected_items) > 1:
            messagebox.showinfo('Błąd', 'Można usunąć tylko jeden rekord na raz.')
            return
        record_id = self.tabela_konta.item(selected_items[0])['values'][-1]
        login_windows = self.tabela_konta.item(selected_items[0])['values'][0]

        conn = create_connection()
        cursor = conn.cursor()
        query_laptops = SQL['select_msprzet_laptopy_ce93a11f']
        query_monitors = SQL['select_msprzet_monitory_69723938']
        query_telefon = SQL['select_msprzet_telefony_62ef32ff']
        query_sluchawki = SQL['select_msprzet_sluchawki_4f429425']
        query_karty_sim = SQL['select_msprzet_karty_sim_48f030cc']
        query_router = SQL['select_msprzet_router_eeda9249']
        query_myszki = SQL['select_msprzet_myszki_a7b46c56']
        query_klawiatury = SQL['select_msprzet_klawiatury_28c225c2']

        cursor.execute(query_laptops, (record_id,))
        laptop_count = cursor.fetchone()[0]
        cursor.execute(query_monitors, (record_id,))
        monitor_count = cursor.fetchone()[0]
        cursor.execute(query_telefon, (record_id,))
        telefon_count = cursor.fetchone()[0]
        cursor.execute(query_sluchawki, (record_id,))
        sluchawki_count = cursor.fetchone()[0]
        cursor.execute(query_karty_sim, (record_id,))
        karty_sim_count = cursor.fetchone()[0]
        cursor.execute(query_router, (record_id,))
        router_count = cursor.fetchone()[0]
        cursor.execute(query_myszki, (record_id,))
        myszki_count = cursor.fetchone()[0]
        cursor.execute(query_klawiatury, (record_id,))
        klawiatury_count = cursor.fetchone()[0]

        if laptop_count > 0 or monitor_count > 0 or telefon_count > 0 or sluchawki_count > 0 or karty_sim_count > 0 or router_count > 0 or myszki_count > 0 or klawiatury_count > 0:
            messagebox.showinfo('Błąd',
                                f'Nie można usunąć UŻYTKOWNIKa ID {record_id} i loginie {login_windows}, ponieważ ma przypisany sprzęt.')
            conn.close()
            return

        confirm = messagebox.askyesno('Potwierdzenie', f'Czy na pewno chcesz usunąć UŻYTKOWNIKa ID {record_id}?')
        if not confirm:
            conn.close()
            return

        delete_query = SQL['delete_from_msprzet_konta_uzytkownikow_72e7ae23']
        cursor.execute(delete_query, (record_id,))
        conn.commit()
        self.tabela_konta.delete(selected_items[0])
        conn.close()
        messagebox.showinfo('Sukces', f'UŻYTKOWNIK ID {record_id} został usunięty.')

    def usun_telefon(self):
        selected_items = self.tabela_telefony.selection()
        if not selected_items:
            messagebox.showinfo('Błąd', 'Nie wybrano żadnego rekordu do usunięcia.')
            return
        confirm = messagebox.askyesno('Potwierdzenie', 'Czy na pewno chcesz usunąć wybrane rekordy?')
        if not confirm:
            return
        conn = create_connection()
        cursor = conn.cursor()
        for item in selected_items:
            record_id = self.tabela_telefony.item(item)['values'][-1]
            delete_query = SQL['delete_from_msprzet_telefony_9369fe4d']
            cursor.execute(delete_query, (record_id,))
            conn.commit()
            self.tabela_telefony.delete(item)
        conn.close()
        messagebox.showinfo('Sukces', 'Rekordy zostały usunięte.')

    def usun_sluchawki(self, section):
        selected_items = self.tabela_sluchawki.selection()
        if not selected_items:
            messagebox.showinfo('Błąd', 'Nie wybrano żadnego rekordu do usunięcia.')
            return
        confirm = messagebox.askyesno('Potwierdzenie', 'Czy na pewno chcesz usunąć wybrane rekordy?')
        if not confirm:
            return
        conn = create_connection()
        cursor = conn.cursor()
        for item in selected_items:
            record_id = self.tabela_sluchawki.item(item)['values'][-1]
            delete_query = SQL['delete_from_msprzet_sluchawki_26a8791d']
            cursor.execute(delete_query, (record_id,))
            conn.commit()
            self.tabela_sluchawki.delete(item)
        conn.close()
        messagebox.showinfo('Sukces', 'Rekordy zostały usunięte.')
        self.populate_frame_with_data(section)

    def usun_karte_sim(self, section):
        selected_items = self.tabela_karty_sim.selection()
        if not selected_items:
            messagebox.showinfo('Błąd', 'Nie wybrano żadnego rekordu do usunięcia.')
            return
        confirm = messagebox.askyesno('Potwierdzenie', 'Czy na pewno chcesz usunąć wybrane rekordy?')
        if not confirm:
            return
        conn = create_connection()
        cursor = conn.cursor()
        for item in selected_items:
            record_id = self.tabela_karty_sim.item(item)['values'][-1]
            delete_query = SQL['delete_from_msprzet_karty_sim_39d10768']
            cursor.execute(delete_query, (record_id,))
            conn.commit()
            self.tabela_karty_sim.delete(item)
        conn.close()
        messagebox.showinfo('Sukces', 'Rekordy zostały usunięte.')
        self.populate_frame_with_data(section)

    def usun_router(self, section):
        selected_items = self.tabela_router.selection()
        if not selected_items:
            messagebox.showinfo('Błąd', 'Nie wybrano żadnego rekordu do usunięcia.')
            return
        confirm = messagebox.askyesno('Potwierdzenie', 'Czy na pewno chcesz usunąć wybrane rekordy?')
        if not confirm:
            return
        conn = create_connection()
        cursor = conn.cursor()
        for item in selected_items:
            record_id = self.tabela_router.item(item)['values'][-1]
            delete_query = SQL['delete_from_msprzet_router_51623e63']
            cursor.execute(delete_query, (record_id,))
            conn.commit()
            self.tabela_router.delete(item)
        conn.close()
        messagebox.showinfo('Sukces', 'Rekordy zostały usunięte.')
        self.populate_frame_with_data(section)

    def usun_myszke(self, section):
        selected_items = self.tabela_myszki.selection()
        if not selected_items:
            messagebox.showinfo('Błąd', 'Nie wybrano żadnego rekordu do usunięcia.')
            return
        confirm = messagebox.askyesno('Potwierdzenie', 'Czy na pewno chcesz usunąć wybrane rekordy?')
        if not confirm:
            return
        conn = create_connection()
        cursor = conn.cursor()
        for item in selected_items:
            record_id = self.tabela_myszki.item(item)['values'][-1]
            delete_query = SQL['delete_from_msprzet_myszki_68aa9e1c']
            cursor.execute(delete_query, (record_id,))
            conn.commit()
            self.tabela_myszki.delete(item)
        conn.close()
        messagebox.showinfo('Sukces', 'Rekordy zostały usunięte.')
        self.populate_frame_with_data(section)

    def usun_klawiature(self, section):
        selected_items = self.tabela_klawiatury.selection()
        if not selected_items:
            messagebox.showinfo('Błąd', 'Nie wybrano żadnego rekordu do usunięcia.')
            return
        confirm = messagebox.askyesno('Potwierdzenie', 'Czy na pewno chcesz usunąć wybrane rekordy?')
        if not confirm:
            return
        conn = create_connection()
        cursor = conn.cursor()
        for item in selected_items:
            record_id = self.tabela_klawiatury.item(item)['values'][-1]
            delete_query = SQL['delete_from_msprzet_klawiatury_f6a09628']
            cursor.execute(delete_query, (record_id,))
            conn.commit()
            self.tabela_klawiatury.delete(item)
        conn.close()
        messagebox.showinfo('Sukces', 'Rekordy zostały usunięte.')
        self.populate_frame_with_data(section)

    def odpisz_uzytkownika(self, id_entry):
        confirm = messagebox.askyesno('Potwierdzenie', 'Czy na pewno chcesz odpisz UŻYTKOWNIKa?')
        if not confirm:
            return
        user = ''
        if self.ID_UZYTKOWNIKA_entry:
            self.ID_UZYTKOWNIKA_entry.config(state='normal')
            self.ID_UZYTKOWNIKA_entry.delete(0, tk.END)
            self.ID_UZYTKOWNIKA_entry.insert(0, user)
            self.ID_UZYTKOWNIKA_entry.config(state='readonly')
        if self.IMIE_entry:
            self.IMIE_entry.config(state='normal')
            self.IMIE_entry.delete(0, tk.END)
            self.IMIE_entry.insert(0, user)
            self.IMIE_entry.config(state='readonly')
        if self.NAZWISKO_entry:
            self.NAZWISKO_entry.config(state='normal')
            self.NAZWISKO_entry.delete(0, tk.END)
            self.NAZWISKO_entry.insert(0, user)
            self.NAZWISKO_entry.config(state='readonly')

    def odpisz_uzytkownika_w_sekcji_UŻYTKOWNIK(self, id_entry):
        confirm = messagebox.askyesno('Potwierdzenie', 'Czy na pewno chcesz odpisz UŻYTKOWNIKa?')
        if not confirm:
            return
        user = ''
        if self.ID_UZYTKOWNIKA_entry:
            self.ID_UZYTKOWNIKA_entry.config(state='normal')
            self.ID_UZYTKOWNIKA_entry.delete(0, tk.END)
            self.ID_UZYTKOWNIKA_entry.insert(0, user)
            self.ID_UZYTKOWNIKA_entry.config(state='readonly')