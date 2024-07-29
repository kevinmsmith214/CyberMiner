import sys
import os
import streamlit as st

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        word = word.lower()
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, prefix):
        node = self.root
        prefix = prefix.lower()
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._find_all_words(node, prefix)

    def _find_all_words(self, node, prefix):
        words = []
        if node.is_end_of_word:
            words.append(prefix)
        for char in node.children:
            words.extend(self._find_all_words(node.children[char], prefix + char))
        return words


def main():
    trie = Trie()
    titles = [
        "Step-by-Step: Mastering the Art of French Cooking",
        "Beginner's Guide to Meditation: Finding Inner Peace",
        "DIY Home Repairs: Fixing a Leaky Faucet with Ease",
        "Plan Your Dream Vacation: A Comprehensive Travel Checklist",
        "My Journey Through the Himalayas: Lessons and Landscapes",
        "Surviving a Startup: What I Learned in My First Year",
        "Finding Love in Unexpected Places: A Modern Romance Tale",
        "The Day I Met My Hero: An Unforgettable Encounter",
        "The Future of Renewable Energy: Challenges and Opportunities",
        "Why Education Needs a Revolution: A Perspective",
        "The Impact of Social Media on Modern Relationships",
        "Privacy in the Digital Age: How Much Are We Losing?",
        "2024 Smartphone Roundup: Which Model Tops the Charts?",
        "Best Coffee Shops in New York: Where to Find the Perfect Brew",
        "Comparing Streaming Services: Which One Wins for Original Content?",
        "SUV vs. Sedan: What's Best for Your Family?",
        "Top 10 Video Games of the Year: Must-Plays for Gamers",
        "Laugh Out Loud: A Compilation of the Best Comedies",
        "Magical Movie Moments: Films That Transport You",
        "Escape Room Challenges: Can You Break Out?",
        "Understanding Blockchain: The Technology Behind Cryptocurrencies",
        "How to Run a Marathon",
        "How to Fry an Egg",
        "Gaming, A How to Guide"
    ]
    for title in titles:
        trie.insert(title)

    st.title('Real-time Autocomplete Example')
    user_input = st.text_input("Start typing to get suggestions:", "")

    if user_input:
        # Search for suggestions based on the Trie
        suggestions = trie.search(user_input.lower())
        if suggestions:
            st.write("Suggestions:")
            for suggestion in suggestions:
                st.write(suggestion)
        else:
            st.write("No suggestions found.")

if __name__ == "__main__":
    main()