
# SichGate Core Framework

# This package contains the fundamental building blocks of the SichGate testing framework:
# - Model interface abstractions
# - Test infrastructure (test cases, scenarios, runners)
# - Result handling and reporting

# These components are designed to be reusable across different test scenarios
# and model types.

from .model_interface import ModelInterface, HuggingFaceSentimentModel
from .test_infrastructure import (
    TestCase,
    TestScenario,
    TestResult,
    TestRunner,
    ThreatCategory,
    Severity
)

__all__ = [
    'ModelInterface',
    'HuggingFaceSentimentModel',
    'TestCase',
    'TestScenario',
    'TestResult',
    'TestRunner',
    'ThreatCategory',
    'Severity'
]

from .behavioral_subversion import (
    create_prompt_injection_scenario,
    get_all_behavioral_scenarios
)

from .capability_failure import (
    create_typo_robustness_scenario,
    create_semantic_edge_cases_scenario,
    create_format_variation_scenario,
    get_all_capability_scenarios
)

__all__ = [
    'create_prompt_injection_scenario',
    'get_all_behavioral_scenarios',
    'create_typo_robustness_scenario',
    'create_semantic_edge_cases_scenario',
    'create_format_variation_scenario',
    'get_all_capability_scenarios'
]
from .behavioral_subversion import (
    create_prompt_injection_scenario,
    get_all_behavioral_scenarios
)

from .capability_failure import (
    create_typo_robustness_scenario,
    create_semantic_edge_cases_scenario,
    create_format_variation_scenario,
    get_all_capability_scenarios
)

from .information_disclosure import (
    create_training_data_extraction_scenario,
    create_rag_isolation_scenario,
    get_all_information_disclosure_scenarios
)

__all__ = [
    'create_prompt_injection_scenario',
    'get_all_behavioral_scenarios',
    'create_typo_robustness_scenario',
    'create_semantic_edge_cases_scenario',
    'create_format_variation_scenario',
    'get_all_capability_scenarios',
    'create_training_data_extraction_scenario',
    'create_rag_isolation_scenario',
    'get_all_information_disclosure_scenarios'
]
