import copy
import json
import os
import subprocess
import sys
import tempfile


def run_validator(pack, envelope):
    with tempfile.TemporaryDirectory() as td:
        pack_path = os.path.join(td, "content.json")
        annotations_path = os.path.join(td, "annotations.json")
        with open(pack_path, "w", encoding="utf-8") as f:
            json.dump(pack, f)
        with open(annotations_path, "w", encoding="utf-8") as f:
            json.dump(envelope, f)

        return subprocess.run(
            [
                sys.executable,
                "scripts/validar-anotacoes.py",
                "--pack",
                pack_path,
                "--annotations",
                annotations_path,
            ],
            capture_output=True,
            text=True,
        )


def annotation(source_id, reasoning, evidence, annotator="ANNOTATOR_A"):
    return {
        "source_id": source_id,
        "annotation_version": "1.0",
        "curriculum_version": "1.0",
        "source_question_version": "1.0",
        "annotator_id": annotator,
        "in_curriculum": True,
        "primary_module": "F01",
        "acceptable_modules": [],
        "annotation_confidence": "HIGH",
        "reasoning_summary": reasoning,
        "image_status": "NOT_APPLICABLE",
        "image_required": False,
        "ambiguity": False,
        "ambiguity_reason": "",
        "supplement_used": False,
        "supplement_fields_used": [],
        "annotation_status": "ANNOTATED",
        "module_evidence": [{"kind": "STATEMENT", "text": evidence}],
    }


def base_pack(n=1):
    return {
        "batch_id": "quality-test",
        "curriculum_version": "1.0",
        "questions": [
            {
                "source_id": f"Q{i}",
                "source_question_version": "1.0",
                "statement": f"A unidade elétrica da questão Q{i} é o volt e deve ser identificada corretamente.",
                "has_image": False,
                "image_inventory_status": "NOT_APPLICABLE",
            }
            for i in range(1, n + 1)
        ],
    }


def test_positive():
    pack = base_pack(1)
    env = {
        "batch_id": "quality-test",
        "annotator_id": "ANNOTATOR_A",
        "annotations": [
            annotation(
                "Q1",
                "A questão pede identificação direta de unidade elétrica, portanto pertence ao módulo de grandezas.",
                "A unidade elétrica da questão Q1 é o volt",
            )
        ],
    }
    res = run_validator(pack, env)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "ANNOTATION_QUALITY_VALID = true" in res.stdout


def test_placeholder_reasoning_rejected():
    pack = base_pack(1)
    env = {
        "batch_id": "quality-test",
        "annotator_id": "ANNOTATOR_A",
        "annotations": [
            annotation(
                "Q1",
                "Auto generated reasoning.",
                "A unidade elétrica da questão Q1 é o volt",
            )
        ],
    }
    res = run_validator(pack, env)
    assert res.returncode != 0
    assert "PLACEHOLDER_REASONING" in res.stdout


def test_placeholder_evidence_rejected():
    pack = base_pack(1)
    env = {
        "batch_id": "quality-test",
        "annotator_id": "ANNOTATOR_A",
        "annotations": [
            annotation(
                "Q1",
                "A questão pede identificação direta de unidade elétrica e tem contexto suficiente.",
                "evidence",
            )
        ],
    }
    res = run_validator(pack, env)
    assert res.returncode != 0
    assert "STATEMENT_EVIDENCE_TOO_SHORT" in res.stdout or "PLACEHOLDER_EVIDENCE" in res.stdout


def test_ungrounded_statement_evidence_rejected():
    pack = base_pack(1)
    env = {
        "batch_id": "quality-test",
        "annotator_id": "ANNOTATOR_A",
        "annotations": [
            annotation(
                "Q1",
                "A questão pede identificação direta de unidade elétrica e tem contexto suficiente.",
                "texto que não existe de forma alguma no enunciado original",
            )
        ],
    }
    res = run_validator(pack, env)
    assert res.returncode != 0
    assert "STATEMENT_EVIDENCE_NOT_GROUNDED" in res.stdout


def test_repeated_reasoning_template_rejected():
    pack = base_pack(4)
    repeated = "A mesma justificativa genérica foi repetida sem análise específica da questão."
    env = {
        "batch_id": "quality-test",
        "annotator_id": "ANNOTATOR_A",
        "annotations": [
            annotation(
                f"Q{i}",
                repeated,
                f"A unidade elétrica da questão Q{i} é o volt",
            )
            for i in range(1, 5)
        ],
    }
    res = run_validator(pack, env)
    assert res.returncode != 0
    assert "REPEATED_REASONING_TEMPLATE" in res.stdout


def run_tests():
    test_positive()
    test_placeholder_reasoning_rejected()
    test_placeholder_evidence_rejected()
    test_ungrounded_statement_evidence_rejected()
    test_repeated_reasoning_template_rejected()
    print("ANNOTATION QUALITY TESTS PASSED")


if __name__ == "__main__":
    run_tests()
