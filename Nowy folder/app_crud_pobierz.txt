import tkinter as tk
from config_db import create_connection, SQL

class PobierzMixin:
    def action6(self, section):
        if section == 'LAPTOPY':
            self.populate_frame_with_data('LAPTOPY')
        elif section == 'MONITORY':
            self.populate_frame_with_data('MONITORY')
        elif section == 'TELEFONY':
            self.populate_frame_with_data('TELEFONY')
        elif section == 'SŁUCHAWKI':
            self.populate_frame_with_data('SŁUCHAWKI')
        elif section == 'KARTY SIM':
            self.populate_frame_with_data('KARTY SIM')
        elif section == 'ROUTER':
            self.populate_frame_with_data('ROUTER')
        elif section == 'MYSZKI':
            self.populate_frame_with_data('MYSZKI')
        elif section == 'KLAWIATURY':
            self.populate_frame_with_data('KLAWIATURY')

    def pobierz_dane_laptopy(self):
        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_laptopy_c30aa83e']
        cursor.execute(query)
        self.tabela.delete(*self.tabela.get_children())
        self.original_data = []
        for row in cursor:
            clean_row = [str(value).strip() for value in row]
            self.tabela.insert('', tk.END, values=clean_row)
            self.original_data.append(('', clean_row))
        self.update_column_widths(self.tabela, 'LAPTOPY')
        conn.close()

    def pobierz_dane_monitory(self):
        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_monitory_19affa3b']
        cursor.execute(query)
        self.tabela_monitory.delete(*self.tabela_monitory.get_children())
        self.original_data_monitory = []
        for row in cursor:
            clean_row = [str(value).strip() for value in row]
            self.tabela_monitory.insert('', tk.END, values=clean_row)
            self.original_data_monitory.append(('', clean_row))
        self.update_column_widths(self.tabela_monitory, 'MONITORY')
        conn.close()

    def pobierz_dane_telefony(self):
        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_telefony_562cc7bc']
        cursor.execute(query)
        self.tabela_telefony.delete(*self.tabela_telefony.get_children())
        self.original_data_telefony = []
        for row in cursor:
            clean_row = [str(value).strip() for value in row]
            self.tabela_telefony.insert('', tk.END, values=clean_row)
            self.original_data_telefony.append(('', clean_row))
        self.update_column_widths(self.tabela_telefony, 'TELEFONY')
        conn.close()

    def pobierz_dane_sluchawki(self):
        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_sluchawki_4be50469']
        cursor.execute(query)
        self.tabela_sluchawki.delete(*self.tabela_sluchawki.get_children())
        self.original_data_sluchawki = []
        for row in cursor:
            clean_row = [str(value).strip() for value in row]
            self.tabela_sluchawki.insert('', tk.END, values=clean_row)
            self.original_data_sluchawki.append(('', clean_row))
        self.update_column_widths(self.tabela_sluchawki, 'SŁUCHAWKI')
        conn.close()

    def pobierz_dane_karty_sim(self):
        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_karty_sim_b548b93d']
        cursor.execute(query)
        self.tabela_karty_sim.delete(*self.tabela_karty_sim.get_children())
        self.original_data_karty_sim = []
        for row in cursor:
            clean_row = [str(value).strip() for value in row]
            self.tabela_karty_sim.insert('', tk.END, values=clean_row)
            self.original_data_karty_sim.append(('', clean_row))
        self.update_column_widths(self.tabela_karty_sim, 'KARTY SIM')
        conn.close()

    def pobierz_dane_router(self):
        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_router_31a18543']
        cursor.execute(query)
        self.tabela_router.delete(*self.tabela_router.get_children())
        self.original_data_router = []
        for row in cursor:
            clean_row = [str(value).strip() for value in row]
            self.tabela_router.insert('', tk.END, values=clean_row)
            self.original_data_router.append(('', clean_row))
        self.update_column_widths(self.tabela_router, 'ROUTER')
        conn.close()

    def pobierz_dane_myszki(self):
        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_myszki_f484d92d']
        cursor.execute(query)
        self.tabela_myszki.delete(*self.tabela_myszki.get_children())
        self.original_data_myszki = []
        for row in cursor:
            clean_row = [str(value).strip() for value in row]
            self.tabela_myszki.insert('', tk.END, values=clean_row)
            self.original_data_myszki.append(('', clean_row))
        self.update_column_widths(self.tabela_myszki, 'MYSZKI')
        conn.close()

    def pobierz_dane_klawiatury(self):
        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_klawiatury_83212e19']
        cursor.execute(query)
        self.tabela_klawiatury.delete(*self.tabela_klawiatury.get_children())
        self.original_data_klawiatury = []
        for row in cursor:
            clean_row = [str(value).strip() for value in row]
            self.tabela_klawiatury.insert('', tk.END, values=clean_row)
            self.original_data_klawiatury.append(('', clean_row))
        self.update_column_widths(self.tabela_klawiatury, 'KLAWIATURY')
        conn.close()

    def pobierz_dane_konta_uzytkownikow(self):
        conn = create_connection()
        cursor = conn.cursor()
        query = SQL['select_msprzet_konta_uzytkownikow_9e64c0f3']
        cursor.execute(query)
        self.tabela_konta.delete(*self.tabela_konta.get_children())
        rows = cursor.fetchall()
        for row in rows:
            values = [value if value is not None else '' for value in row]
            self.tabela_konta.insert('', tk.END, values=values)
        conn.close()
        self.original_data_konta = [(self.tabela_konta.item(item)['text'], self.tabela_konta.item(item)['values']) for item in self.tabela_konta.get_children()]