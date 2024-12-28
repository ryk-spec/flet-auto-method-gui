from flet import Column, Text, TextField, IconButton, Dropdown, dropdown, ElevatedButton, Row, FilePicker, FilePickerResultEvent, Image, Checkbox

class LogWidget:
    """プログラムのログを記述するウィジェット"""
    def __init__(self):
        self.logs = Column()
    
    def add_log(self, message: str):
        """ログを追加する"""
        self.logs.controls.append(Text(message))
        self.logs.update()
    
    def get_widget(self):
        """ウィジェットを取得する"""
        return self.logs


class FileDialogWidget:
    """ファイル名入力フィールドとファイルダイアログを連携するウィジェット"""
    def __init__(self, placeholder: str, callback):
        """
        placeholder: 入力フィールドのプレースホルダー
        callback: ファイル選択後に実行する関数
        """
        self.file_picker = FilePicker(on_result=self._on_file_picked)
        self.text_field = TextField(expand=True)
        self.icon_button = IconButton(
            icon="folder_open",
            on_click=lambda e: self.file_picker.pick_files()
        )
        self.widget = Row([self.text_field, self.icon_button], expand=True)
        self.callback = callback
    
    def _on_file_picked(self, e: FilePickerResultEvent):
        if e.files:
            # 選択されたファイルのパスを入力フィールドに表示
            file_path = e.files[0].path
            self.text_field.value = file_path
            self.text_field.update()
            # コールバック関数にファイルパスを渡す
            self.callback(file_path)
        else:
            self.callback(None)
    
    def get_widget(self):
        """ウィジェットを取得する"""
        return [self.file_picker, self.widget]


class DropdownWidget:
    """ドロップダウンウィジェット"""
    def __init__(self, label: str, options: list, callback):
        """
        label: ドロップダウンのラベル
        options: ドロップダウンの選択肢（リスト形式）
        callback: 選択後に実行する関数
        """
        self.label = Text(label)
        self.dropdown = Dropdown(
            options=[dropdown.Option(option) for option in options],
        )
        self.widget = Column([self.label, self.dropdown])
    
    def get_widget(self):
        """ウィジェットを取得する"""
        return self.widget


class ImageWidget:
    """画像を表示するウィジェット"""
    def __init__(self, image_url: str):
        """
        image_url: 初期画像のURL
        """
        self.image = Image(src=image_url, width=200, height=200)
    
    def update_image(self, new_image_url: str):
        """画像を更新する"""
        self.image.src = new_image_url
        self.image.update()
    
    def get_widget(self):
        """ウィジェットを取得する"""
        return self.image


class InputWidget:
    """変数を取得するためのウィジェット"""
    def __init__(self, label: str, callback):
        """
        label: ユーザー入力のラベル
        callback: 入力値を処理する関数
        """
        self.label = Text(label)
        self.text_field = TextField()
        self.submit_button = ElevatedButton("Submit", on_click=lambda e: callback(self.text_field.value))
        self.widget = Column([self.label, self.text_field, self.submit_button])
    
    def get_widget(self):
        """ウィジェットを取得する"""
        return self.widget


