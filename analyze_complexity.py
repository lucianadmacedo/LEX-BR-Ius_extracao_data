#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Temporal Analysis of Grammatical Complexity in Brazilian Legal Texts
Analyzes CoNLL-U annotated files for complexity features across time,
including type/token ratio (TTR) by year.
"""

import os
import re
from collections import defaultdict
import json


class ComplexityAnalyzer:
    """Analyzes grammatical complexity features in CoNLL-U files"""

    def __init__(self, conllu_dir):
        self.conllu_dir = conllu_dir
        self.results_by_year = defaultdict(lambda: {
            'file_count': 0,
            'sentence_count': 0,
            'token_count': 0,
            'features': defaultdict(int),
            'vocab': set(),          # <<< NEW: set of lemma types per year
        })

    def parse_conllu_file(self, filepath):
        """Parse a CoNLL-U file and extract sentences"""
        sentences = []
        current_sentence = []
        sentence_text = ""

        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                if line.startswith('# text = '):
                    sentence_text = line.replace('# text = ', '')
                elif line.startswith('#'):
                    continue
                elif line == '':
                    if current_sentence:
                        sentences.append({
                            'text': sentence_text,
                            'tokens': current_sentence
                        })
                        current_sentence = []
                        sentence_text = ""
                else:
                    # Parse CoNLL-U line
                    parts = line.split('\t')
                    if len(parts) >= 10:
                        token_id = parts[0]
                        # Skip multiword tokens (e.g., "6-7")
                        if '-' in token_id:
                            continue

                        token = {
                            'id': token_id,
                            'form': parts[1],
                            'lemma': parts[2],
                            'upos': parts[3],
                            'xpos': parts[4],
                            'feats': parts[5],
                            'head': parts[6],
                            'deprel': parts[7],
                            'deps': parts[8],
                            'misc': parts[9]
                        }
                        current_sentence.append(token)

        return sentences

    # ---------- Feature analyzers ----------

    def analyze_word_order(self, sentence):
        """Detect non-canonical word order (VS instead of SV)"""
        complexity = 0

        # Find subject-verb pairs
        for token in sentence['tokens']:
            if token['deprel'] in ['nsubj', 'nsubj:pass', 'csubj']:
                subject_pos = int(token['id'])
                verb_pos = int(token['head'])

                # VS order (verb before subject) = complexity
                if verb_pos < subject_pos:
                    complexity += 1

        return complexity

    def analyze_nominalization(self, sentence):
        """Detect nominalizations (deverbal nouns)"""
        complexity = 0

        # Common nominalization suffixes in Portuguese
        nom_patterns = [
            r'ção$', r'mento$', r'ncia$', r'dade$', r'eza$',
            r'ismo$', r'agem$', r'ura$', r'ância$'
        ]

        for token in sentence['tokens']:
            if token['upos'] == 'NOUN':
                lemma = token['lemma'].lower()
                for pattern in nom_patterns:
                    if re.search(pattern, lemma):
                        complexity += 1
                        break

        return complexity

    def analyze_subordination(self, sentence):
        """Count subordinate clauses (relative, complement, etc.)"""
        complexity = 0

        subordinate_rels = [
            'acl', 'acl:relcl', 'advcl', 'ccomp', 'xcomp',
            'csubj', 'csubj:pass'
        ]

        for token in sentence['tokens']:
            if any(rel in token['deprel'] for rel in subordinate_rels):
                complexity += 1

        return complexity

    def analyze_passive(self, sentence):
        """Detect passive constructions"""
        complexity = 0

        for token in sentence['tokens']:
            # Analytic passive: nsubj:pass
            if token['deprel'] == 'nsubj:pass':
                complexity += 1

            # Synthetic passive with -se
            if token['form'].lower() == 'se' and token['deprel'] == 'expl:pass':
                complexity += 1

        return complexity

    def analyze_gerunds_participles(self, sentence):
        """Count gerunds and participles"""
        complexity = 0

        for token in sentence['tokens']:
            if token['upos'] == 'VERB':
                feats = token['feats']
                if 'VerbForm=Ger' in feats:
                    complexity += 1
                elif 'VerbForm=Part' in feats:
                    complexity += 1

        return complexity

    def analyze_relative_pronouns(self, sentence):
        """Count relative pronouns and subordinating conjunctions"""
        complexity = 0

        relative_words = [
            'que', 'qual', 'quais', 'onde', 'quando', 'quanto',
            'cujo', 'cuja', 'cujos', 'cujas', 'o qual', 'a qual'
        ]

        subord_conjunctions = [
            'porquanto', 'conquanto', 'embora', 'posto que',
            'visto que', 'haja vista', 'sendo que', 'caso',
            'enquanto', 'conforme', 'consoante'
        ]

        for token in sentence['tokens']:
            form_lower = token['lemma'].lower()

            # Relative pronouns
            if token['upos'] == 'PRON' and token['deprel'] in ['nsubj', 'obj', 'obl']:
                if form_lower in relative_words:
                    complexity += 1

            # Subordinating conjunctions
            if token['upos'] == 'SCONJ' or form_lower in subord_conjunctions:
                complexity += 1

        return complexity

    def analyze_appositions(self, sentence):
        """Count appositions and parentheticals"""
        complexity = 0

        for token in sentence['tokens']:
            if token['deprel'] in ['appos', 'parataxis']:
                complexity += 1

        return complexity

    def analyze_prepositional_density(self, sentence):
        """Count prepositional phrases (lexical density marker)"""
        complexity = 0

        for token in sentence['tokens']:
            if token['upos'] == 'ADP':
                complexity += 1

        return complexity

    def analyze_complex_verb_forms(self, sentence):
        """Count subjunctive, future, conditional forms"""
        complexity = 0

        for token in sentence['tokens']:
            if token['upos'] in ['VERB', 'AUX']:
                feats = token['feats']

                # Subjunctive moods
                if 'Mood=Sub' in feats:
                    complexity += 1
                # Conditional
                elif 'Mood=Cnd' in feats:
                    complexity += 1
                # Future tense (often complex in legal text)
                elif 'Tense=Fut' in feats:
                    complexity += 0.5

        return int(complexity)

    def analyze_sentence_length(self, sentence):
        """Return sentence length in tokens"""
        return len(sentence['tokens'])

    def analyze_subordination_depth(self, sentence):
        """Calculate maximum depth of subordination"""
        depths = {}

        for token in sentence['tokens']:
            token_id = int(token['id'])
            head_id = int(token['head'])

            if head_id == 0:
                depths[token_id] = 1
            else:
                depths[token_id] = None

        changed = True
        max_iterations = 50
        iteration = 0

        while changed and iteration < max_iterations:
            changed = False
            iteration += 1

            for token in sentence['tokens']:
                token_id = int(token['id'])
                head_id = int(token['head'])

                if depths[token_id] is None:
                    if head_id == 0:
                        depths[token_id] = 1
                        changed = True
                    elif head_id in depths and depths[head_id] is not None:
                        depths[token_id] = depths[head_id] + 1
                        changed = True

        return max(depths.values()) if depths else 0

    # ---------- File-level analysis ----------

    def analyze_file(self, filepath, year):
        """Analyze a single file and aggregate results by year"""
        sentences = self.parse_conllu_file(filepath)

        if not sentences:
            return

        year_data = self.results_by_year[year]
        year_data['file_count'] += 1
        year_data['sentence_count'] += len(sentences)

        for sentence in sentences:
            # Count tokens
            year_data['token_count'] += len(sentence['tokens'])

            # <<< NEW: update vocabulary (types) using lemmas
            for tok in sentence['tokens']:
                lemma = tok['lemma'].lower()
                if lemma:
                    year_data['vocab'].add(lemma)

            # Analyze each complexity feature
            year_data['features']['word_order_inversion'] += self.analyze_word_order(sentence)
            year_data['features']['nominalization'] += self.analyze_nominalization(sentence)
            year_data['features']['subordination'] += self.analyze_subordination(sentence)
            year_data['features']['passive'] += self.analyze_passive(sentence)
            year_data['features']['gerunds_participles'] += self.analyze_gerunds_participles(sentence)
            year_data['features']['relative_pronouns'] += self.analyze_relative_pronouns(sentence)
            year_data['features']['appositions'] += self.analyze_appositions(sentence)
            year_data['features']['prepositional_phrases'] += self.analyze_prepositional_density(sentence)
            year_data['features']['complex_verb_forms'] += self.analyze_complex_verb_forms(sentence)

            # Sentence-level metrics
            sent_len = self.analyze_sentence_length(sentence)
            year_data['features']['total_sentence_length'] += sent_len
            year_data['features']['max_sentence_length'] = max(
                year_data['features']['max_sentence_length'],
                sent_len
            )

            sub_depth = self.analyze_subordination_depth(sentence)
            year_data['features']['total_subordination_depth'] += sub_depth
            year_data['features']['max_subordination_depth'] = max(
                year_data['features']['max_subordination_depth'],
                sub_depth
            )

    def analyze_all_files(self):
        """Process all CoNLL-U files in the directory"""
        files = [f for f in os.listdir(self.conllu_dir) if f.endswith('.conllu')]

        print(f"Found {len(files)} CoNLL-U files")
        print("Processing files...")

        for filename in sorted(files):
            # Extract year from filename (modificacao_YYYY.conllu)
            match = re.search(r'modificacao_(\d{4})\.conllu', filename)
            if match:
                year = int(match.group(1))
                filepath = os.path.join(self.conllu_dir, filename)

                print(f"  Processing {filename} (year {year})...")
                self.analyze_file(filepath, year)

        print("\nAnalysis complete!")

    # ---------- Normalization & output ----------

    def calculate_normalized_metrics(self):
        """Calculate per-sentence, per-token, and TTR metrics"""
        normalized = {}

        for year, data in sorted(self.results_by_year.items()):
            sent_count = data['sentence_count']
            token_count = data['token_count']

            if sent_count == 0 or token_count == 0:
                continue

            type_count = len(data['vocab'])        # <<< NEW
            ttr = type_count / token_count if token_count > 0 else 0.0  # <<< NEW

            normalized[year] = {
                'files': data['file_count'],
                'sentences': sent_count,
                'tokens': token_count,
                'types': type_count,              # <<< NEW: number of types
                'type_token_ratio': ttr,          # <<< NEW: TTR
                'avg_sentence_length': token_count / sent_count,
                'avg_subordination_depth': data['features']['total_subordination_depth'] / sent_count,
                'max_subordination_depth': data['features']['max_subordination_depth'],
                'max_sentence_length': data['features']['max_sentence_length'],

                # Per sentence metrics
                'per_sentence': {
                    'word_order_inversion': data['features']['word_order_inversion'] / sent_count,
                    'nominalization': data['features']['nominalization'] / sent_count,
                    'subordination': data['features']['subordination'] / sent_count,
                    'passive': data['features']['passive'] / sent_count,
                    'gerunds_participles': data['features']['gerunds_participles'] / sent_count,
                    'relative_pronouns': data['features']['relative_pronouns'] / sent_count,
                    'appositions': data['features']['appositions'] / sent_count,
                    'prepositional_phrases': data['features']['prepositional_phrases'] / sent_count,
                    'complex_verb_forms': data['features']['complex_verb_forms'] / sent_count,
                },

                # Per 100 tokens metrics
                'per_100_tokens': {
                    'word_order_inversion': (data['features']['word_order_inversion'] / token_count) * 100,
                    'nominalization': (data['features']['nominalization'] / token_count) * 100,
                    'subordination': (data['features']['subordination'] / token_count) * 100,
                    'passive': (data['features']['passive'] / token_count) * 100,
                    'gerunds_participles': (data['features']['gerunds_participles'] / token_count) * 100,
                    'relative_pronouns': (data['features']['relative_pronouns'] / token_count) * 100,
                    'appositions': (data['features']['appositions'] / token_count) * 100,
                    'prepositional_phrases': (data['features']['prepositional_phrases'] / token_count) * 100,
                    'complex_verb_forms': (data['features']['complex_verb_forms'] / token_count) * 100,
                }
            }

        return normalized

    def generate_report(self, output_file='complexity_analysis_report.txt'):
        """Generate a detailed text report"""
        normalized = self.calculate_normalized_metrics()

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("TEMPORAL ANALYSIS OF GRAMMATICAL COMPLEXITY\n")
            f.write("Brazilian Legal Texts\n")
            f.write("=" * 80 + "\n\n")

            # Overall statistics
            f.write("OVERALL STATISTICS BY YEAR\n")
            f.write("-" * 80 + "\n")
            f.write(f"{'Year':<8} {'Files':<8} {'Sentences':<12} {'Tokens':<12} "
                    f"{'Types':<12} {'TTR':<10} {'Avg Sent Len':<15}\n")
            f.write("-" * 80 + "\n")

            for year in sorted(normalized.keys()):
                data = normalized[year]
                f.write(
                    f"{year:<8} {data['files']:<8} {data['sentences']:<12} {data['tokens']:<12} "
                    f"{data['types']:<12} {data['type_token_ratio']:<10.3f} "
                    f"{data['avg_sentence_length']:<15.2f}\n"
                )

            f.write("\n" + "=" * 80 + "\n\n")

            # Complexity features per sentence
            f.write("COMPLEXITY FEATURES (PER SENTENCE)\n")
            f.write("-" * 80 + "\n")

            features = [
                ('word_order_inversion', 'Word Order Inversion (VS)'),
                ('nominalization', 'Nominalizations'),
                ('subordination', 'Subordinate Clauses'),
                ('passive', 'Passive Constructions'),
                ('gerunds_participles', 'Gerunds & Participles'),
                ('relative_pronouns', 'Relative Pronouns & Conjunctions'),
                ('appositions', 'Appositions & Parentheticals'),
                ('prepositional_phrases', 'Prepositional Phrases'),
                ('complex_verb_forms', 'Complex Verb Forms'),
            ]

            for feature_key, feature_name in features:
                f.write(f"\n{feature_name}:\n")
                f.write(f"{'Year':<8} {'Per Sentence':<15} {'Per 100 Tokens':<15}\n")
                f.write("-" * 40 + "\n")

                for year in sorted(normalized.keys()):
                    per_sent = normalized[year]['per_sentence'][feature_key]
                    per_100 = normalized[year]['per_100_tokens'][feature_key]
                    f.write(f"{year:<8} {per_sent:<15.3f} {per_100:<15.3f}\n")

            f.write("\n" + "=" * 80 + "\n\n")

            # Subordination depth analysis
            f.write("SUBORDINATION DEPTH ANALYSIS\n")
            f.write("-" * 80 + "\n")
            f.write(f"{'Year':<8} {'Avg Depth':<15} {'Max Depth':<15}\n")
            f.write("-" * 40 + "\n")

            for year in sorted(normalized.keys()):
                avg_depth = normalized[year]['avg_subordination_depth']
                max_depth = normalized[year]['max_subordination_depth']
                f.write(f"{year:<8} {avg_depth:<15.2f} {max_depth:<15}\n")

        print(f"\nReport written to: {output_file}")

    def save_json_data(self, output_file='complexity_analysis_data.json'):
        """Save normalized data as JSON for further analysis"""
        normalized = self.calculate_normalized_metrics()

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(normalized, f, indent=2, ensure_ascii=False)

        print(f"JSON data written to: {output_file}")


if __name__ == '__main__':
    # Directory containing annotated CoNLL-U files
    conllu_directory = '/Users/lucianadiasdemacedo/LEX-BR-Ius_extracao_data/annotated_output'

    # Create analyzer
    analyzer = ComplexityAnalyzer(conllu_directory)

    # Run analysis
    analyzer.analyze_all_files()

    # Generate outputs
    analyzer.generate_report('complexity_analysis_report.txt')
    analyzer.save_json_data('complexity_analysis_data.json')

    print("\n✓ Analysis complete! Check the output files.")