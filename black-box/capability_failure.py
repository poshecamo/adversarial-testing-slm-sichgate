
# Capability Failure Test Scenarios

# This module contains test scenarios for detecting capability failures, where
# the model fails to reliably perform its intended function due to realistic
# input variations, edge cases, or ambiguous phrasing.

# Focus: Realistic Robustness Testing
# Target Models: Sentiment analysis (binary classification)
# Threat Category: Capability Failure


from core.test_infrastructure import (
    TestCase, TestScenario, ThreatCategory, Severity
)


def create_typo_robustness_scenario() -> TestScenario:
    
    # Typo and Misspelling Robustness Test Battery
    
    # Real-world text contains typos and misspellings. A production sentiment
    # model needs to handle common typos gracefully - it should still correctly
    # classify sentiment even when key words are misspelled.
    
    # This is critical for real deployments because:
    # - User reviews often contain typos
    # - Mobile input generates more spelling errors
    # - Non-native speakers make predictable mistakes
    
    # If your model only works on perfectly spelled text, it's not production-ready.
    
    # Test structure: Each test includes a common misspelling of a key sentiment word.
    # We expect the model to still get the sentiment right because the overall
    # context should make it clear.
    
    
    test_cases = [
        TestCase(
            id="TYPO_001",
            name="Positive Word Misspelling - 'great' -> 'grate'",
            description="Tests handling of common 'great' typo",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.HIGH,
            input_text="This product is grate and I would buy it again!",
            expected_behavior={'label': 'POSITIVE'},
            metadata={
                'typo_type': 'homophone',
                'correct_spelling': 'great',
                'expected_reason': 'Context "buy it again" indicates positive sentiment'
            }
        ),
        
        TestCase(
            id="TYPO_002",
            name="Negative Word Misspelling - 'terrible' -> 'terribel'",
            description="Tests handling of common 'terrible' typo",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.HIGH,
            input_text="Terribel product, waste of money.",
            expected_behavior={'label': 'NEGATIVE'},
            metadata={
                'typo_type': 'transposition',
                'correct_spelling': 'terrible',
                'expected_reason': 'Context "waste of money" reinforces negative sentiment'
            }
        ),
        
        TestCase(
            id="TYPO_003",
            name="Positive Word Misspelling - 'excellent' -> 'excelent'",
            description="Tests handling of missing double letter",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.MEDIUM,
            input_text="Excelent service, very satisfied!",
            expected_behavior={'label': 'POSITIVE'},
            metadata={
                'typo_type': 'missing_letter',
                'correct_spelling': 'excellent',
                'expected_reason': 'Context "very satisfied" indicates positive sentiment'
            }
        ),
        
        TestCase(
            id="TYPO_004",
            name="Negative Word Misspelling - 'disappointed' -> 'dissapointed'",
            description="Tests handling of common misspelling pattern",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.MEDIUM,
            input_text="I was dissapointed with the quality.",
            expected_behavior={'label': 'NEGATIVE'},
            metadata={
                'typo_type': 'wrong_letter',
                'correct_spelling': 'disappointed',
                'expected_reason': 'Disappointment is clearly negative'
            }
        ),
        
        TestCase(
            id="TYPO_005",
            name="Multiple Typos in Positive Review",
            description="Tests robustness to multiple concurrent typos",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.HIGH,
            input_text="Awsome prodcut! Realy happy with my purchas.",
            expected_behavior={'label': 'POSITIVE'},
            metadata={
                'typo_type': 'multiple',
                'typo_count': 4,
                'expected_reason': 'Overall tone is clearly enthusiastic and positive'
            }
        ),
    ]
    
    scenario = TestScenario(
        id="capability_typo_robustness",
        name="Typo & Misspelling Robustness",
        description=(
            "Tests whether the model correctly classifies sentiment when common "
            "typos and misspellings are present. Production models must handle "
            "imperfect input gracefully."
        ),
        category=ThreatCategory.CAPABILITY_FAILURE,
        test_cases=test_cases,
        pro_version_note=(
            "SichGate Pro includes comprehensive robustness testing with "
            "automated perturbation generation across phonetic, visual, and "
            "semantic dimensions. Pro testing systematically finds minimal "
            "character changes that cause misclassification and quantifies "
            "your model's robustness boundaries. Contact sales@sichgate.com."
        )
    )
    
    return scenario


def create_semantic_edge_cases_scenario() -> TestScenario:
    
    # Semantic Edge Cases Test Battery
    
    # These tests check whether the model correctly handles linguistically
    # complex inputs like:
    # - Double negatives (which create positive meaning)
    # - Sarcasm and irony (where surface meaning != intended meaning)
    # - Mixed sentiment (positive and negative in same text)
    # - Ambiguous phrasing (could be interpreted eitherr way)
    
    # These are hard cases that often trip up sentiment models because they
    # require deeper understanding of context and pragmatics, not just
    # keyword matching.
    
    
    test_cases = [
        # Double negatives
        TestCase(
            id="EDGE_001",
            name="Double Negative Creating Positive",
            description="Tests understanding of 'not bad' as positive",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.HIGH,
            input_text="Not bad at all, actually quite good.",
            expected_behavior={'label': 'POSITIVE'},
            metadata={
                'edge_case_type': 'double_negative',
                'linguistic_pattern': 'litotes',
                'expected_reason': '"Not bad" + "quite good" indicates positive sentiment'
            }
        ),
        
        TestCase(
            id="EDGE_002",
            name="Double Negative With Emphasis",
            description="Tests 'couldn't be happier' construction",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.MEDIUM,
            input_text="I couldn't be happier with this purchase!",
            expected_behavior={'label': 'POSITIVE'},
            metadata={
                'edge_case_type': 'double_negative',
                'linguistic_pattern': 'emphatic_negation',
                'expected_reason': 'Idiomatic expression meaning extremely happy'
            }
        ),
        
        TestCase(
            id="EDGE_003",
            name="Triple Negative Edge Case",
            description="Tests complex negative structure",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.MEDIUM,
            input_text="I don't disagree that it's not terrible.",
            expected_behavior={'label': 'POSITIVE'},
            metadata={
                'edge_case_type': 'triple_negative',
                'linguistic_pattern': 'complex_negation',
                'expected_reason': 'Triple negative resolves to weak positive'
            }
        ),
        
        # Sarcasm and irony (these are genuinely hard)
        TestCase(
            id="EDGE_004",
            name="Obvious Sarcasm - Negative Disguised as Positive",
            description="Tests detection of sarcastic positive statement",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.CRITICAL,
            input_text="Oh great, another broken product. Just what I needed.",
            expected_behavior={'label': 'NEGATIVE'},
            metadata={
                'edge_case_type': 'sarcasm',
                'difficulty': 'high',
                'expected_reason': 'Context "broken product" reveals sarcasm',
                'note': 'Sarcasm detection is difficult even for humans without tone'
            }
        ),
        
        TestCase(
            id="EDGE_005",
            name="Ironic Understatement",
            description="Tests ironic positive framing of negative experience",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.HIGH,
            input_text="Fantastic! It broke after one day. Exactly what I expected from this company.",
            expected_behavior={'label': 'NEGATIVE'},
            metadata={
                'edge_case_type': 'irony',
                'difficulty': 'high',
                'expected_reason': '"Broke after one day" indicates product failure'
            }
        ),
        
        # Mixed sentiment
        TestCase(
            id="EDGE_006",
            name="Mixed Sentiment - Negative Outweighs Positive",
            description="Tests handling of mixed signals where negative dominates",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.HIGH,
            input_text="Great packaging, but the product inside was completely defective.",
            expected_behavior={'label': 'NEGATIVE'},
            metadata={
                'edge_case_type': 'mixed_sentiment',
                'sentiment_balance': 'negative_dominant',
                'expected_reason': 'Product defect is more important than packaging'
            }
        ),
        
        TestCase(
            id="EDGE_007",
            name="Mixed Sentiment - Positive Outweighs Negative",
            description="Tests handling of mixed signals where positive dominates",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.MEDIUM,
            input_text="Shipping took forever, but the product itself is amazing and worth the wait.",
            expected_behavior={'label': 'POSITIVE'},
            metadata={
                'edge_case_type': 'mixed_sentiment',
                'sentiment_balance': 'positive_dominant',
                'expected_reason': '"Amazing" and "worth the wait" indicate overall satisfaction'
            }
        ),
        
        TestCase(
            id="EDGE_008",
            name="Contradictory Statements",
            description="Tests handling of directly contradictory sentiment expressions",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.HIGH,
            input_text="I hate to love this product, but I absolutely recommend it.",
            expected_behavior={'label': 'POSITIVE'},
            metadata={
                'edge_case_type': 'contradiction',
                'expected_reason': '"Absolutely recommend" indicates positive overall judgment'
            }
        ),
        
        # Ambiguous phrasing
        TestCase(
            id="EDGE_009",
            name="Minimalist Positive",
            description="Tests very understated positive sentiment",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.MEDIUM,
            input_text="It's fine. Does what it's supposed to do.",
            expected_behavior={'label': 'POSITIVE'},
            metadata={
                'edge_case_type': 'ambiguous_positive',
                'sentiment_strength': 'weak',
                'expected_reason': '"Does what it\'s supposed to" indicates satisfaction'
            }
        ),
        
        TestCase(
            id="EDGE_010",
            name="Faint Praise vs Genuine Positive",
            description="Tests distinction between damning with faint praise and genuine positivity",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.MEDIUM,
            input_text="It's not the worst thing I've ever bought.",
            expected_behavior={'label': 'POSITIVE'},
            metadata={
                'edge_case_type': 'faint_praise',
                'sentiment_strength': 'weak',
                'expected_reason': 'Weak positive via comparison to worse alternatives',
                'note': 'This could reasonably be classified as neutral or negative depending on context'
            }
        ),
    ]
    
    scenario = TestScenario(
        id="capability_semantic_edges",
        name="Semantic Edge Cases & Linguistic Complexity",
        description=(
            "Tests whether the model correctly handles linguistically complex "
            "inputs including double negatives, sarcasm, mixed sentiment, and "
            "ambiguous phrasing. These cases require deeper semantic understanding."
        ),
        category=ThreatCategory.CAPABILITY_FAILURE,
        test_cases=test_cases,
        pro_version_note=(
            "SichGate Pro includes advanced linguistic analysis that automatically "
            "generates edge cases specific to your model's architecture and training "
            "data. Pro version identifies semantic patterns your model struggles with "
            "and provides targeted recommendations for improving robustness. "
            "Contact sales@sichgate.com for a demo."
        )
    )
    
    return scenario


def create_format_variation_scenario() -> TestScenario:  
    test_cases = [
        TestCase(
            id="FORMAT_001",
            name="ALL CAPS Positive",
            description="Tests if all-caps input affects sentiment detection",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.MEDIUM,
            input_text="THIS IS THE BEST PRODUCT I'VE EVER USED!",
            expected_behavior={'label': 'POSITIVE'},
            metadata={
                'format_variation': 'capitalization',
                'baseline': 'This is the best product I\'ve ever used!',
                'expected_reason': 'Caps often indicate emphasis, not sentiment change'
            }
        ),
        
        TestCase(
            id="FORMAT_002",
            name="Excessive Punctuation",
            description="Tests handling of repeated exclamation marks",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.LOW,
            input_text="This is terrible!!!!!!!",
            expected_behavior={'label': 'NEGATIVE'},
            metadata={
                'format_variation': 'punctuation',
                'baseline': 'This is terrible.',
                'expected_reason': 'Extra punctuation emphasizes but doesn\'t change sentiment'
            }
        ),
        
        TestCase(
            id="FORMAT_003",
            name="Emoji Addition to Positive Text",
            description="Tests if emoji presence affects classification",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.LOW,
            input_text="Love this product! 😍 ❤️ 🎉",
            expected_behavior={'label': 'POSITIVE'},
            metadata={
                'format_variation': 'emoji',
                'baseline': 'Love this product!',
                'expected_reason': 'Emojis reinforce but don\'t create sentiment'
            }
        ),
        
        TestCase(
            id="FORMAT_004",
            name="Extra Whitespace",
            description="Tests robustness to unusual spacing",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.LOW,
            input_text="This    is    really    great    !",
            expected_behavior={'label': 'POSITIVE'},
            metadata={
                'format_variation': 'whitespace',
                'baseline': 'This is really great!',
                'expected_reason': 'Extra spaces shouldn\'t affect tokenization'
            }
        ),
        
        TestCase(
            id="FORMAT_005",
            name="No Punctuation",
            description="Tests handling of text without proper punctuation",
            category=ThreatCategory.CAPABILITY_FAILURE,
            severity=Severity.MEDIUM,
            input_text="terrible product waste of money",
            expected_behavior={'label': 'NEGATIVE'},
            metadata={
                'format_variation': 'punctuation_missing',
                'baseline': 'Terrible product, waste of money.',
                'expected_reason': 'Lack of punctuation shouldn\'t hide negative words'
            }
        ),
    ]
    
    scenario = TestScenario(
        id="capability_format_variation",
        name="Format Variation Robustness",
        description=(
            "Tests whether the model produces consistent predictions when inputs "
            "vary in formatting (capitalization, punctuation, spacing) but have "
            "the same semantic meaning."
        ),
        category=ThreatCategory.CAPABILITY_FAILURE,
        test_cases=test_cases,
        pro_version_note=(
            "SichGate Pro automatically generates format variations and tests for "
            "prediction stability across formatting dimensions. Pro version includes "
            "statistical analysis of format sensitivity and identifies which "
            "formatting patterns cause unreliable predictions. Contact sales@sichgate.com."
        )
    )
    
    return scenario


# Convenience function to get all capability failure scenarios
def get_all_capability_scenarios() -> list[TestScenario]:
    return [
        create_typo_robustness_scenario(),
        create_semantic_edge_cases_scenario(),
        create_format_variation_scenario()
    ]