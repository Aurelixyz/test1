import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import Calendar
from models_specs import get_employment_day_1, get_employment_day_15


class DialogsMixin:
    def pick_date_dialog(self, parent=None, initial_dt=None, title='Wybierz datę'):
        today = datetime.date.today()
        if isinstance(initial_dt, str):
            try:
                initial_dt = datetime.datetime.strptime(initial_dt.strip(), '%Y-%m-%d').date()
            except Exception:
                initial_dt = None
        if initial_dt is None:
            initial_dt = today

        def days_in_month(year, month):
            if month == 12:
                nxt = datetime.date(year + 1, 1, 1)
            else:
                nxt = datetime.date(year, month + 1, 1)
            first = datetime.date(year, month, 1)
            return (nxt - first).days

        dlg = tk.Toplevel(parent if parent is not None else self)
        dlg.title(title)
        dlg.transient(self)
        dlg.resizable(False, False)
        dlg.grab_set()
        main = ttk.Frame(dlg, padding=12)
        main.grid(row=0, column=0)
        ttk.Label(main, text='Dzień').grid(row=0, column=0, padx=(0, 8))
        ttk.Label(main, text='Miesiąc').grid(row=0, column=1, padx=(0, 8))
        ttk.Label(main, text='Rok').grid(row=0, column=2)
        var_day = tk.IntVar(value=initial_dt.day)
        var_month = tk.IntVar(value=initial_dt.month)
        var_year = tk.IntVar(value=initial_dt.year)

        def clamp_day():
            y, m = (var_year.get(), var_month.get())
            dim = days_in_month(y, m)
            if var_day.get() > dim:
                var_day.set(dim)
            elif var_day.get() < 1:
                var_day.set(1)

        def on_month_year_changed(*_):
            clamp_day()

        var_month.trace_add('write', on_month_year_changed)
        var_year.trace_add('write', on_month_year_changed)
        spn_day = ttk.Spinbox(main, from_=1, to=31, width=4, textvariable=var_day, wrap=True, justify='center')
        spn_month = ttk.Spinbox(main, from_=1, to=12, width=4, textvariable=var_month, wrap=True, justify='center')
        spn_year = ttk.Spinbox(main, from_=1900, to=2100, width=6, textvariable=var_year, wrap=True, justify='center')
        spn_day.grid(row=1, column=0, padx=(0, 8), pady=(4, 10))
        spn_month.grid(row=1, column=1, padx=(0, 8), pady=(4, 10))
        spn_year.grid(row=1, column=2, pady=(4, 10))
        btns = ttk.Frame(main)
        btns.grid(row=2, column=0, columnspan=3, sticky='e')
        result = {'date': None}

        def _on_ok():
            try:
                d = datetime.date(var_year.get(), var_month.get(), var_day.get())
                result['date'] = d
                dlg.destroy()
            except Exception:
                messagebox.showerror('Błąd daty', 'Nieprawidłowa data.')

        def _set_day(day):
            var_day.set(day)
            clamp_day()

        ttk.Button(btns, text='Zatrudnienie 1', command=lambda: _set_day(1)).grid(row=0, column=0, padx=(0, 6))
        ttk.Button(btns, text='Zatrudnienie 15', command=lambda: _set_day(15)).grid(row=0, column=1, padx=(0, 6))
        ttk.Button(btns, text='OK', command=_on_ok).grid(row=0, column=2)
        dlg.bind('<Return>', lambda e: _on_ok())
        dlg.bind('<Escape>', lambda e: dlg.destroy())
        dlg.update_idletasks()
        pr = parent if parent is not None else self
        px = pr.winfo_rootx() + (pr.winfo_width() - dlg.winfo_width()) // 2
        py = pr.winfo_rooty() + (pr.winfo_height() - dlg.winfo_height()) // 2
        dlg.geometry(f'+{max(px, 0)}+{max(py, 0)}')
        spn_day.focus_set()
        dlg.wait_window()
        return result['date']

    def date_input_dialog(self, parent=None, initial_date=None, title='Data złożenia oświadczenia'):
        today = datetime.date.today()
        if initial_date is None:
            initial_date = today
        elif isinstance(initial_date, str):
            try:
                initial_date = datetime.datetime.strptime(initial_date.strip(), '%Y-%m-%d').date()
            except Exception:
                initial_date = today

        dlg = tk.Toplevel(parent if parent is not None else self)
        dlg.title(title)
        dlg.transient(self)
        dlg.resizable(False, False)
        dlg.grab_set()
        frm = ttk.Frame(dlg, padding=12)
        frm.grid(row=0, column=0)
        ttk.Label(frm, text='Podaj datę (RRRR-MM-DD):').grid(row=0, column=0, sticky='w')
        var_date = tk.StringVar()
        ent = ttk.Entry(frm, textvariable=var_date, width=14, justify='center')
        ent.grid(row=1, column=0, sticky='w', pady=(4, 8))

        def format_date_input(event):
            raw = ent.get().replace('-', '')
            new_val = ''
            if len(raw) >= 1:
                new_val += raw[:4]
            if len(raw) >= 5:
                new_val += '-' + raw[4:6]
            if len(raw) >= 7:
                new_val += '-' + raw[6:8]
            ent.delete(0, tk.END)
            ent.insert(0, new_val)
            ent.icursor(len(new_val))

        ent.bind('<KeyRelease>', format_date_input)
        btns_inline = ttk.Frame(frm)
        btns_inline.grid(row=1, column=1, padx=(8, 0), sticky='w')
        calendar_open = {'active': False}

        def _choose():
            if calendar_open['active']:
                return
            calendar_open['active'] = True
            cal_win = tk.Toplevel(dlg)
            cal_win.title('Kalendarz')
            cal_win.transient(dlg)
            cal_win.grab_set()
            cal_win.resizable(False, False)
            cal_win.withdraw()
            NUMS13 = [''] + [str(i) for i in range(1, 13)]
            POL13 = ['', 'Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień',
                     'Październik', 'Listopad', 'Grudzień']
            cal = Calendar(cal_win, selectmode='day', locale='pl', date_pattern='yyyy-mm-dd', month_names=POL13)
            cal.pack(padx=10, pady=10)
            try:
                if hasattr(cal, '_month_names'):
                    cal._month_names = POL13
                if hasattr(cal, '_month_names_gen'):
                    cal._month_names_gen = POL13
                if hasattr(cal, '_month_names_short'):
                    cal._month_names_short = POL13
                if hasattr(cal, '_month_names_abbr'):
                    cal._month_names_abbr = POL13
            except Exception:
                pass
            try:
                cal._display_calendar()
            except Exception:
                try:
                    cal.next_month()
                    cal.prev_month()
                except Exception:
                    pass

            def _select_date():
                var_date.set(cal.get_date())
                calendar_open['active'] = False
                cal_win.destroy()

            def _on_close():
                calendar_open['active'] = False
                cal_win.destroy()

            ttk.Button(cal_win, text='Wybierz', command=_select_date).pack(pady=(0, 10))
            cal_win.protocol('WM_DELETE_WINDOW', _on_close)
            cal_win.update_idletasks()
            screen_w = cal_win.winfo_screenwidth()
            screen_h = cal_win.winfo_screenheight()
            win_w = cal_win.winfo_width()
            win_h = cal_win.winfo_height()
            x = screen_w // 2 - win_w // 2
            y = screen_h // 2 - win_h // 2
            cal_win.geometry(f'+{x}+{y}')
            cal_win.deiconify()
            cal.focus_set()

        def _set_day(day):
            if day == 1:
                d = get_employment_day_1()
            else:
                d = get_employment_day_15()
            if d:
                var_date.set(d.strftime('%Y-%m-%d'))

        ttk.Button(btns_inline, text='Kalendarz', command=_choose).grid(row=0, column=0, padx=(0, 6))
        ttk.Button(btns_inline, text='Zatrudnienie 1', command=lambda: _set_day(1)).grid(row=0, column=1, padx=(0, 6))
        ttk.Button(btns_inline, text='Zatrudnienie 15', command=lambda: _set_day(15)).grid(row=0, column=2)
        actions = ttk.Frame(frm)
        actions.grid(row=2, column=0, columnspan=2, sticky='e')
        result = {'value': None}

        def _ok():
            val = var_date.get().strip()
            try:
                dt = datetime.datetime.strptime(val, '%Y-%m-%d')
                result['value'] = dt.strftime('%Y-%m-%d')
                dlg.destroy()
            except ValueError:
                messagebox.showerror('Nieprawidłowa data', 'Użyj formatu RRRR-MM-DD, np. 2025-11-05.')

        ttk.Button(actions, text='OK', command=_ok).grid(row=0, column=0)
        dlg.bind('<Return>', lambda e: _ok())
        dlg.bind('<Escape>', lambda e: dlg.destroy())
        dlg.update_idletasks()
        pr = parent if parent is not None else self
        px = pr.winfo_rootx() + (pr.winfo_width() - dlg.winfo_width()) // 2
        py = pr.winfo_rooty() + (pr.winfo_height() - dlg.winfo_height()) // 2
        dlg.geometry(f'+{max(px, 0)}+{max(py, 0)}')
        ent.focus_set()
        dlg.wait_window()
        return result['value']

    @staticmethod
    def pobierz_date_od_uzytkownika(parent_window=None, domyslny_format='%Y-%m-%d'):
        today_str = datetime.datetime.now().strftime(domyslny_format)
        while True:
            value = simpledialog.askstring(title='Data złożenia oświadczenia',
                                           prompt=f'Podaj datę w formacie DD.MM.RRRR:\n\nDomyślnie: {today_str}',
                                           initialvalue=today_str, parent=parent_window)
            if value is None:
                return None
            value = value.strip()
            try:
                dt = datetime.datetime.strptime(value, '%Y-%m-%d')
                return dt.strftime(domyslny_format)
            except ValueError:
                messagebox.showerror('Nieprawidłowa data', 'Użyj formatu RRRR.MM.DD, np. 2025.02.11.')

    def input_text_dialog(self, title='Wpisz wartość', prompt='Podaj tekst:', initial=''):
        dlg = tk.Toplevel(self)
        dlg.title(title)
        dlg.transient(self)
        dlg.resizable(False, False)
        dlg.grab_set()
        frm = ttk.Frame(dlg, padding=12)
        frm.grid(row=0, column=0)
        ttk.Label(frm, text=prompt).grid(row=0, column=0, sticky='w')
        var_txt = tk.StringVar(value=initial)
        ent = ttk.Entry(frm, textvariable=var_txt, width=40)
        ent.grid(row=1, column=0, sticky='we', pady=(4, 10))

        result = {'value': None}

        def _ok():
            result['value'] = var_txt.get().strip()
            dlg.destroy()

        def _cancel():
            result['value'] = None
            dlg.destroy()

        btns = ttk.Frame(frm)
        btns.grid(row=2, column=0, sticky='e')
        ttk.Button(btns, text='OK', command=_ok).grid(row=0, column=1)
        dlg.bind('<Return>', lambda e: _ok())
        dlg.bind('<Escape>', lambda e: _cancel())
        dlg.update_idletasks()
        px = self.winfo_rootx() + (self.winfo_width() - dlg.winfo_width()) // 2
        py = self.winfo_rooty() + (self.winfo_height() - dlg.winfo_height()) // 2
        dlg.geometry(f'+{max(px, 0)}+{max(py, 0)}')
        ent.focus_set()
        dlg.wait_window()
        return result['value']