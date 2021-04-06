
from ...report_scripts.weekly.weekly import Sh2
from ...classes.styles import st
from ...classes.data import get_max_row
from ..report_setting import (
    CLUSTER_GROUP,
    CLUSTER_LIST,
)


class Data(Sh2):
    new_report = 'Количество чеков.xlsx'
    sheet_name = 'ФМ'

    data = [[CLUSTER_LIST],
            [st['smoky20']]]
    head_list = [['Счит. QR', 'Чеки', 'QR / Чеки'],
                 [st['apricot40'], st['apricot60'], st['apricot80']]]
    value = {}
    summary = []
    receiving_data = {}
    chart = False

    def create_template(self):
        self.high = {}
        self.width = {'A': 18, }
        self.image = {}
        self.rows_group = {}
        self.columns_group = {}
        self.merge = {}
        self.cells = {'A1': ['Кластер', st['blue20']],
                      'B1': ['Чеки', st['blue20']],
                      }

        self.add_cells_by_rows(self.data[0],
                               self.data[1],
                               start_row=2,
                               start_column=1)

        self.max_row = 1 + get_max_row(self.cells.keys())

    def create_mutable_part(self):
        self.reared('count', read_only=False)

        last_column = self.wb.sheet_r.max_column
        column_list = list(range(4, last_column))

        amount = self.wb.get_data(CLUSTER_GROUP, [1, 2], column_list, 'COUNT')

        value = [amount.get(clust, 0) for clust in CLUSTER_LIST]

        self.add_cells_by_rows([value],
                               self.data[1],
                               start_row=2,
                               start_column=2)
