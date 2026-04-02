# AGENT 5: Cost Estimator Agent (Hybrid - Balanced Approach)
# Real-time hospital price adjustment + deterministic cost calculation + light LLM for summary

import json
import os
import requests
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

# ── Cost Benchmarks ─────────────────────────────────────────────────────────
COST_BENCHMARKS = {
    "General Physician": {"consultation_min": 400, "consultation_max": 1200, "tests": {"blood_test": 600, "urine_test": 250, "xray": 900, "cbc": 550}, "medicines_avg": 500},
    "Cardiologist": {"consultation_min": 1200, "consultation_max": 3000, "tests": {"ecg": 500, "echo": 2800, "stress_test": 4000}, "medicines_avg": 1800},
    "Emergency Medicine": {"consultation_min": 2000, "consultation_max": 6000, "tests": {"blood_panel": 2500, "ct_scan": 8500, "xray": 1000}, "medicines_avg": 2500},
    "Orthopedic": {"consultation_min": 900, "consultation_max": 2500, "tests": {"xray": 900, "mri": 6500}, "medicines_avg": 1000},
    "Dermatologist": {"consultation_min": 600, "consultation_max": 1800, "tests": {"skin_biopsy": 2500}, "medicines_avg": 700}
}

INSURANCE_PLANS = { ... }   # Keep your existing INSURANCE_PLANS
CURRENCY_RATES = { ... }    # Keep your existing CURRENCY_RATES

# ── Real-time Hospital Price Adjustment ─────────────────────────────────────
def get_hospital_price_level(hospital_name: str, city: str = "Kolkata") -> dict:
    if not GOOGLE_PLACES_API_KEY:
        return {"multiplier": 1.0, "note": "Using standard benchmarks"}
    
    try:
        url = "https://places.googleapis.com/v1/places:searchText"
        payload = {"textQuery": f"{hospital_name} {city}", "maxResultCount": 3}
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
            "X-Goog-FieldMask": "places.priceLevel"
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        data = resp.json()

        for place in data.get("places", []):
            level = place.get("priceLevel")
            if level is not None:
                multiplier = 0.8 if level <= 1 else 1.0 if level == 2 else 1.3 if level == 3 else 1.6
                return {"multiplier": multiplier, "note": f"Price level {level} from Google"}
    except:
        pass
    return {"multiplier": 1.0, "note": "Using standard benchmarks"}


# ── Core Cost Calculation (Deterministic) ───────────────────────────────────
def calculate_cost_breakdown(specialty: str, city: str, hospital_name: str = None) -> dict:
    benchmark = COST_BENCHMARKS.get(specialty, COST_BENCHMARKS["General Physician"])
    
    multiplier = 1.35 if city in ["Mumbai", "Delhi", "Bangalore"] else 1.15 if city == "Kolkata" else 1.0
    
    price_info = get_hospital_price_level(hospital_name, city)
    final_multiplier = multiplier * price_info["multiplier"]

    consultation = (benchmark["consultation_min"] + benchmark["consultation_max"]) // 2
    tests_total = sum(benchmark["tests"].values()) // 2   # average tests cost
    medicines = benchmark["medicines_avg"]

    total_estimated = int((consultation + tests_total + medicines) * final_multiplier)

    return {
        "consultation": int(consultation * final_multiplier),
        "estimated_tests": int(tests_total * final_multiplier),
        "estimated_medicines": int(medicines * final_multiplier),
        "total_estimated": total_estimated,
        "price_adjustment_note": price_info["note"]
    }


def calculate_insurance(plan_type: str, total_inr: float) -> dict:
    plan = INSURANCE_PLANS.get(plan_type, INSURANCE_PLANS["no_insurance"])
    if plan["coverage_percent"] == 0:
        return {
            "plan": plan["plan_name"],
            "covered_inr": 0,
            "out_of_pocket_inr": round(total_inr, 2),
            "coverage_percent": 0
        }

    after_deductible = max(0, total_inr - plan["deductible_inr"])
    covered = min(after_deductible * (plan["coverage_percent"] / 100), plan["max_claim_inr"])
    out_of_pocket = total_inr - covered

    return {
        "plan": plan["plan_name"],
        "covered_inr": round(covered, 2),
        "out_of_pocket_inr": round(out_of_pocket, 2),
        "coverage_percent": plan["coverage_percent"]
    }


def convert_to_currency(amount_inr: float, target_currency: str) -> dict:
    rate = CURRENCY_RATES.get(target_currency.upper(), 83.8)
    return {
        "amount_inr": round(amount_inr, 2),
        "target_currency": target_currency.upper(),
        "converted_amount": round(amount_inr / rate, 2)
    }


# ── LLM Only for Friendly Summary ───────────────────────────────────────────
def generate_cost_summary(specialty: str, breakdown: dict, insurance: dict, 
                         home_currency: str, out_of_pocket_converted: float) -> dict:
    prompt = f"""
    Create a short, friendly cost summary for a tourist.

    Specialty: {specialty}
    Total Estimated Cost: ₹{breakdown['total_estimated']}
    Insurance Covered: ₹{insurance['covered_inr']}
    Out of Pocket: ₹{insurance['out_of_pocket_inr']} (~{home_currency} {out_of_pocket_converted})

    Write:
    1. One friendly cost_summary sentence
    2. 2-3 practical payment_tips for India
    """

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.content[0].text

        # Simple parsing (you can improve this)
        summary = text.split("\n")[0].strip()
        tips = [line.strip("- •") for line in text.split("\n") if line.strip().startswith(('-', '•'))]

        return {
            "cost_summary": summary or "This is an estimated cost for your consultation.",
            "payment_tips": tips[:3] or ["Carry cash or UPI", "Keep all receipts for insurance claims"]
        }
    except:
        return {
            "cost_summary": f"Estimated total cost for {specialty} consultation in {city} is around ₹{breakdown['total_estimated']}.",
            "payment_tips": ["Carry cash or UPI", "Keep receipts for reimbursement"]
        }


# ── Main Agent (Hybrid) ─────────────────────────────────────────────────────
class CostEstimatorAgent:
    def estimate(self, triage_result: dict, matched_provider: dict, tourist_info: dict) -> dict:
        specialty = triage_result.get("recommended_specialty", "General Physician")
        city = tourist_info.get("city", "Kolkata")
        hospital_name = matched_provider.get("hospital_name") or matched_provider.get("provider_name", "")
        home_currency = tourist_info.get("home_currency", "USD")
        insurance_plan = tourist_info.get("insurance_plan", "no_insurance")

        # Deterministic calculations
        breakdown = calculate_cost_breakdown(specialty, city, hospital_name)
        insurance = calculate_insurance(insurance_plan, breakdown["total_estimated"])
        currency_info = convert_to_currency(insurance["out_of_pocket_inr"], home_currency)

        # Light LLM call only for natural language part
        summary = generate_cost_summary(
            specialty, breakdown, insurance, home_currency, currency_info["converted_amount"]
        )

        return {
            "specialty": specialty,
            "cost_breakdown_inr": {
                "consultation": breakdown["consultation"],
                "estimated_tests": breakdown["estimated_tests"],
                "estimated_medicines": breakdown["estimated_medicines"],
                "total_estimated": breakdown["total_estimated"]
            },
            "insurance": insurance,
            f"out_of_pocket_{home_currency.lower()}": currency_info["converted_amount"],
            "payment_tips": summary["payment_tips"],
            "cost_summary": summary["cost_summary"],
            "disclaimer": "Costs are estimates only. Actual charges may vary based on tests and treatment."
        }


# Test
if __name__ == "__main__":
    agent = CostEstimatorAgent()
    result = agent.estimate(
        {"recommended_specialty": "General Physician"},
        {"hospital_name": "Apollo Gleneagles Hospital"},
        {"city": "Kolkata", "home_currency": "USD", "insurance_plan": "standard_tourist"}
    )
    print(json.dumps(result, indent=2))