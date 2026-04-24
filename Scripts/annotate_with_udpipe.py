#!/usr/bin/env python3
"""
Script to annotate Portuguese legal text files with UDPipe
Processes all modificacao_*.txt files and outputs CoNLL-U format
"""

import glob
import os
from ufal.udpipe import Model, Pipeline

def process_files_with_udpipe(model_path, input_pattern, output_dir="annotated_output"):
    """
    Process text files with UDPipe and save annotated output

    Args:
        model_path: Path to the UDPipe model file
        input_pattern: Glob pattern for input files (e.g., "modificacao_*.txt")
        output_dir: Directory to save annotated files
    """

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load the UDPipe model
    print(f"Loading model: {model_path}")
    model = Model.load(model_path)
    if not model:
        print(f"Error: Cannot load model from {model_path}")
        return

    # Create pipeline for tokenization, tagging, and parsing
    pipeline = Pipeline(model, "tokenize", Pipeline.DEFAULT, Pipeline.DEFAULT, "conllu")

    # Get all files matching the pattern
    input_files = sorted(glob.glob(input_pattern))
    print(f"Found {len(input_files)} files to process")

    # Process each file
    for input_file in input_files:
        filename = os.path.basename(input_file)
        output_file = os.path.join(output_dir, filename.replace(".txt", ".conllu"))

        print(f"Processing: {filename}")

        # Read input text
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"  Error reading {filename}: {e}")
            continue

        # Skip empty files
        if not text.strip():
            print(f"  Skipping empty file: {filename}")
            continue

        # Process with UDPipe
        annotated = pipeline.process(text)

        # Save output
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(annotated)
            print(f"  Saved: {output_file}")
        except Exception as e:
            print(f"  Error writing {output_file}: {e}")

    print(f"\nAnnotation complete! Files saved in '{output_dir}/' directory")
    print(f"\nCoNLL-U format includes:")
    print("  - Token ID, Form, Lemma")
    print("  - Universal POS tags (UPOS)")
    print("  - Language-specific POS tags (XPOS)")
    print("  - Morphological features")
    print("  - Dependency relations (HEAD, DEPREL)")

if __name__ == "__main__":
    # Configuration
    BASE_DIR = "/Users/lucianadiasdemacedo/LEX-BR-Ius_extracao_data"
    MODEL_PATH = os.path.join(BASE_DIR, "portuguese-bosque-ud.udpipe")
    INPUT_PATTERN = os.path.join(BASE_DIR, "modificacao_*.txt")
    OUTPUT_DIR = os.path.join(BASE_DIR, "annotated_output")

    # Run the annotation
    process_files_with_udpipe(MODEL_PATH, INPUT_PATTERN, OUTPUT_DIR)
