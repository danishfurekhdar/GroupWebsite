import json

# Load existing publications
with open('_data/OldPubs.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

# Load new publications
with open('publications.json', 'r', encoding='utf-8') as f:
    new_data = json.load(f)

# Titles already in old_data
existing_titles = {pub['title'] for pub in old_data}

# Filter new publications that are not already in old_data
unique_new_pubs = [pub for pub in new_data if pub['title'] not in existing_titles]

# Add new ones to the top
merged_publications = unique_new_pubs + old_data

# Save merged list back
with open('_data/OldPubs.json', 'w', encoding='utf-8') as f:
    json.dump(merged_publications, f, indent=4)

print(f"✅ Added {len(unique_new_pubs)} new publication(s) to the top of OldPubs.json.")
