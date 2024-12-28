from flet import Page, Column, Container,app
from widget import LogWidget, FileDialogWidget, DropdownWidget, ImageWidget, InputWidget

class MyApp:
    """Fletアプリケーションのウィジェット管理クラス"""
    def __init__(self):
        # 各ウィジェットの初期化
        self.log_widget = LogWidget()
        self.file_dialog_widget = FileDialogWidget("Select a file...", self.handle_file)
        self.dropdown_widget = DropdownWidget(
            "Choose an option:", ["Option 1", "Option 2", "Option 3"], self.handle_dropdown
        )
        self.image_widget = ImageWidget("https://via.placeholder.com/150")
        self.input_widget = InputWidget("Enter a value:", self.handle_input)
    
    def handle_file(self, file_path):
        """ファイル選択時の処理"""
        self.log_widget.add_log(file_path)
        if file_path:
            self.log_widget.add_log(f"Selected file: {file_path}")
        else:
            self.log_widget.add_log("No file selected")
    
    def handle_dropdown(self, value):
        """ドロップダウン選択時の処理"""
        self.log_widget.add_log(f"Dropdown selected: {value}")
    
    def handle_input(self, value):
        """入力送信時の処理"""
        self.log_widget.add_log(f"Input value: {value}")
    
    def build_layout(self):
        """ページレイアウトを生成"""
        return Column([
            self.log_widget.get_widget(),
            self.file_dialog_widget.get_widget()[1],  # ファイル入力フィールドとアイコン
            self.dropdown_widget.get_widget(),
            # self.image_widget.get_widget(),
            self.input_widget.get_widget(),
        ],expand=True)
    
    def get_file_picker(self):
        """ファイルピッカーウィジェットを取得"""
        return self.file_dialog_widget.get_widget()[0]

def main(page: Page):
    page.title = "Smart Flet App"

    # アプリケーションクラスを初期化
    app = MyApp()

    # レイアウトを生成してページに追加
    layout = app.build_layout()
    page.add(app.get_file_picker())  # ファイルピッカーを直接追加
    page.add(layout)

# Fletアプリの実行
if __name__ == "__main__":
    app(target=main, view="web_browser", port=8080)