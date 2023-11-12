from dataclasses import dataclass
from enum import Enum
import re
import nltk
from rake_nltk import Rake

class FeatureType(Enum):
    IoC_DNS = 1
    IoC_IP = 2
    IoC_Hash = 3
    Yara = 4
    
class Tags(Enum):
    Ransomware = 1
    Cybercrime = 2

@dataclass
class Feature:
    ft_type: FeatureType
    value: str
    
    def to_json(self) -> str:
        return {
            "type": self.ft_type,
            "value": self.value
        }
        
    @staticmethod
    def from_json(data: dict) -> "Feature":
        return Feature(data["type"], data["value"])
    
def get_keywords_from_markdown(text: str, limit: int = 10, score_threshold: int = 14):
    # cleanup text
    # remove images
    text = re.sub(r"!\[(.*?)\]\(.+?\)", r"", text)
    # remove links but keep the text
    text = re.sub(r"\[(.*?)\]\(.+?\)", r"\1", text)
    # remove styling
    text = text.replace("**", "")
    text = text.replace("### ", "")
    text = text.replace("## ", "")
    text = text.replace("# ", "")
    
    # TODO: remove ?
    # remove code blocks
    text = re.sub(r"```[.\w\n\r :\-\>\<\[\]\/\+\"“]*```", r"", text)
    
    # uncomment to write cleaned text to disk
    # with open("res.md", "w") as f:
    #     f.write(text)
    
    # download models
    nltk.download("stopwords", quiet=True)
    nltk.download("punkt", quiet=True)
    
    # extract keywords
    r = Rake()
    r.extract_keywords_from_text(text)
    
    # process best words
    keywords_scored = sorted(r.get_word_degrees().items(), key=lambda x: x[1], reverse=True)
    keywords_scored = [k for k in keywords_scored if k[1] >= score_threshold and len(k[0]) >= 3 and not k[0].isdigit()]
    
    # remove IOCS
    # TODO: find better detection system
    keywords_scored = [k for k in keywords_scored if len(k[0]) != 40 and k[0] != "[.]"]
    
    keywords = [k for k in keywords_scored[:limit]]
    
    return keywords