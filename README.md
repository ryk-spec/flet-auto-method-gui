# flet-auto-method-gui

fletで動的にメソッド入力画面を生成

## ユーザが定義するメソッド（以下、ターゲットメソッド）が満足すべき条件

### 名前付き引数とデフォルト値をもつ関数であること

- ターゲットメソッドは、以下のように 名前付き引数（キーワード引数）をもち、デフォルト値が設定されている関数 として定義してください。

```python
def target_method(
    param1=default1,
    param2=default2,
    ...
)
```

- デフォルト値が指定されていない場合、GUI 側では入力欄が空の状態で表示されます。実装上の都合で必須引数（デフォルト値なし）を使用する場合も可能ですが、ユーザに入力を促す必要があるため推奨されません。

### デフォルト値として扱える型
   
- 標準の組み込み型
  
  - str / int / float / bool などの Python 組み込み型。
   
  - None も許容されます。

- 本モジュール独自の型

  - `FileInput` : GUI 上に「ファイル選択ボタンとテキスト欄」が自動生成されます。
  - `ChoiceInput` : GUI 上に「ドロップダウンリスト」が自動生成されます。

  - これらをデフォルト値として指定すると、Flet UIBuilder が自動的に対応する入力フォームを生成します。

```python
def target_method(
    file=FileInput("Select a file"),
    choice=ChoiceInput(["Option A", "Option B", "Option C"])
):
```

### printした内容

- GUI上に表示されます。画像をprintすると画像が表示されます。
