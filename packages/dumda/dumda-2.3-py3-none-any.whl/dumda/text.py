from random import choice, randint
import os
import pandas as pd


def generate_text(paragraphs: int = 1):
    def getWords():
        filePath = os.path.join(os.path.dirname(__file__), 'latin.xls')
        df = pd.read_excel(filePath, sheet_name=2)
        return df

    def getType(word_type: str):
        words = getWords()
        return words['word'][words['type'] == word_type].tolist()

    def generate_sentence():
        sentence_length = randint(7, 14)
        words = getType('Noun') + getType('Verb') + getType('Adjective')

        sentence = list()
        for i in range(sentence_length):
            sentence.append(choice(words))

        if sentence_length > 10:
            sentence.insert(len(sentence) // 2, ",")

        sentence = " ".join(sentence)
        sentence = sentence.replace('?', '')
        sentence += '. '

        return sentence

    def generateParagraph():
        num_sentences = randint(4, 5)
        paragraph = generate_sentence() * num_sentences + "\n"
        return paragraph

    text = ''
    for j in range(paragraphs):
        text = text + generateParagraph()

    return text
