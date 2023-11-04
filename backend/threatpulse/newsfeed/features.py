from dataclasses import dataclass
from enum import Enum

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