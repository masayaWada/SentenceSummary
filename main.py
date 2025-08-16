from pysummarization.nlp_base import NlpBase
from pysummarization.similarityfilter.tfidf_cosine import TfIdfCosine
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
import argparse
import os
from datetime import datetime


class ImprovedSummarizer:
    def __init__(self):
        self.nlp_base = NlpBase()
        self.nlp_base.tokenizable_doc = MeCabTokenizer()
        self.similarity_filter = TfIdfCosine()
        self.similarity_filter.nlp_base = self.nlp_base
        self.auto_abstractor = AutoAbstractor()
        self.auto_abstractor.tokenizable_doc = MeCabTokenizer()
        self.auto_abstractor.delimiter_list = ["。", "\n"]

    def summarize_with_granularity(self, document, granularity_level="medium", similarity_limit=0.3, min_sentences=3, max_sentences=20):
        """
        粒度レベルに応じた要約を生成

        Args:
            document: 入力テキスト
            granularity_level: 粒度レベル ("fine", "medium", "coarse")
            similarity_limit: 類似性フィルターの閾値
            min_sentences: 最小文数
            max_sentences: 最大文数
        """

        # 粒度レベルに応じたパラメータ調整
        if granularity_level == "fine":
            # 詳細な要約：多くの文を含み、類似性フィルターを緩く
            similarity_limit = 0.4
            target_sentences = min(max_sentences, max(
                min_sentences, int(len(document.split("。")) * 0.4)))
        elif granularity_level == "medium":
            # 中程度の要約：バランスの取れた文数
            similarity_limit = 0.3
            target_sentences = min(max_sentences, max(
                min_sentences, int(len(document.split("。")) * 0.25)))
        else:  # coarse
            # 粗い要約：少ない文数で要点のみ
            similarity_limit = 0.2
            target_sentences = min(max_sentences, max(
                min_sentences, int(len(document.split("。")) * 0.15)))

        # 類似性フィルターの設定
        self.similarity_filter.similarity_limit = similarity_limit

        # 要約実行
        abstractable_doc = TopNRankAbstractor()
        abstractable_doc.limit = target_sentences

        # 類似性フィルター付きで要約
        result_dict = self.auto_abstractor.summarize(
            document, abstractable_doc, self.similarity_filter)

        return result_dict, target_sentences

    def post_process_summary(self, summary_sentences, original_document):
        """
        要約結果の後処理：文の順序調整と接続詞の追加
        """
        if not summary_sentences:
            return summary_sentences

        # 空の文や短すぎる文をフィルタリング
        filtered_sentences = []
        for sent in summary_sentences:
            sent = sent.strip()
            if sent and len(sent) > 5:  # 5文字以上の文のみ
                filtered_sentences.append(sent)

        if not filtered_sentences:
            return summary_sentences

        # 元文書での文の順序を保持
        original_sentences = original_document.split("。")
        ordered_summary = []

        for orig_sent in original_sentences:
            orig_sent = orig_sent.strip()
            if orig_sent and any(orig_sent in sent for sent in filtered_sentences):
                # 元文書の順序で要約文を並べ替え
                for sent in filtered_sentences:
                    if orig_sent in sent or sent in orig_sent:
                        ordered_summary.append(sent)
                        break

        # 順序が保持できない場合は元の順序を使用
        if len(ordered_summary) != len(filtered_sentences):
            ordered_summary = filtered_sentences

        # 接続詞の追加で文の流れを改善
        improved_summary = []
        for i, sent in enumerate(ordered_summary):
            if i == 0:
                improved_summary.append(sent)
            else:
                # 前の文との関連性を考慮して接続詞を追加
                if "しかし" in sent or "だが" in sent or "一方" in sent:
                    improved_summary.append(sent)
                else:
                    improved_summary.append(f"また、{sent}")

        return improved_summary


def main():
    parser = argparse.ArgumentParser(description='日本語テキスト要約システム')
    parser.add_argument('--input', '-i', default='./test/インプット.txt',
                        help='入力ファイルのパス')
    parser.add_argument('--output', '-o', default='',
                        help='出力ファイルのパス（指定しない場合は自動生成）')
    parser.add_argument('--granularity', '-g', choices=['fine', 'medium', 'coarse'], default='medium',
                        help='要約の粒度レベル (fine: 詳細, medium: 中程度, coarse: 粗い)')
    parser.add_argument('--similarity_limit', '-s', type=float, default=0.3,
                        help='類似性フィルターの閾値 (0.1-0.5)')
    parser.add_argument('--min_sentences', type=int, default=3,
                        help='最小文数')
    parser.add_argument('--max_sentences', type=int, default=20,
                        help='最大文数')

    args = parser.parse_args()

    # ファイルの読み込み
    if not os.path.exists(args.input):
        print(f"エラー: 入力ファイル '{args.input}' が見つかりません。")
        return

    try:
        with open(args.input, encoding='utf-8') as f:
            contents = f.readlines()
        document = ''.join(contents)

        print(f"入力ファイル: {args.input}")
        print(f"テキスト長: {len(document)} 文字")
        print(f"粒度レベル: {args.granularity}")
        print(f"類似性閾値: {args.similarity_limit}")
        print("要約処理中...")

        # 要約実行
        summarizer = ImprovedSummarizer()
        result_dict, target_sentences = summarizer.summarize_with_granularity(
            document,
            args.granularity,
            args.similarity_limit,
            args.min_sentences,
            args.max_sentences
        )

        # 後処理
        summary_sentences = result_dict["summarize_result"]
        improved_summary = summarizer.post_process_summary(
            summary_sentences, document)

        # 出力ファイル名の自動生成（実行時間を含む）
        if not args.output:
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            input_filename = os.path.splitext(os.path.basename(args.input))[0]
            output_filename = f"要約結果_{input_filename}_{args.granularity}_{current_time}.txt"
            output_path = output_filename  # 実行ディレクトリの直下
        else:
            output_path = args.output

        # 結果出力
        output_content = f"""=== 要約結果 ===
粒度レベル: {args.granularity}
目標文数: {target_sentences}
実際の文数: {len(improved_summary)}
類似性閾値: {args.similarity_limit}
実行時刻: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

【要約】
{chr(10).join(improved_summary)}

【元文書の文数】: {len(document.split('。'))}
【要約率】: {len(improved_summary) / len(document.split('。')) * 100:.1f}%
"""

        with open(output_path, mode='w', encoding='utf-8') as f:
            f.write(output_content)

        print(f"要約完了！出力ファイル: {output_path}")
        print(f"要約文数: {len(improved_summary)} / {len(document.split('。'))}")
        print(
            f"要約率: {len(improved_summary) / len(document.split('。')) * 100:.1f}%")

    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    main()
