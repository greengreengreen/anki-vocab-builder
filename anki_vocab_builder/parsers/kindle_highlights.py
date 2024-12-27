from pathlib import Path
from typing import List, Tuple
from datetime import datetime


def parse_date(date_str: str) -> str:
    """Parse date string from Kindle format to YYYY-MM-DD"""
    try:
        date = datetime.strptime(date_str, "%A, %B %d, %Y %I:%M:%S %p")
        return date.strftime("%Y-%m-%d")
    except ValueError:
        return ""


def parse_kindle_clippings(file_path: Path) -> List[Tuple[str, str, str]]:
    """
    Parse Kindle My Clippings.txt file and extract highlights with their sources and dates.
    
    Args:
        file_path: Path to My Clippings.txt file
        
    Returns:
        List of tuples containing (highlight_text, source, date)
        where:
        - source is in format "Book Title (Author Name)"
        - date is in format "YYYY-MM-DD"
    """
    highlights = []
    
    try:
        content = file_path.read_text(encoding='utf-8-sig')
        sections = content.split("==========")
        
        for section in sections:
            if not section.strip():
                continue
                
            lines = [line.strip() for line in section.split('\n') if line.strip()]
            if len(lines) < 3:  # Need at least title, metadata, and highlight
                continue
                
            # Parse source (title and author)
            source = lines[0].strip()
            
            # Parse date from metadata line
            metadata_line = lines[1]
            if "Added on" in metadata_line:
                date_part = metadata_line.split("Added on")[-1].strip()
                date = parse_date(date_part)
            else:
                date = ""
            
            # Get highlight text (everything after metadata line)
            highlight = lines[2]
            
            highlights.append((highlight, source, date))
    
    except Exception as e:
        print(f"Error parsing Kindle clippings: {str(e)}")
        return []
        
    return highlights


def format_highlight(highlight: str, source: str, date: str) -> str:
    """
    Format a highlight for display or processing.
    """
    return f"Highlight ({date}):\n{highlight}\nSource: {source}"


if __name__ == "__main__":
    highlights = parse_kindle_clippings(Path(".anki_vocab_builder/input/kindle/My Clippings.txt"))
    for highlight, source, date in highlights:
        print(f"Date: {date}")
        print(f"Source: {source}")
        print(f"Highlight: {highlight}")
        print("---")
