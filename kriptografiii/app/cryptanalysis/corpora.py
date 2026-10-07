import math
from typing import Dict

# Unigram frequency distributions (in percentages)
FREQ_INDONESIAN: Dict[str, float] = {
    'A': 19.26, 'N': 8.87, 'E': 8.52, 'I': 7.64, 'T': 5.76, 'U': 5.37,
    'R': 5.09, 'K': 4.88, 'D': 4.54, 'M': 4.41, 'S': 3.75, 'L': 3.49,
    'G': 3.32, 'P': 3.23, 'B': 2.59, 'Y': 1.48, 'O': 1.43, 'H': 1.40,
    'C': 0.81, 'J': 0.77, 'W': 0.44, 'V': 0.15, 'F': 0.11, 'Z': 0.05,
    'X': 0.02, 'Q': 0.01
}

FREQ_ENGLISH: Dict[str, float] = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
    'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
    'P': 1.93, 'B': 1.49, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07
}

# Common Bigrams
COMMON_BIGRAMS_ID = [
    "AN", "ME", "DI", "ER", "IN", "EN", "DA", "NG", "AR", "KA",
    "TI", "AL", "PA", "AT", "MA", "NY", "RA", "LA", "IS", "UK"
]

COMMON_BIGRAMS_EN = [
    "TH", "HE", "IN", "ER", "AN", "RE", "ED", "ON", "ES", "ST",
    "EN", "AT", "TO", "NT", "HA", "ND", "OU", "EA", "NG", "AS"
]

# Common Trigrams
COMMON_TRIGRAMS_ID = [
    "DAN", "KAN", "MEN", "TER", "BER", "PER", "ANG", "PEN", "NYA",
    "YAN", "ADA", "DAP", "INI", "ITU", "DAR", "PAD", "MAS", "UNT", "BIA"
]

COMMON_TRIGRAMS_EN = [
    "THE", "AND", "THA", "ENT", "ING", "ION", "NDE", "HAS", "NCE",
    "EDT", "TIS", "OFT", "STH", "MEN", "FOR", "ALL", "HIS", "ITH"
]

# Representative quadgrams / trigrams with log frequencies for scoring
# Common Indonesian high-frequency patterns
ID_PATTERNS = {
    "YANG": -3.2, "DENG": -3.5, "ENGA": -3.5, "NGAN": -3.4, "PADA": -3.8,
    "BER": -2.8, "TER": -2.9, "KAN": -2.7, "MEN": -2.8, "PER": -3.0,
    "PEN": -3.0, "DAN": -2.6, "NYA": -2.9, "UNT": -3.6, "NTU": -3.7,
    "TUK": -3.8, "TID": -3.7, "IDA": -3.7, "DAK": -3.8, "ADA": -3.1,
    "DAR": -3.4, "ARI": -3.4, "BIA": -4.0, "IAS": -4.1, "ASA": -3.9,
    "KEM": -3.9, "EMU": -4.0, "MUD": -4.1, "UDI": -4.1, "DIA": -3.6,
    "IAN": -3.5, "MER": -3.6, "ERE": -3.8, "EKA": -3.9, "MAS": -3.7,
    "ASI": -3.5, "SWA": -4.2, "INDO": -4.0, "NESI": -4.1, "ESIA": -4.1
}

EN_PATTERNS = {
    "TION": -3.1, "NTHE": -3.2, "THER": -3.3, "THAT": -3.4, "OFTH": -3.4,
    "FTHE": -3.4, "THES": -3.5, "WITH": -3.5, "INTH": -3.5, "ATIO": -3.6,
    "OFT": -3.0, "THE": -2.4, "AND": -2.8, "ING": -2.7, "ENT": -3.0,
    "ION": -3.0, "FOR": -3.2, "TIO": -3.1, "NDE": -3.3, "HAS": -3.4,
    "NCE": -3.4, "EDT": -3.5, "TIS": -3.5, "HIS": -3.5, "ALL": -3.6,
    "ARE": -3.4, "NOT": -3.5, "BUT": -3.6, "FROM": -3.8, "THEY": -3.7
}
