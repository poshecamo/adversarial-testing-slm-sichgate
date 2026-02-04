
# Model Interface Layer for SichGate Testing Framework

# This module provides a unified interface for interacting with different types of models:
# - HuggingFace models (sentiment, classification, etc.)
# - Local PyTorch models
# - API endpoints (future: OpenAI, Anthropic, custom APIs)

# The abstraction allows test cases to be written once and run against any model type.

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import time
import json


class ModelInterface(ABC):
    def __init__(self):
        self.query_count = 0
        self.total_latency = 0.0
        
    @abstractmethod
    def predict(self, text: str) -> Dict[str, Any]:
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        avg_latency = self.total_latency / self.query_count if self.query_count > 0 else 0
        return {
            'total_queries': self.query_count,
            'total_latency_seconds': round(self.total_latency, 3),
            'average_latency_ms': round(avg_latency * 1000, 2)
        }


class HuggingFaceSentimentModel(ModelInterface):
    """
    Wrapper for HuggingFace sentiment analysis models.
    
    This is specifically designed for binary sentiment models (positive/negative)
    like distilbert-base-uncased-finetuned-sst-2-english.
    
    Design note: We inherit from ModelInterface to ensure consistency, but we add
    sentiment-specific functionality like label mapping and confidence thresholds.
    """
    
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        super().__init__()
        self.model_name = model_name
        
        print(f"Loading model: {model_name}")
        print("This may take a moment on first run as weights are downloaded...")
        
        # Load the tokenizer and model
        # Using .from_pretrained() caches models locally, so subsequent runs are fast
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        
        # Set to evaluation mode (disables dropout, etc.)
        self.model.eval()
        
        # Sentiment models typically use id2label mapping
        # This maps the numeric output (0, 1) to semantic labels
        self.label_map = self.model.config.id2label
        
        print(f"Model loaded successfully. Label mapping: {self.label_map}")
    
    def predict(self, text: str) -> Dict[str, Any]:
        start_time = time.time()
        
        # Tokenize the input
        # return_tensors="pt" gives us PyTorch tensors
        inputs = self.tokenizer(
            text, 
            return_tensors="pt", 
            truncation=True,
            max_length=512  # Standard BERT-style model limit
        )
        
        # Run inference
        with torch.no_grad():
            outputs = self.model(**inputs)
            
        # Convert logits to probabilities
        # Logits are raw scores; softmax normalizes them to sum to 1
        probs = torch.softmax(outputs.logits, dim=-1)
        
        # Get the predicted class and its confidence
        predicted_class_id = int(torch.argmax(probs))
        confidence = float(torch.max(probs))
        
        # Map numeric ID to semantic label
        label = self.label_map.get(predicted_class_id, f"CLASS_{predicted_class_id}")
        
        # Update statistics
        latency = time.time() - start_time
        self.query_count += 1
        self.total_latency += latency
        
        return {
            'label': label,
            'confidence': confidence,
            'raw_output': {
                'logits': outputs.logits.tolist(),
                'probabilities': probs.tolist(),
                'predicted_id': predicted_class_id
            },
            'latency_ms': round(latency * 1000, 2)
        }
    
    def predict_batch(self, texts: list) -> list:
        start_time = time.time()
        
        # Tokenize all texts at once
        inputs = self.tokenizer(
            texts,
            return_tensors="pt",
            truncation=True,
            padding=True,  # Pad to the longest sequence in batch
            max_length=512
        )
        
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        probs = torch.softmax(outputs.logits, dim=-1)
        
        results = []
        for i in range(len(texts)):
            predicted_class_id = int(torch.argmax(probs[i]))
            confidence = float(torch.max(probs[i]))
            label = self.label_map.get(predicted_class_id, f"CLASS_{predicted_class_id}")
            
            results.append({
                'label': label,
                'confidence': confidence,
                'raw_output': {
                    'logits': outputs.logits[i].tolist(),
                    'probabilities': probs[i].tolist(),
                    'predicted_id': predicted_class_id
                }
            })
        
        # Update statistics for batch
        latency = time.time() - start_time
        self.query_count += len(texts)
        self.total_latency += latency
        
        return results


class LocalPyTorchModel(ModelInterface):
    
    def __init__(self, model_path: str, preprocessing_fn=None, label_map=None):
        super().__init__()
        self.model_path = model_path
        self.preprocessing_fn = preprocessing_fn or (lambda x: x)
        self.label_map = label_map or {0: "CLASS_0", 1: "CLASS_1"}
        
        # Load the model
        self.model = torch.load(model_path)
        self.model.eval()
    
    def predict(self, text: str) -> Dict[str, Any]:
        start_time = time.time()
        
        # Apply user-provided preprocessing
        processed_input = self.preprocessing_fn(text)
        
        with torch.no_grad():
            output = self.model(processed_input)
        
        # Assume output is logits, convert to probabilities
        if len(output.shape) > 1:
            probs = torch.softmax(output, dim=-1)
            predicted_class_id = int(torch.argmax(probs))
            confidence = float(torch.max(probs))
        else:
            # Binary classification with sigmoid
            prob = torch.sigmoid(output)
            predicted_class_id = 1 if prob > 0.5 else 0
            confidence = float(prob) if predicted_class_id == 1 else float(1 - prob)
        
        label = self.label_map.get(predicted_class_id, f"CLASS_{predicted_class_id}")
        
        latency = time.time() - start_time
        self.query_count += 1
        self.total_latency += latency
        
        return {
            'label': label,
            'confidence': confidence,
            'raw_output': output.tolist(),
            'latency_ms': round(latency * 1000, 2)
        }


class APIModel(ModelInterface):
    def __init__(self, api_endpoint: str, api_key: Optional[str] = None):
        super().__init__()
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        
        # TODO: Implement API client logic
        # This would include:
        # - Request construction
        # - Rate limiting
        # - Retry logic with exponential backoff
        # - Error handling
        
    def predict(self, text: str) -> Dict[str, Any]:
        raise NotImplementedError(
            "API model support is coming in SichGate Pro. "
            "For early access, contact us at support@sichgate.com"
        )