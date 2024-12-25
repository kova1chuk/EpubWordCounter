import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from collections import Counter
import re

def extract_text_from_epub(epub_path: str) -> str:
    """
    Extracts all text from an EPUB file.
    """
    book = epub.read_epub(epub_path)
    text = ''
    
    for item in book.items:
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            content = item.get_content()
            soup = BeautifulSoup(content, 'html.parser')
            text += soup.get_text(separator=' ')
    
    return text

def count_word_frequency(text: str) -> list[tuple[str, int]]:
    """
    Counts word frequencies in the given text and returns them sorted.
    """
    # Remove non-alphabetic characters and normalize to lowercase
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    word_counts = Counter(words)
    # Sort by frequency (descending) and then alphabetically (ascending)
    sorted_words = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))
    return sorted_words

def save_word_frequencies_to_txt(word_frequencies: list[tuple[str, int]], output_path: str):
    """
    Saves word frequencies to a TXT file.
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        for word, freq in word_frequencies:
            file.write(f"{word}: {freq}\n")

def process_epub(epub_path: str, output_path: str):
    """
    Processes an EPUB file, saves sorted word frequencies to a TXT file.
    """
    text = extract_text_from_epub(epub_path)
    word_frequencies = count_word_frequency(text)
    save_word_frequencies_to_txt(word_frequencies, output_path)
    print(f"Word frequencies saved to {output_path}")

# Example usage
if __name__ == "__main__":
    epub_path = 'book.epub'  # Replace with your EPUB file path
    output_path = 'word_frequencies.txt'  # Output file
    process_epub(epub_path, output_path)