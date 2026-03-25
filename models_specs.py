import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

def get_employment_day_1():
    today = datetime.date.today()
    current_1 = datetime.date(today.year, today.month, 1)
    if today.month == 12:
        next_1 = datetime.date(today.year + 1, 1, 1)
    else:
        next_1 = datetime.date(today.year, today.month + 1, 1)
    target = current_1 if abs((today - current_1).days) <= abs((next_1 - today).days) else next_1
    for i in range(0, 7):
        candidate = target + datetime.timedelta(days=i)
        if candidate.weekday() < 5:
            return candidate

def get_employment_day_15():
    today = datetime.date.today()
    try:
        current_15 = datetime.date(today.year, today.month, 15)
    except ValueError:
        current_15 = None
    if today.month == 12:
        next_15 = datetime.date(today.year + 1, 1, 15)
    else:
        next_15 = datetime.date(today.year, today.month + 1, 15)
    if current_15:
        target = current_15 if abs((today - current_15).days) <= abs((next_15 - today).days) else next_15
    else:
        target = next_15
    for i in range(0, 7):
        candidate = target + datetime.timedelta(days=i)
        if candidate.weekday() < 5:
            return candidate

@dataclass(frozen=True)
class SectionSpec:
    name: str
    columns: List[str]
    filter_labels: List[str]
    tree_attr: str
    original_data_attr: str
    fetch_method: str
    hidden_columns: Tuple[str, ...] = ()
    filter_col_map: Optional[Dict[str, int]] = None
    use_custom_style: bool = False

SECTION_SPECS: Dict[str, SectionSpec] = {
    'LAPTOPY': SectionSpec(name='LAPTOPY', columns=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'NR SRODKA TRWALEGO', 'NAZWA LAPTOPA', 'NR SERYJNY', 'MODEL', 'NR SDJ', 'UWAGI', 'ID'], filter_labels=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'NR SRODKA TRWALEGO', 'NAZWA LAPTOPA', 'NR SERYJNY', 'MODEL', 'NR SDJ', 'UWAGI'], tree_attr='tabela', original_data_attr='original_data', fetch_method='pobierz_dane_laptopy', hidden_columns=('ID',)),
    'MONITORY': SectionSpec(name='MONITORY', columns=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'NR SERYJNY', 'MODEL', 'NR SDJ', 'UWAGI', 'ID'], filter_labels=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'NR SERYJNY', 'MODEL', 'NR SDJ', 'UWAGI'], tree_attr='tabela_monitory', original_data_attr='original_data_monitory', fetch_method='pobierz_dane_monitory', hidden_columns=('ID',)),
    'TELEFONY': SectionSpec(name='TELEFONY', columns=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'IMEI', 'LADOWARKA', 'KABEL \nUSB C', 'LADOWARKA INDUKCYJNA', 'PRZEJSCIOWKA DO TELEFONU', 'ETUI', 'NR TELEFONU', 'MODEL', 'NR SDJ', 'UWAGI', 'ID'], filter_labels=['NR KADROWY', 'NAZWISKO', 'STATUS', 'IMEI', 'NR TELEFONU', 'MODEL', 'NR SDJ', 'UWAGI'], tree_attr='tabela_telefony', original_data_attr='original_data_telefony', fetch_method='pobierz_dane_telefony', hidden_columns=('ID',), filter_col_map={'NR KADROWY': 0, 'NAZWISKO': 2, 'STATUS': 3, 'IMEI': 4, 'NR TELEFONU': 10, 'MODEL': 11, 'NR SDJ': 12, 'UWAGI': 13}, use_custom_style=True),
    'SŁUCHAWKI': SectionSpec(name='SŁUCHAWKI', columns=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'NR SERYJNY', 'MODEL', 'NR SDJ', 'UWAGI', 'ID'], filter_labels=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'NR SERYJNY', 'MODEL', 'NR SDJ', 'UWAGI'], tree_attr='tabela_sluchawki', original_data_attr='original_data_sluchawki', fetch_method='pobierz_dane_sluchawki', hidden_columns=('ID',)),
    'KARTY SIM': SectionSpec(name='KARTY SIM', columns=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'NR TELEFONU', 'NR SIM', 'OPERATOR', 'NR SDJ', 'UWAGI', 'ID'], filter_labels=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'NR TELEFONU', 'NR SIM', 'OPERATOR', 'NR SDJ', 'UWAGI'], tree_attr='tabela_karty_sim', original_data_attr='original_data_karty_sim', fetch_method='pobierz_dane_karty_sim', hidden_columns=('ID',)),
    'ROUTER': SectionSpec(name='ROUTER', columns=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'IMEI', 'NR TELEFONU', 'NR SIM', 'OPERATOR', 'NR SDJ', 'UWAGI', 'ID'], filter_labels=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'IMEI', 'NR TELEFONU', 'NR SIM', 'OPERATOR', 'NR SDJ', 'UWAGI'], tree_attr='tabela_router', original_data_attr='original_data_router', fetch_method='pobierz_dane_router', hidden_columns=('ID',)),
    'MYSZKI': SectionSpec(name='MYSZKI', columns=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'NR SDJ', 'UWAGI', 'ID'], filter_labels=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'NR SDJ', 'UWAGI'], tree_attr='tabela_myszki', original_data_attr='original_data_myszki', fetch_method='pobierz_dane_myszki', hidden_columns=('ID',)),
    'KLAWIATURY': SectionSpec(name='KLAWIATURY', columns=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'NR SDJ', 'UWAGI', 'ID'], filter_labels=['NR KADROWY', 'IMIE', 'NAZWISKO', 'STATUS', 'NR SDJ', 'UWAGI'], tree_attr='tabela_klawiatury', original_data_attr='original_data_klawiatury', fetch_method='pobierz_dane_klawiatury', hidden_columns=('ID',)),
    'KONTA UŻYTKOWNIKÓW': SectionSpec(name='KONTA UŻYTKOWNIKÓW', columns=['NR KADROWY', 'IMIE', 'NAZWISKO', 'RODZAJ ZATRUDNIENIA', 'LOKALIZACJA', 'ID_UZYTKOWNIKA'], filter_labels=['NR KADROWY', 'IMIE', 'NAZWISKO', 'RODZAJ ZATRUDNIENIA', 'LOKALIZACJA'], tree_attr='tabela_konta', original_data_attr='original_data_konta', fetch_method='pobierz_dane_konta_uzytkownikow', hidden_columns=('ID_UZYTKOWNIKA',))
}

@dataclass(frozen=True)
class FieldSpec:
    label: str
    kind: str = 'entry'
    readonly: bool = False
    default: Union[str, int] = ''
    options_sql: Optional[str] = None
    width: int = 40
    height: int = 5