from fuzzywuzzy import fuzz
from typing import List, Dict, Optional
import json
from config import SEARCH_THRESHOLD, MAX_RESULTS

class SearchEngine:
    def __init__(self, data_file: str):
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                self.techniques = json.load(f)
            if not isinstance(self.techniques, list):
                raise ValueError("JSON data must be a list of techniques")
        except Exception as e:
            print(f"Error loading data: {e}")
            self.techniques = []

    @staticmethod
    def best_score(query: str, text: str) -> int:
        """Calculate the best matching score between query and text"""
        return max(
            fuzz.partial_ratio(query.lower(), text.lower()),
            fuzz.token_set_ratio(query.lower(), text.lower())
        )

    def search(self, query: str) -> List[Dict]:
        """Search techniques based on query using fuzzy matching"""
        results = []
        for technique in self.techniques:
            name_score = self.best_score(query, technique['name'])
            desc_score = self.best_score(query, technique['description'])
            category_score = self.best_score(query, technique['category'])
            max_score = max(name_score, desc_score, category_score)

            if max_score >= SEARCH_THRESHOLD:
                results.append({
                    'technique': technique,
                    'score': max_score
                })

        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:MAX_RESULTS]

    def get_technique_by_id(self, technique_id: str) -> Optional[Dict]:
        """Get technique details by ID"""
        for technique in self.techniques:
            if technique['id'] == technique_id:
                return technique
        return None

    def get_categories(self) -> List[str]:
        """Get unique list of categories from techniques"""
        if not self.techniques:
            return []
        categories = set(t['category'] for t in self.techniques if 'category' in t)
        return sorted(list(categories))

    def get_techniques_by_category(self, category: str) -> List[Dict]:
        """Get list of techniques by category"""
        return [t for t in self.techniques if 'category' in t and t['category'].lower() == category.lower()] 