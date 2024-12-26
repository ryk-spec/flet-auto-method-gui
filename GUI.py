#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example showing:
1. Class-based method argument analysis (MethodAnalyzer).
2. Mapping param_name -> default_value for building dynamic GUI.
3. Flet-based GUI with custom input types (FileInput, ChoiceInput).
4. Matplotlib figure rendering with MatplotlibChart.
5. Stdout redirection to display print outputs on the GUI.
6. Three-column layout for method arguments, two-column layout for print and figure.
7. Display selected file path in a read-only TextField.
"""

import sys
import inspect
from io import StringIO

import flet as ft
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
from matplotlib.figure import Figure


class FileInput:
    """
    Represents a file selection requirement for a method argument.
    """

    def __init__(self, description: str = "Select a file") -> None:
        self.description = description

    def __str__(self) -> str:
        return f"FileInput(description='{self.description}')"


class ChoiceInput:
    """
    Represents a choice (dropdown) for a method argument.
    """

    def __init__(self, choices: list[str]) -> None:
        self.choices = choices

    def __str__(self) -> str:
        return f"ChoiceInput(choices={self.choices})"


class MethodAnalyzer:
    """
    Analyzes the signature of a given method, extracting the param_name and default_value.
    Stores the results in a dictionary for further use.
    """

    def __init__(self, method):
        self.method = method
        self.signature = inspect.signature(method)
        self.arguments_map: dict[str, object] = {}

    def analyze_arguments(self) -> dict[str, object]:
        """
        Returns a dictionary mapping:
            param_name -> default_value (or None if no default).
        """
        for param_name, param in self.signature.parameters.items():
            default_value = param.default
            if default_value != inspect.Parameter.empty:
                self.arguments_map[param_name] = default_value
            else:
                self.arguments_map[param_name] = None
        return self.arguments_map


class StdoutRedirector:
    """
    Redirects sys.stdout to update a Flet Text or similar UI component in real-time.
    """

    def __init__(self, callback) -> None:
        self._buffer = StringIO()
        self._callback = callback

    def write(self, message: str) -> None:
        self._buffer.write(message)
        self._callback(message)

    def flush(self) -> None:
        """Required for file-like object. (No special action needed here.)"""


class UIBuilder:
    """
    Builds a dynamic Flet GUI based on the analyzed arguments.
    - 3-column layout for arguments
    - 2-column layout for (MatplotlibChart + stdout_text)
    """

    def __init__(self, method, page: ft.Page):
        self.method = method
        self.page = page

        self.analyzer = MethodAnalyzer(method)
        self.arguments_map = self.analyzer.analyze_arguments()

        # Keep track of Flet controls for each argument
        self.input_controls: dict[str, dict] = {}

        # Redirect stdout
        self.original_stdout = sys.stdout
        self.stdout_text = ft.Text(value="==以下にprint内容==", selectable=True, expand=1)
        self.chart = MatplotlibChart(plt.figure(),expand=True)  # dummy figure
        self.stdout_redirector = StdoutRedirector(self.update_stdout_text)
        sys.stdout = self.stdout_redirector

        # Create layout containers for 3 columns (arguments area)
        self.col1 = ft.Column(spacing=10, expand=1,width=450)
        self.col2 = ft.Column(spacing=10, expand=1,width=450)
        self.col3 = ft.Column(spacing=10, expand=1,width=450)
        self.arg_row = ft.Row(controls=[self.col1, self.col2, self.col3], spacing=20)

    def build_ui(self) -> None:
        """
        Builds the UI controls according to the arguments_map.
        Places them in a 3-column layout.
        Then places the Matplotlib chart and stdout text in a 2-column layout.
        """
        # Create input fields
        param_list = list(self.arguments_map.items())
        for idx, (param_name, default_value) in enumerate(param_list):
            # Decide which column to put this control in
            target_col = [self.col1, self.col2, self.col3][idx % 3]

            if isinstance(default_value, FileInput):
                self._add_file_input(target_col, param_name, default_value)
            elif isinstance(default_value, ChoiceInput):
                self._add_choice_input(target_col, param_name, default_value)
            else:
                self._add_text_input(target_col, param_name, default_value)

        # Execute button (placed below the argument columns, or in one column)
        execute_button = ft.ElevatedButton("Execute Method", on_click=self.execute_method)

        # 2-column layout for Matplotlib chart & stdout text
        result_row = ft.Row(
            controls=[
                ft.Row([self.chart],width=750,height=600), 
                ft.Row([self.stdout_text],width=400,height=600)
            ],
            alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=20,
            width=1200, 
        )

        whole_column = ft.Column(
            [
                self.arg_row,
                execute_button
            ]
        )
        self.page.add(whole_column)
        self.page.add(result_row)

        def on_close(_):
            sys.stdout = self.original_stdout

        self.page.on_close = on_close
        self.page.update()

    def _add_file_input(self, target_col: ft.Column, param_name: str, default_value: FileInput) -> None:
        """
        Adds a file picker button and a read-only text field to display the file name.
        """
        file_picker = ft.FilePicker(
            on_result=lambda e, n=param_name: self._on_file_result(e, n),
        )
        self.page.overlay.append(file_picker)

        pick_button = ft.ElevatedButton(
            text=default_value.description,
            on_click=lambda _, fp=file_picker: fp.pick_files(),
            width=100,
        )

        file_name_field = ft.TextField(
            label="Selected file",
            value="",
            read_only=False,
            expand=True,
            width=300
        )

        self.input_controls[param_name] = {
            "type": "file",
            "value": None,  # Will store the file path here
            "button": pick_button,
            "field": file_name_field,
        }

        # Place both the button and text field in the column
        target_col.controls.append(ft.Row([file_name_field,pick_button]))

    def _on_file_result(self, e: ft.FilePickerResultEvent, param_name: str) -> None:
        """
        Updates the input_controls dict with the selected file path,
        displays it in the text field.
        """
        ctrl_info = self.input_controls[param_name]
        if e.files:
            file_path = e.files[0].path
            ctrl_info["value"] = file_path
            ctrl_info["field"].value = file_path
        else:
            ctrl_info["value"] = ""
            ctrl_info["field"].value = ""
        self.page.update()

    def _add_choice_input(self, target_col: ft.Column, param_name: str, default_value: ChoiceInput) -> None:
        """
        Adds a dropdown to the page for the given param_name.
        """
        dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(c) for c in default_value.choices],
            value=default_value.choices[0] if default_value.choices else None,
            width=350
        )
        self.input_controls[param_name] = {
            "type": "choice",
            "dropdown": dropdown,
        }
        target_col.controls.append(dropdown)

    def _add_text_input(self, target_col: ft.Column, param_name: str, default_value: object) -> None:
        """
        Adds a text field to the page for the given param_name.
        """
        default_str = str(default_value) if default_value is not None else ""
        text_field = ft.TextField(
            label=f"{param_name} (default: {default_str})",
            value=default_str,
            width=350
        )
        self.input_controls[param_name] = {
            "type": "text",
            "field": text_field,
        }
        target_col.controls.append(text_field)

    def execute_method(self, _: ft.ControlEvent) -> None:
        """
        Collects input values, calls the method, and updates the GUI with outputs.
        """
        # Clear current stdout text
        self.stdout_text.value = ""

        # Build arguments from input controls
        args_dict = {}
        sig = inspect.signature(self.method)

        for name, ctrl_info in self.input_controls.items():
            param = sig.parameters[name]
            default_val = param.default

            if ctrl_info["type"] == "file":
                args_dict[name] = ctrl_info["value"]
            elif ctrl_info["type"] == "choice":
                args_dict[name] = ctrl_info["dropdown"].value
            elif ctrl_info["type"] == "text":
                raw_value = ctrl_info["field"].value
                # Convert to int if the original default was int
                if isinstance(default_val, int):
                    try:
                        raw_value = int(raw_value)
                    except ValueError:
                        pass
                args_dict[name] = raw_value

        result = self.method(**args_dict)

        # If the method returns a Matplotlib Figure, update the chart
        if isinstance(result, Figure):
            self.chart.figure = result

        self.page.update()

    def update_stdout_text(self, message: str) -> None:
        """
        Append new print outputs to the stdout_text control.
        """
        self.stdout_text.value += message
        self.page.update()


def my_method(
    file: FileInput = FileInput("Upload a file"),
    choice: ChoiceInput = ChoiceInput(["Option 1", "Option 2", "Option 3"]),
    number: int = 5
) -> Figure:
    """
    Example method demonstrating:
    1. FileInput
    2. ChoiceInput
    3. Integer input
    4. Printing outputs (redirected to the Flet UI)
    5. Returning a Matplotlib figure
    """
    print(f"file   : {file}")
    print(f"choice : {choice}")
    print(f"number : {number}")

    fig, ax = plt.subplots(figsize=(4, 3))
    x_data = list(range(1, number + 1))
    y_data = [x**2 for x in x_data]
    ax.plot(x_data, y_data, label="y = x^2", marker="o")
    ax.set_title("Sample Plot")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.legend()

    # Print the figure object
    print(fig)



def gui_run(my_method) -> None:
    """
    Entry point for the Flet application.
    """
    def main(page: ft.Page) -> None:
        """
        Entry point for the Flet application.
        """
        page.title = "Class-based Flet & Matplotlib Demo (3-column & 2-column layout)"
        page.scroll = "auto"

        ui_builder = UIBuilder(my_method, page)
        ui_builder.build_ui()
        page.title = "Class-based Flet & Matplotlib Demo (3-column & 2-column layout)"
        page.scroll = "auto"

        ui_builder = UIBuilder(my_method, page)
        ui_builder.build_ui()
    ft.app(target=main)

gui_run(my_method=my_method)