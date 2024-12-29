import flet as ft
import os

class WidgetConfig:
    """
    ウィジェットの設定を保持するクラス。

    :param type: ウィジェットの種類 (例: 'str', 'int', 'dropdown', 'file', など)
    :param label: ウィジェットに表示するラベル
    :param default: ウィジェットの初期値
    :param options: オプション (dropdown の選択肢など)
    """
    def __init__(self, type, label, default, options=None):
        self.type: str = type
        self.label: str = label
        self.default: str = default
        self.options: list | tuple = options

class ParameterLogViewer:
    """
    Fletを使用したパラメータ入力とログビューア。

    :param page: Fletのページオブジェクト
    :param parameter_config: パラメータ設定 (key: パラメータ名, value: WidgetConfigオブジェクト)
    :param callback: 実行ボタンが押された際に呼び出されるコールバック関数
    """
    def __init__(self, page, parameter_config):
        self.page: ft.Page = page
        self.parameter_config: dict[str, WidgetConfig] = parameter_config
        self.inputs: dict = {}  # 各ウィジェットを格納する辞書
        self.log = "# This is start of logfile\n"

    def add_log(self, msg):
        """
        ログに新しいメッセージを追加する。

        :param msg: 追加するメッセージ
        """
        self.log += msg + "\n"

    def get_parameters(self):
        """
        各入力ウィジェットから値を取得し、辞書形式で返す。

        :return: パラメータ名をキーとする辞書
        """
        result = {}
        for name, widget in self.inputs.items():
            result[name] = widget.value
            if self.parameter_config[name].type == "float":
                result[name] = float(result[name])
            elif self.parameter_config[name].type == "int":
                result[name] = int(result[name])
        return result

    def build_and_add_to_page(self,callback):
        """
        ウィジェットを動的に生成し、ページに追加する。
        """
        self.param_col = ft.Column(width=600, height=800, scroll=ft.ScrollMode.AUTO)
        self.buttons = ft.Row(width=600, height=100,scroll=ft.ScrollMode.AUTO)
        self.output_col = ft.Column(width=600, height=900, scroll=ft.ScrollMode.AUTO)
        self.layout = ft.Container(
            content=ft.Row([
                ft.Column([self.param_col, self.buttons]),
                self.output_col]
                ),  
        )
        self.page.add(self.layout)
        self.inputs = {}

        widgets = []
        for name, config in self.parameter_config.items():
            if config.type in ["str", "int", "list", "float"]:
                field = ft.TextField(
                    label=config.label, 
                    value=config.default,
                    width=300,
                    height=50
                )
                self.inputs[name] = field
                self.param_col.controls.append(field)
            elif config.type == "dropdown":
                field = ft.Dropdown(
                    label=config.label,
                    options=[ft.dropdown.Option(opt) for opt in config.options],
                    width=300,
                    height=50
                )
                self.param_col.controls.append(field)
                self.inputs[name] = field
            elif config.type == "file":
                def file_register(e: ft.FilePickerResultEvent):
                    field.value = e.files[0].path
                    self.page.update()
                file_picker = ft.FilePicker(on_result=file_register)
                self.page.add(file_picker)
                field = ft.TextField(label=config.label, width=300, height=50)
                file_picker_button = ft.ElevatedButton(
                    text="select",
                    width=50,
                    height=50,
                    icon=ft.icons.FILE_UPLOAD_ROUNDED,
                    on_click=lambda e, p=file_picker: p.pick_files(
                        allow_multiple=False,
                        initial_directory=os.curdir)
                )
                widgets.append(ft.Row([field, file_picker_button]))
                self.inputs[name] = field

            elif config.type == "files":
                def file_register(e: ft.FilePickerResultEvent):
                    field.value = [file.path for file in e.files]
                    self.page.update()
                file_picker = ft.FilePicker(on_result=file_register)
                self.page.add(file_picker)
                field = ft.TextField(label=config.label, width=300, height=50)
                file_picker_button = ft.ElevatedButton(
                    text="select",
                    width=50,
                    height=50,
                    icon=ft.icons.FILE_UPLOAD_ROUNDED,
                    on_click=lambda e, p=file_picker: p.pick_files(
                        allow_multiple=True,
                        initial_directory=os.curdir)
                )
                widgets.append(ft.Row([field, file_picker_button]))
                self.inputs[name] = field

            elif config.type == "dir":
                def file_register(e: ft.FilePickerResultEvent):
                    field.value = e.path
                    self.page.update()
                file_picker = ft.FilePicker(on_result=file_register)
                self.page.add(file_picker)
                field = ft.TextField(label=config.label, width=300, height=50)
                file_picker_button = ft.ElevatedButton(
                    text="select",
                    width=50,
                    height=50,
                    icon=ft.icons.FILE_UPLOAD_ROUNDED,
                    on_click=lambda e, p=file_picker: p.get_directory_path(
                        initial_directory=os.curdir)
                )
                widgets.append(ft.Row([field, file_picker_button]))
                self.inputs[name] = field

        execute_button = ft.ElevatedButton("実行", on_click=callback)

        # ログ表示ボタン
        log_button = ft.ElevatedButton(
            "ログを出力",
            on_click=self._show_log,
        )

        # ログ保存ボタン
        save_button = ft.ElevatedButton(
            "ログを保存",
            on_click=self._save_log_to_file,
        )

        # 全てのウィジェットをページに追加
        self.param_col.controls.append(ft.Column(widgets))
        self.buttons.controls.append(ft.Row([execute_button, save_button, log_button]))
        self.log_text = ft.Text(self.log)
        self.output_col.controls.append(self.log_text)
        self.page.update()

    def _show_log(self, e):
        """
        ログを画面に出力する。

        :param e: イベントオブジェクト
        """
        self.log_text.value = self.log
        self.page.update()

    def _save_log_to_file(self, e):
        """
        ログをファイルに保存する。

        :param e: イベントオブジェクト
        """
        log_filename = "log.txt"
        with open(log_filename, "w", encoding="utf-8") as f:
            f.write(self.log)


