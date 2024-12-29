import flet as ft
import os

class WidgetConfig:
    
    def __init__(self,type,label,default,options=None):
        
        self.type : str = type
        self.label : str = label
        self.default : str = default
        self.options : list|tuple = options
        
class ParameterLogViewer:
    def __init__(self, page, parameter_config,callback):
        """
        :param page: Fletのページオブジェクト
        :param parameter_config: パラメータ設定 (key: パラメータ名, value: 入力形式情報)
        """
        self.page : ft.Page = page
        self.parameter_config : dict[str,WidgetConfig] = parameter_config
        self.inputs : dict = {}  # 各ウィジェットを格納する辞書
        self.callback = callback
        self.log = "# This is start of logfile\n"
        self.build_and_add_to_page()  # 初期化時にページに追加

    def add_log(self,msg):
        
        self.log += msg+"\n"
    def get_parameters(self):
        """
        各入力ウィジェットから値を取得し、辞書形式で返す。
        """
        result = {}
        for name, widget in self.inputs.items():
            if isinstance(widget, ft.TextField):
                result[name] = widget.value
            elif isinstance(widget, ft.Dropdown):
                result[name] = widget.value
            elif isinstance(widget, ft.FilePickerResultEvent):
                result[name] = widget.files[0].name if widget.files else None
        return result

    def build_and_add_to_page(self):
        """
        ウィジェットを動的に生成し、ページに追加。
        """
        self.page.window_width = 1200
        self.page.window_height = 600
        self.param_col = ft.Column(width=500,height=300,scroll=ft.ScrollMode.ALWAYS)
        self.buttons = ft.Row(width=500,height=200,scroll=ft.ScrollMode.ALWAYS)
        self.output_col = ft.Column(width=500,height=500,scroll=ft.ScrollMode.ALWAYS)
        self.layout = ft.Container(
            content=ft.Row([
                ft.Column([self.param_col,self.buttons]),
                self.output_col]),  
            bgcolor=  ft.colors.AMBER_100
        )
        self.page.add(self.layout)
        self.inputs={}
        
        widgets = []
        for name, config in self.parameter_config.items():
            if config.type in ["str","int","list","float"]:
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
                    label= config.label,
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
                field = ft.TextField(label= config.label,width=300,height=50)
                file_picker_button = ft.ElevatedButton(
                    text="select",
                    icon=ft.icons.FILE_UPLOAD_ROUNDED,
                    on_click=lambda e, p=file_picker: p.pick_files(
                        allow_multiple=False,
                        initial_directory=os.curdir)
                )
                widgets.append(ft.Row([field,file_picker_button]))
                self.inputs[name] = field

            elif config.type == "files":
                def file_register(e: ft.FilePickerResultEvent):
                    field.value = [file.path for file in e.files]
                    self.page.update()
                file_picker = ft.FilePicker(on_result=file_register)
                self.page.add(file_picker)
                field = ft.TextField(label= config.label,width=300,height=50)
                file_picker_button = ft.ElevatedButton(
                    text="select",
                    icon=ft.icons.FILE_UPLOAD_ROUNDED,
                    on_click=lambda e, p=file_picker: p.pick_files(
                        allow_multiple=True,
                        initial_directory=os.curdir)
                )
                widgets.append(ft.Row([field,file_picker_button]))
                self.inputs[name] = field

            elif config.type == "dir":
                def file_register(e: ft.FilePickerResultEvent):
                    field.value = e.path
                    self.page.update()
                file_picker = ft.FilePicker(on_result=file_register)
                self.page.add(file_picker)
                field = ft.TextField(label= config.label,width=300,height=50)
                file_picker_button = ft.ElevatedButton(
                    text="select",
                    icon=ft.icons.FILE_UPLOAD_ROUNDED,
                    on_click=lambda e, p=file_picker: p.get_directory_path(
                        initial_directory=os.curdir)
                )
                widgets.append(ft.Row([field,file_picker_button]))
                self.inputs[name] = field

        execute_button = ft.ElevatedButton("実行",on_click=self.callback)

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
        self.param_col.controls.append(ft.Row([execute_button,save_button,log_button]))
        self.log_text = ft.Text(self.log)
        self.output_col.controls.append(self.log_text)
        self.page.update()
        
 

    def _show_log(self, e):
        """
        ログを画面に出力。
        """
        self.log_text.value = self.log
        self.page.update()

    def _save_log_to_file(self, e):
        """
        ログをファイルに保存。
        """
        log_filename = "log.txt"
        with open(log_filename, "w", encoding="utf-8") as f:
                f.write(self.log)
        self.page.add(ft.Text(f"ログを {log_filename} に保存しました。"))

# メインアプリケーション
def main(page: ft.Page):
    page.title = "動的パラメータ入力とログ機能"
    page.scroll = "auto"

    # パラメータ設定
    parameter_config = {
        "text_param": WidgetConfig(
            type="dir",label="テキスト入力",
            default="opt1")
    }

    # コールバック関数を登録
    def on_execute_action(parameters):
        pass

    # パラメータ収集UIを作成
    collector = ParameterLogViewer(page=page, parameter_config=parameter_config,callback=on_execute_action)


    # collector.add_execute_callback(on_execute_action)

# アプリケーションの実行
ft.app(target=main)
