"""
Nancy Guan
DS3500
Homework 7: Natural Language Processing
5 December 2025
parse_pal.py
"""
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
from words import EMOTION_KEYWORDS, CERTAINTY_KEYWORDS
from parse_pal_parsers import default_parser, propaganda_parser

class ParsePal:
    def __init__(self):
        """ Constructor to initialize state """
        self.data = defaultdict(dict)
        self.stop_words = set()
        self.data = {
            'raw_text': {},
            'word_count': {},
            'wordcount': {},
            'numwords': {},
            'avg_word_length': {},
            'lexical_diversity': {},
            'avg_sentence_length': {}
        }

    def load_stop_words(self, stop_file):
        """ Load a list of common/stop words to filter from each file """
        with open(stop_file, 'r', encoding='utf-8') as f:
            self.stop_words = set(word.strip().lower() for word in f)

    def load_text(self, filename, label=None, parser=None):
        """ Register a text document with the framework """
        if parser is None:
            results = default_parser(filename)
        else:
            results = parser(filename)
        if label is None:
            label = filename

        if self.stop_words and 'wordcount' in results:
            filtered_count = Counter({
                word: count for word, count in results['wordcount'].items()
                if word not in self.stop_words and len(word) > 2
            })
            results['wordcount_filtered'] = filtered_count
        else:
            results['wordcount_filtered'] = Counter({
                word: count for word, count in results['wordcount'].items()
                if len(word) > 2
            })

        for k, v in results.items():
            if k not in self.data:
                self.data[k] = {}
            self.data[k][label] = v

    def wordcount_sankey(self, word_list=None, k=5):
        """ Make a sankey diagram showing k most common words """
        wordcount_key = 'wordcount_filtered' if 'wordcount_filtered' in self.data else 'wordcount'
        wordcounts = self.data[wordcount_key]

        if word_list is None:
            all_words = Counter()
            for label, wc in wordcounts.items():
                top_words = [word for word, count in wc.most_common(k)]
                all_words.update(top_words)
            word_list = [word for word, _ in all_words.most_common(k * 2)][:10]

        sources = []
        targets = []
        values = []
        labels_list = list(wordcounts.keys())
        node_labels = labels_list + word_list

        for i, (doc_label, wc) in enumerate(wordcounts.items()):
            for word in word_list:
                count = wc.get(word, 0)
                if count > 0:
                    sources.append(i)
                    targets.append(len(labels_list) + word_list.index(word))
                    values.append(count)

        fig = go.Figure(data=[go.Sankey(node=dict(pad=15, thickness=20, line=dict
        (color="black", width=0.5), label=node_labels), link=dict(source=sources, target=targets,
        value=values))])
        fig.update_layout(title_text="Most Frequent Words", font_size=10)
        fig.show()

    def subplot(self, num_segments=10):
        """ Stacked bar chart showing emotional composition across text segments """
        num_texts = len(self.data['raw_text'])
        cols = 2
        rows = (num_texts + cols - 1) // cols

        fig, axes = plt.subplots(rows, cols, figsize=(10, 3.5 * rows))
        axes = axes.flatten() if num_texts > 1 else [axes]
        # fear, anger, hope, pride
        colors = ['#005EE0', '#E00000', '#F2D900', '#04E000']

        for idx, (label, text) in enumerate(self.data['raw_text'].items()):
            ax = axes[idx]
            words = [w.lower() for w in text.split()]
            segment_size = len(words) // num_segments
            if segment_size < 10:
                ax.text(0.5, 0.5, 'Text too short',
                        ha='center', va='center', transform=ax.transAxes)
                ax.set_title(f'{label}', fontsize=10)
                ax.axis('off')
                continue

            segment_data = {emotion: [] for emotion in EMOTION_KEYWORDS.keys()}

            for seg in range(num_segments):
                start = seg * segment_size
                end = start + segment_size if seg < num_segments - 1 else len(words)
                segment_words = words[start:end]

                for emotion, keywords in EMOTION_KEYWORDS.items():
                    count = sum(1 for word in segment_words if word in keywords)
                    score = count / len(segment_words) * 100 if segment_words else 0
                    segment_data[emotion].append(score)

            x = np.arange(num_segments)
            bottom = np.zeros(num_segments)

            for emotion_idx, (emotion, scores) in enumerate(segment_data.items()):
                ax.bar(x, scores, bottom=bottom, label=emotion, color=colors[emotion_idx],
                       alpha=0.8, edgecolor='white', linewidth=0.5)
                bottom += np.array(scores)

            ax.set_title(f'{label}', fontsize=10, fontweight='bold')
            ax.set_ylabel('Intensity (%)', fontsize=9)
            x_labels = [f'{int(i / num_segments * 100)}-{int((i + 1) / num_segments * 100)}%'
                        for i in range(num_segments)]
            ax.set_xticks(x)
            ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=7)
            ax.legend(loc='upper left', fontsize=7)
            ax.grid(axis='y', alpha=0.3)

        for idx in range(num_texts, len(axes)):
            axes[idx].axis('off')

        plt.suptitle('Emotional Appeal Progression',
                     fontsize=13, fontweight='bold')
        plt.tight_layout()
        plt.show()

    def comparative_overlay(self):
        """ Bubble chart: X = Emotional intensity, Y = Certainty, Size = Word count, Color = Diversity"""
        labels = list(self.data['word_count'].keys())
        emotional_intensity = []
        certainty_scores = []
        word_counts = []
        diversities = []
        certainty_words = CERTAINTY_KEYWORDS

        for label in labels:
            word_count_dict = self.data['word_count'][label]
            total_words = sum(word_count_dict.values())

            # Emotional intensity
            emotion_total = 0
            for emotion, keywords in EMOTION_KEYWORDS.items():
                emotion_total += sum(word_count_dict.get(word, 0) for word in keywords)
            emot_score = (emotion_total / total_words * 1000) if total_words > 0 else 0
            emotional_intensity.append(emot_score)

            # Certainty
            cert_count = sum(word_count_dict.get(word, 0) for word in certainty_words)
            cert_score = (cert_count / total_words * 1000) if total_words > 0 else 0
            certainty_scores.append(cert_score)

            # Word count and diversity
            word_counts.append(total_words)
            diversities.append(self.data['lexical_diversity'][label])

        fig, ax = plt.subplots(figsize=(12, 9))
        sizes = np.array(word_counts) / max(word_counts) * 1500 + 200

        scatter = ax.scatter(emotional_intensity, certainty_scores, s=sizes, c=diversities,
                             cmap='viridis', alpha=0.6, edgecolors='black', linewidth=2)

        for i, label in enumerate(labels):
            ax.annotate(label, (emotional_intensity[i], certainty_scores[i]),
                        xytext=(8, 8), textcoords='offset points', fontsize=10, fontweight='bold',
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.85, edgecolor='black',
                                  linewidth=1.5), arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2',
                                 color='gray', lw=1.5))

        ax.axvline(x=np.median(emotional_intensity), color='gray',
                   linestyle='--', alpha=0.5, linewidth=2)
        ax.axhline(y=np.median(certainty_scores), color='gray',
                   linestyle='--', alpha=0.5, linewidth=2)
        ax.text(0.02, 0.98, 'Emotional\nUncertain', transform=ax.transAxes,
                fontsize=10, style='italic', verticalalignment='top', color='gray', fontweight='bold')
        ax.text(0.98, 0.98, 'Emotional\nAbsolute\n(Aggressive)', transform=ax.transAxes,
                fontsize=10, style='italic', verticalalignment='top', horizontalalignment='right',
                color='darkred', fontweight='bold')
        ax.text(0.02, 0.02, 'Measured\nUncertain', transform=ax.transAxes, fontsize=10,
                style='italic', verticalalignment='bottom', color='gray', fontweight='bold')
        ax.text(0.98, 0.02, 'Rational\nAbsolute', transform=ax.transAxes, fontsize=10,
                style='italic', verticalalignment='bottom', horizontalalignment='right',
                color='gray', fontweight='bold')

        cbar = plt.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Lexical Diversity', fontsize=12, fontweight='bold')
        ax.set_xlabel('Emotional Intensity (per 1000 words)', fontsize=13, fontweight='bold')
        ax.set_ylabel('Certainty Language (per 1000 words)', fontsize=13, fontweight='bold')
        ax.set_title('Propaganda Aggression Map', fontsize=15, fontweight='bold', pad=20)
        ax.grid(alpha=0.3)

        legend_sizes = [200, 600, 1200]
        legend_labels = ['Short', 'Medium', 'Long']
        legend_elements = [plt.scatter([], [], s=s, c='gray', alpha=0.6, edgecolors='black', linewidth=2)
                           for s in legend_sizes]
        legend1 = ax.legend(legend_elements, legend_labels, title='Document\nLength', loc='upper left',
                            fontsize=9, title_fontsize=10, framealpha=0.9)
        ax.add_artist(legend1)
        plt.tight_layout()
        plt.show()