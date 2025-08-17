import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from datetime import datetime
from main import ImprovedSummarizer


class SummarizationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("日本語テキスト要約システム")
        self.root.geometry("800x750")
        self.root.resizable(True, True)

        # 変数の初期化
        self.input_file_path = tk.StringVar()
        self.output_file_path = tk.StringVar()
        self.granularity = tk.StringVar(value="medium")
        self.similarity_limit = tk.DoubleVar(value=0.3)
        self.min_sentences = tk.IntVar(value=3)
        self.max_sentences = tk.IntVar(value=20)

        # 要約システムの初期化
        self.summarizer = ImprovedSummarizer()

        self.create_widgets()

    def create_widgets(self):
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # タイトル
        title_label = ttk.Label(main_frame, text="日本語テキスト要約システム",
                                font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # 入力ファイル選択
        input_frame = ttk.LabelFrame(main_frame, text="入力ファイル設定", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3,
                         sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(input_frame, text="入力ファイル:").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Entry(input_frame, textvariable=self.input_file_path,
                  width=50).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(input_frame, text="参照",
                   command=self.browse_input_file).grid(row=0, column=2)

        # 出力ファイル設定
        output_frame = ttk.LabelFrame(
            main_frame, text="出力ファイル設定", padding="10")
        output_frame.grid(row=2, column=0, columnspan=3,
                          sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(output_frame, text="出力ファイル:").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Entry(output_frame, textvariable=self.output_file_path,
                  width=50).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(output_frame, text="参照",
                   command=self.browse_output_file).grid(row=0, column=2)

        # 自動生成チェックボックス
        self.auto_generate = tk.BooleanVar(value=True)
        ttk.Checkbutton(output_frame, text="ファイル名を自動生成",
                        variable=self.auto_generate,
                        command=self.toggle_output_file).grid(row=1, column=1, sticky=tk.W, pady=(5, 0))

        # 要約パラメータ設定
        params_frame = ttk.LabelFrame(main_frame, text="要約パラメータ", padding="10")
        params_frame.grid(row=3, column=0, columnspan=3,
                          sticky=(tk.W, tk.E), pady=(0, 10))

        # 粒度レベル
        ttk.Label(params_frame, text="粒度レベル:").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10))
        granularity_combo = ttk.Combobox(params_frame, textvariable=self.granularity,
                                         values=["fine", "medium", "coarse"], state="readonly", width=15)
        granularity_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))

        # 類似性閾値
        ttk.Label(params_frame, text="類似性閾値:").grid(
            row=0, column=2, sticky=tk.W, padx=(0, 10))
        similarity_scale = ttk.Scale(params_frame, from_=0.1, to=0.5,
                                     variable=self.similarity_limit, orient=tk.HORIZONTAL, length=150)
        similarity_scale.grid(row=0, column=3, sticky=tk.W, padx=(0, 10))
        ttk.Label(params_frame, textvariable=tk.StringVar(
            value="0.3")).grid(row=0, column=4)

        # 文数設定
        ttk.Label(params_frame, text="最小文数:").grid(
            row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        min_spin = ttk.Spinbox(params_frame, from_=1, to=50,
                               textvariable=self.min_sentences, width=10)
        min_spin.grid(row=1, column=1, sticky=tk.W, padx=(0, 20), pady=(10, 0))

        ttk.Label(params_frame, text="最大文数:").grid(
            row=1, column=2, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        max_spin = ttk.Spinbox(params_frame, from_=1, to=100,
                               textvariable=self.max_sentences, width=10)
        max_spin.grid(row=1, column=3, sticky=tk.W, padx=(0, 10), pady=(10, 0))

        # テキスト表示エリア
        text_frame = ttk.LabelFrame(main_frame, text="テキスト内容", padding="10")
        text_frame.grid(row=4, column=0, columnspan=3, sticky=(
            tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        # 入力テキスト
        ttk.Label(text_frame, text="入力テキスト:").grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.input_text = scrolledtext.ScrolledText(
            text_frame, height=8, width=80)
        self.input_text.grid(row=1, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        # 要約結果
        ttk.Label(text_frame, text="要約結果:").grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.output_text = scrolledtext.ScrolledText(
            text_frame, height=8, width=80)
        self.output_text.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # ボタンエリア
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)

        ttk.Button(button_frame, text="テキストを読み込み",
                   command=self.load_text, style="Accent.TButton").grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="要約実行",
                   command=self.run_summarization, style="Accent.TButton").grid(row=0, column=1, padx=(0, 10))
        ttk.Button(button_frame, text="クリア",
                   command=self.clear_all).grid(row=0, column=2, padx=(0, 10))
        ttk.Button(button_frame, text="終了",
                   command=self.root.quit).grid(row=0, column=3)

        # ステータスバー
        self.status_var = tk.StringVar(value="準備完了")
        status_bar = ttk.Label(
            main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, columnspan=3,
                        sticky=(tk.W, tk.E), pady=(10, 0))

        # グリッドの重み設定
        main_frame.columnconfigure(1, weight=1)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(1, weight=1)
        text_frame.rowconfigure(3, weight=1)

        # 初期設定
        self.toggle_output_file()

    def browse_input_file(self):
        """入力ファイルを選択"""
        file_path = filedialog.askopenfilename(
            title="入力ファイルを選択",
            filetypes=[("テキストファイル", "*.txt"), ("すべてのファイル", "*.*")]
        )
        if file_path:
            self.input_file_path.set(file_path)
            self.load_text()

    def browse_output_file(self):
        """出力ファイルを選択"""
        file_path = filedialog.asksaveasfilename(
            title="出力ファイルを保存",
            defaultextension=".txt",
            filetypes=[("テキストファイル", "*.txt"), ("すべてのファイル", "*.*")]
        )
        if file_path:
            self.output_file_path.set(file_path)

    def toggle_output_file(self):
        """出力ファイル名の自動生成を切り替え"""
        if self.auto_generate.get():
            self.output_file_path.set("")
            # 出力ファイルのEntryを無効化
            for child in self.root.winfo_children():
                if isinstance(child, ttk.Frame):
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, ttk.LabelFrame) and "出力ファイル設定" in grandchild.cget("text"):
                            for greatgrandchild in grandchild.winfo_children():
                                if isinstance(greatgrandchild, ttk.Entry):
                                    greatgrandchild.config(state="disabled")
        else:
            # 出力ファイルのEntryを有効化
            for child in self.root.winfo_children():
                if isinstance(child, ttk.Frame):
                    for grandchild in child.winfo_children():
                        if isinstance(grandchild, ttk.LabelFrame) and "出力ファイル設定" in grandchild.cget("text"):
                            for greatgrandchild in grandchild.winfo_children():
                                if isinstance(greatgrandchild, ttk.Entry):
                                    greatgrandchild.config(state="normal")

    def load_text(self):
        """テキストファイルを読み込み"""
        file_path = self.input_file_path.get()
        if not file_path:
            messagebox.showwarning("警告", "入力ファイルが選択されていません。")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(1.0, content)
                self.status_var.set(
                    f"ファイル '{os.path.basename(file_path)}' を読み込みました")
        except Exception as e:
            messagebox.showerror("エラー", f"ファイルの読み込みに失敗しました: {e}")
            self.status_var.set("ファイル読み込みエラー")

    def run_summarization(self):
        """要約を実行"""
        # 入力チェック
        if not self.input_file_path.get():
            messagebox.showwarning("警告", "入力ファイルが選択されていません。")
            return

        input_content = self.input_text.get(1.0, tk.END).strip()
        if not input_content:
            messagebox.showwarning("警告", "入力テキストが空です。")
            return

        try:
            self.status_var.set("要約処理中...")
            self.root.update()

            # 要約実行
            result_dict, target_sentences = self.summarizer.summarize_with_granularity(
                input_content,
                self.granularity.get(),
                self.similarity_limit.get(),
                self.min_sentences.get(),
                self.max_sentences.get()
            )

            # 後処理
            summary_sentences = result_dict["summarize_result"]
            improved_summary = self.summarizer.post_process_summary(
                summary_sentences, input_content)

            # 出力ファイル名の決定
            if self.auto_generate.get():
                current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                input_filename = os.path.splitext(
                    os.path.basename(self.input_file_path.get()))[0]
                output_filename = f"要約結果_{input_filename}_{self.granularity.get()}_{current_time}.txt"
                output_path = output_filename
            else:
                output_path = self.output_file_path.get()
                if not output_path:
                    messagebox.showwarning("警告", "出力ファイル名が指定されていません。")
                    return

            # 結果の表示
            output_content = f"""=== 要約結果 ===
粒度レベル: {self.granularity.get()}
目標文数: {target_sentences}
実際の文数: {len(improved_summary)}
類似性閾値: {self.similarity_limit.get()}
実行時刻: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

【要約】
{chr(10).join(improved_summary)}

【元文書の文数】: {len(input_content.split('。'))}
【要約率】: {len(improved_summary) / len(input_content.split('。')) * 100:.1f}%
"""

            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, output_content)

            # ファイルに保存
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output_content)

            self.status_var.set(f"要約完了！出力ファイル: {output_path}")
            messagebox.showinfo("完了", f"要約が完了しました。\n出力ファイル: {output_path}")

        except Exception as e:
            error_msg = f"要約処理中にエラーが発生しました: {e}"
            self.status_var.set("エラーが発生しました")
            messagebox.showerror("エラー", error_msg)

    def clear_all(self):
        """すべての内容をクリア"""
        self.input_text.delete(1.0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.input_file_path.set("")
        self.output_file_path.set("")
        self.status_var.set("準備完了")


def main():
    root = tk.Tk()
    app = SummarizationGUI(root)

    # ウィンドウを中央に配置
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_width() // 2)
    root.geometry(f"+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    main()
