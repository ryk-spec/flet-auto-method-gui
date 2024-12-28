from flet import Page,Dropdown,app,Text
from layout import GridApp
from widget import InputWidget
import flet as ft
def main(page: Page):
    """
    cellsはcontainer型のリストのリスト
    cells.contentにはColumnsが入ってるので，そこにウィジェットを逐次追加せよ

    Args:
        page (Page): _description_
    """
    # グリッドの行数と列数を指定
    rows, cols = 3, 3
    app = GridApp(rows, cols)
    app.build_ui(page)
    app.page.window_width = 1200
    app.page.window_height= 900
    # セルにアクセスして内容を変更する例
    # 例えば、2行3列目のセルのテキストを変更
    app.cells[0][0].width=1200
    app.cells[0][0].height=50
    app.cells[0][0].alignment = ft.alignment.center
    app.cells[0][0].content.controls.append(
        Text(
            "This is GUI program",
            size=24
            )
    )
    app.update()

# Fletアプリケーションの起動
app(target=main)
