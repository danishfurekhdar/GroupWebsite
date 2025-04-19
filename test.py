import sys
import json
import time
from pathlib import Path
from datetime import datetime
import concurrent.futures

print("🚀 Starting test.py")
sys.stdout.flush()

try:
    from scholarly import scholarly
    print("✅ scholarly imported")
    sys.stdout.flush()
except Exception as e:
    print(f"❌ Import or execution error: {e}")
    sys.stdout.flush()
    sys.exit(1)


def safe_fill(pub, timeout_sec=15):
    """Safely fill a publication or author object with timeout."""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(scholarly.fill, pub)
        try:
            return future.result(timeout=timeout_sec)
        except concurrent.futures.TimeoutError:
            print("⚠️ scholarly.fill() timed out")
            sys.stdout.flush()
            return {}
        except Exception as e:
            print(f"⚠️ scholarly.fill() failed: {e}")
            sys.stdout.flush()
            return {}

def get_publications(author_id):
    try:
        print("📚 Starting pub. search")
        sys.stdout.flush()
        author = scholarly.search_author_id(author_id)
        author_filled = safe_fill(author, timeout_sec=30)

        print("📈 Counts section:", json.dumps(author_filled.get("cites_per_year", {})))
        sys.stdout.flush()
        print("📝 Author data (partial):", json.dumps(author_filled, indent=2)[:500] + "...")
        sys.stdout.flush()

        return author_filled.get("publications", [])
    except Exception as e:
        print(f"❌ Error fetching publications: {str(e)}")
        sys.stdout.flush()
        return []

def get_current_year_publications(publications):
    pub_data = []
    current_year = datetime.now().year

    for pub in publications:
        try:
            pub_year = int(pub.get("bib", {}).get("pub_year", "0"))
            if pub_year != current_year:
                continue

            time.sleep(1)  # Rate limiting
            filled_pub = safe_fill(pub, timeout_sec=15)
            bib = filled_pub.get("bib", {})

            authors = bib.get("author", "N/A")
            if isinstance(authors, list):
                authors = ", ".join(authors)

            venue = bib.get("venue") or \
                    bib.get("journal") or \
                    bib.get("conference") or \
                    bib.get("booktitle") or \
                    bib.get("source", "N/A")

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
            print(f"⚠️ Skipping publication due to error: {e}")
            sys.stdout.flush()
            continue

    return pub_data

def save_to_json(data, filename):
    data_dir = Path(__file__).parent
    data_dir.mkdir(exist_ok=True)
    with open(data_dir / filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    author_id = "cyQLH48AAAAJ"
    publications = get_publications(author_id)
    pub_data = get_current_year_publications(publications)
    save_to_json(pub_data, "publications.json")
    print(f"✅ Retrieved {len(pub_data)} publications")
    print(f"📄 Saved to: {Path('publications.json').absolute()}")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
