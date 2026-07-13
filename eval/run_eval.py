import json
import asyncio
from pathlib import Path
from datetime import datetime
import sys

sys.path.append(str(Path(__file__).parent.parent))

from services.rag import retrieve, generate_answer
from eval.judge import judge_answer

DATASET_PATH = Path(__file__).parent / "golden_dataset.json"
RESULTS_DIR = Path(__file__).parent / "results"

def load_dataset() -> list[dict]:
    return json.loads(DATASET_PATH.read_text())

def check_topics(answer: str, expected_topics: list[str]) -> dict:
    answer_lower = answer.lower()
    results = {}
    for topic in expected_topics:
        results[topic] = topic.lower() in answer_lower
    return results

async def run_single(case: dict) -> dict:
    sources = retrieve(case["question"])
    answer = generate_answer(case["question"], case["document"], sources)

    topic_results = check_topics(answer, case["expected_topics"])
    covered = sum(topic_results.values())
    total = len(topic_results)
    coverage_score = round(covered / total * 100) if total > 0 else 0

    judgment = judge_answer(case["question"], answer, case["expected_topics"], sources)

    return {
        "id": case["id"],
        "question": case["question"],
        "answer": answer,
        "sources_count": len(sources),
        "topic_coverage": topic_results,
        "coverage_score": coverage_score,
        "heuristic_passed": coverage_score >= 75,
        "judgment": judgment,
        "passed": judgment["passed"]
    }

async def run_eval():
    dataset = load_dataset()
    results = []

    print(f"Running eval on {len(dataset)} cases...\n")

    for case in dataset:
        print(f"  [{case['id']}] {case['question'][:60]}...")
        result = await run_single(case)
        results.append(result)
        j = result["judgment"]
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        print(f"  {status} overall: {j['overall']}/10 | relevance: {j['relevance']} faithfulness: {j['faithfulness']} coverage: {j['coverage']}")
        print(f"       {j['comment']}")

    passed = sum(1 for r in results if r["passed"])
    avg_overall = round(sum(r["judgment"]["overall"] for r in results) / len(results), 1)

    print(f"\n{'='*40}")
    print(f"Results: {passed}/{len(results)} passed")
    print(f"Average overall score: {avg_overall}/10")

    RESULTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = RESULTS_DIR / f"eval_{timestamp}.json"

    output = {
        "timestamp": timestamp,
        "total": len(results),
        "passed": passed,
        "avg_overall": avg_overall,
        "cases": results
    }

    output_path.write_text(json.dumps(output, indent=2))
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    asyncio.run(run_eval())