import flet as ft
from flet import Page, Row, Column, Container, Text,Dropdown

class GridApp:
    def __init__(self, rows: int, cols: int):
        """
        グリッドアプリケーションを初期化します。

        :param rows: グリッドの行数
        :param cols: グリッドの列数
        """
        self.rows = rows
        self.cols = cols
        self.cells : list[list[Container]] = [[None for row in range(rows)] for col in range(cols)]
        print(self.cells)

    def build_ui(self, page: Page):
        """
        UIを構築し、ページに追加します。

        :param page: FletのPageオブジェクト
        """
        self.page = page
        grid_rows = []
        for r in range(self.rows):
            grid_cols = []
            for c in range(self.cols):
                # セルのContainerを生成
                cell = Container(
                    width=100,
                    height=50,
                    content=Column(scroll=ft.ScrollMode.ALWAYS)
                )
                grid_cols.append(cell)
                # セルをリストに保存
                self.cells[r][c] = cell
            # 各行のRowを生成
            row = Row(controls=grid_cols)
            grid_rows.append(row)
        
        # 親のColumnに全てのRowを追加
        layout = Column(controls=grid_rows)
        self.layout = layout
        page.add(layout)
    
    def update(self):
        
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].update()

    def __getitem__(self, index):
        """
        layout[i][j] の形式でセルにアクセスできるようにします。

        :param index: 行番号（0から始まる）
        :return: 指定行のセルリスト
        """
        if 0 <= index < self.rows:
            return self.cells[index]
        else:
            raise IndexError("行番号が範囲外です。")

