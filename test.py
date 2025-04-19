import sys
import json
import time
from pathlib import Path
from datetime import datetime

print("🚀 Starting test.py")
sys.stdout.flush()

try:
    from scholarly import scholarly
    print("✅ scholarly imported")
    sys.stdout.flush()

    print("🧠 Python environment is working")
    sys.stdout.flush()
except Exception as e:
    print(f"❌ Import or execution error: {e}")
    sys.stdout.flush()


def get_publications(author_id):
    try:
        print("Starting pub. search")
        # Search for the author and retrieve their publications
        author = scholarly.search_author_id(author_id)
        author_filled = scholarly.fill(author, sections=['publications'])
        print("Counts section:", json.dumps(author_filled.get("cites_per_year", {})))
        # Debug: Print partial author data
        print("Full author data:", json.dumps(author_filled, indent=2)[:500] + "...")
        return author_filled.get("publications", [])
    except Exception as e:
        print(f"Error fetching publications: {str(e)}")
        return []

def get_current_year_publications(publications):
    pub_data = []
    current_year = datetime.now().year
    
    # Filter and process ALL current year publications
    for pub in publications:
        try:
            # Skip if not current year
            pub_year = int(pub.get("bib", {}).get("pub_year", "0"))
            if pub_year != current_year:
                continue
                
            time.sleep(1)  # Maintain rate limiting
            filled_pub = scholarly.fill(pub)
            bib = filled_pub.get("bib", {})
            
            # Original author processing
            authors = bib.get("author", "N/A")
            if isinstance(authors, list):
                authors = ", ".join(authors)

            # Original venue priority chain
            venue = bib.get("venue") or \
                   bib.get("journal") or \
                   bib.get("conference") or \
                   bib.get("booktitle") or \
                   bib.get("source", "N/A")

            # Original output structure
            pub_data.append({
                "title": bib.get("title", "N/A"),
                "authors": authors,
                "publication_year": current_year,
                "citations": filled_pub.get("num_citations", 0),
                "venue": venue,
                "source_link": filled_pub.get("pub_url", ""),
                "doi": filled_pub.get("pub_url", "")
            })
            
        except Exception as e:
            print(f"Skipping publication: {e}")
            continue
            
    return pub_data

def save_to_json(data, filename):
    data_dir = Path(__file__).parent
    data_dir.mkdir(exist_ok=True)
    with open(data_dir / filename, "w") as f:
        json.dump(data, f, indent=2)

def main():
    author_id = "cyQLH48AAAAJ"
    
    publications = get_publications(author_id)
    pub_data = get_current_year_publications(publications)
    save_to_json(pub_data, "publications.json")
    print(f"✅ Retrieved {len(pub_data)} publications")

if __name__ == "__main__":
    main()
