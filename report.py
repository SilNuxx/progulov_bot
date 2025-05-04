from fpdf import FPDF

import config

class Report(FPDF):
    
    def init(self):
        for font in config.fonts:
            self.add_font(fname=f"font/{font}")

    def create_headers(self, title, report_info):
        self.init()
        self.set_font("Times New Roman - Bold", size=14)
        self.add_page()

        for string in title, report_info:
            width = self.get_string_width(string)
            self.set_x((210 - width) / 2)
            self.cell(width, 10, string)
            self.ln(10)

    def create_table(self, list_truancy):
        self.set_font("Times New Roman", size=12)

        with self.table(
            first_row_as_headings=False,
            line_height=self.font_size,
            col_widths=(8, 30, 10, 10, 10, 10, 10, 10, 10, 10),
            text_align=("CENTER", "CENTER", "CENTER", "CENTER", "CENTER", "CENTER", "CENTER", "CENTER", "CENTER", "CENTER", )
        ) as table:
            # Название колонок
            first_row = table.row()
            first_row.cell("№п/п", rowspan=2)
            first_row.cell("ФИО Студента", rowspan=2)
            first_row.cell("Дней", colspan=4)
            first_row.cell("Уроков", colspan=4)

            second_row = table.row()
            second_row.cell("всего")
            second_row.cell("по болезни")
            second_row.cell("уваж. причина")
            second_row.cell("без уваж.")
            second_row.cell("всего")
            second_row.cell("по болезни")
            second_row.cell("уваж. причина")
            second_row.cell("без уваж.")

            # Заполнение таблицы
        