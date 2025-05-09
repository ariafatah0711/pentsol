import os
import json
from typing import List, Dict, Any, Optional
from config import DATA_FILE, DEFAULT_ALGORITHM, MAX_RESULTS

SEARCH_ALGORITHM = os.getenv('SEARCH_ALGORITHM', DEFAULT_ALGORITHM)

class SearchEngine:
    def __init__(self, algorithm: str = DEFAULT_ALGORITHM):
        self.algorithm = algorithm
        self.techniques = self._load_data()

    def _load_data(self) -> List[Dict[str, Any]]:
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Jika data dict dengan key 'techniques', ambil listnya
                if isinstance(data, dict) and 'techniques' in data:
                    return data['techniques']
                elif isinstance(data, list):
                    return data
                else:
                    return []
        except Exception as e:
            print(f"Error loading data: {e}")
            return []

    def search(self, query: str, max_results: int = MAX_RESULTS) -> List[Dict[str, Any]]:
        if not query or len(query) < 2:
            return []
        query = query.lower()
        if self.algorithm == 'boyer_moore':
            results = self._boyer_moore_search(query)
        elif self.algorithm == 'kmp':
            results = self._kmp_search(query)
        else:
            results = self._brute_force_search(query)
        return results[:max_results]

    def _boyer_moore_search(self, query: str) -> List[Dict[str, Any]]:
        results = []
        for tech in self.techniques:
            name = tech.get('name', '').lower()
            desc = tech.get('description', '').lower()
            if self._boyer_moore_match(name, query) or self._boyer_moore_match(desc, query):
                results.append({'technique': tech, 'score': 100})
        return results

    def _boyer_moore_match(self, text: str, pattern: str) -> bool:
        if not pattern:
            return True
        bad_char = {pattern[i]: i for i in range(len(pattern))}
        i = len(pattern) - 1
        while i < len(text):
            j = len(pattern) - 1
            k = i
            while j >= 0 and text[k] == pattern[j]:
                j -= 1
                k -= 1
            if j < 0:
                return True
            i += max(1, j - bad_char.get(text[i], -1))
        return False

    def _kmp_search(self, query: str) -> List[Dict[str, Any]]:
        results = []
        for tech in self.techniques:
            name = tech.get('name', '').lower()
            desc = tech.get('description', '').lower()
            if self._kmp_match(name, query) or self._kmp_match(desc, query):
                results.append({'technique': tech, 'score': 100})
        return results

    def _kmp_match(self, text: str, pattern: str) -> bool:
        if not pattern:
            return True
        failure = [0] * len(pattern)
        i = 1
        j = 0
        while i < len(pattern):
            if pattern[i] == pattern[j]:
                failure[i] = j + 1
                i += 1
                j += 1
            elif j > 0:
                j = failure[j-1]
            else:
                failure[i] = 0
                i += 1
        i = 0
        j = 0
        while i < len(text):
            if pattern[j] == text[i]:
                if j == len(pattern) - 1:
                    return True
                i += 1
                j += 1
            elif j > 0:
                j = failure[j-1]
            else:
                i += 1
        return False

    def _brute_force_search(self, query: str) -> List[Dict[str, Any]]:
        results = []
        for tech in self.techniques:
            name = tech.get('name', '').lower()
            desc = tech.get('description', '').lower()
            if query in name or query in desc:
                results.append({'technique': tech, 'score': 100})
        return results

    def get_technique_by_id(self, technique_id: str) -> Optional[Dict[str, Any]]:
        for tech in self.techniques:
            if str(tech.get('id')) == str(technique_id):
                return tech
        return None

    def get_categories(self) -> List[str]:
        categories = set()
        for tech in self.techniques:
            if 'category' in tech:
                categories.add(tech['category'])
        return sorted(list(categories))

    def get_techniques_by_category(self, category: str) -> List[Dict[str, Any]]:
        return [tech for tech in self.techniques if tech.get('category', '').lower() == category.lower()] 