import json
import os

with open('data/editorial/curriculum-35-modules.json', 'r', encoding='utf-8') as f:
    modules = json.load(f)
module_codes = [m['code'] for m in modules]

schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "source_id": {"type": "string"},
        "annotation_version": {"type": "string"},
        "curriculum_version": {"type": "string"},
        "source_question_version": {"type": "string"},
        "annotator_id": {"type": "string", "enum": ["ANNOTATOR_A", "ANNOTATOR_B", "ADJUDICATOR"]},
        "in_curriculum": {"type": "boolean"},
        "primary_module": {"type": ["string", "null"], "enum": module_codes + [None]},
        "acceptable_modules": {
            "type": "array",
            "items": {"type": "string", "enum": module_codes}
        },
        "annotation_confidence": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"]},
        "reasoning_summary": {"type": "string"},
        "image_status": {"type": "string"},
        "image_required": {"type": "boolean"},
        "ambiguity": {"type": "boolean"},
        "ambiguity_reason": {"type": "string"},
        "supplement_used": {"type": "boolean"},
        "supplement_fields_used": {"type": "array", "items": {"type": "string"}},
        "annotation_status": {
            "type": "string",
            "enum": [
                "ANNOTATED",
                "IMAGE_REQUIRED",
                "INSUFFICIENT_CONTEXT",
                "AMBIGUOUS",
                "OUT_OF_CURRICULUM",
                "NEEDS_ADJUDICATION"
            ]
        },
        "module_evidence": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "kind": {"type": "string", "enum": ["STATEMENT", "CURRICULUM_SUBTOPIC"]},
                    "text": {"type": "string"},
                    "module": {"type": "string", "enum": module_codes},
                    "subtopic": {"type": "string"}
                },
                "required": ["kind"],
                "allOf": [
                    {
                        "if": {"properties": {"kind": {"const": "STATEMENT"}}},
                        "then": {"required": ["text"]}
                    },
                    {
                        "if": {"properties": {"kind": {"const": "CURRICULUM_SUBTOPIC"}}},
                        "then": {"required": ["module", "subtopic"]}
                    }
                ]
            }
        }
    },
    "required": [
        "source_id", "annotation_version", "curriculum_version", "source_question_version",
        "annotator_id", "in_curriculum", "acceptable_modules",
        "annotation_confidence", "reasoning_summary", "image_required",
        "ambiguity", "supplement_used", "annotation_status", "module_evidence"
    ],
    "allOf": [
        {
            "if": {"properties": {"annotation_status": {"const": "OUT_OF_CURRICULUM"}}},
            "then": {
                "properties": {
                    "in_curriculum": {"const": False},
                    "primary_module": {"type": "null"}
                },
                "required": ["primary_module"]
            }
        },
        {
            "if": {"properties": {"annotation_status": {"const": "ANNOTATED"}}},
            "then": {
                "properties": {
                    "in_curriculum": {"const": True},
                    "primary_module": {"type": "string"}
                },
                "required": ["primary_module"]
            }
        },
        {
            "if": {"properties": {"annotation_status": {"const": "IMAGE_REQUIRED"}}},
            "then": {"properties": {"image_required": {"const": True}}}
        },
        {
            "if": {"properties": {"annotation_status": {"const": "AMBIGUOUS"}}},
            "then": {
                "properties": {
                    "ambiguity": {"const": True},
                    "ambiguity_reason": {"type": "string", "minLength": 1}
                },
                "required": ["ambiguity_reason"]
            }
        },
        {
            "if": {"properties": {"supplement_used": {"const": False}}},
            "then": {"properties": {"supplement_fields_used": {"maxItems": 0}}}
        },
        {
            "if": {"properties": {"supplement_used": {"const": True}}},
            "then": {"properties": {"supplement_fields_used": {"minItems": 1}}}
        }
    ]
}

with open('data/editorial/schema-anotacao-v2.json', 'w', encoding='utf-8') as f:
    json.dump(schema, f, indent=2)
