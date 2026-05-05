"""
Personal Finance Tracker - Correction complète
ScrumBan Exercise - 3 Sprints
"""

import json
import os
from datetime import datetime

# ─────────────────────────────────────────────
# SPRINT 1 : Income Tracker + Expense Tracker
# ─────────────────────────────────────────────

DATA_FILE = "data.json"

# Structure de données en mémoire
data = {
    "income": [],       # [{"amount": float, "description": str, "date": str}]
    "expenses": [],     # [{"amount": float, "category": str, "description": str, "date": str}]
    "budgets": {}       # {"Food": float, "Rent": float, ...}
}

CATEGORIES = ["Food", "Rent", "Utilities", "Transport", "Other"]


# ─────────────────────────────────────────────
# SPRINT 2 : Data Persistence
# ─────────────────────────────────────────────

def load_data():
    """Charge les données depuis data.json si le fichier existe."""
    global data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        print("✓ Data loaded from", DATA_FILE)
    else:
        print("ℹ No existing data found. Starting fresh.")


def save_data():
    """Sauvegarde les données dans data.json."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print("✓ Data saved to", DATA_FILE)


# ─────────────────────────────────────────────
# SPRINT 1 : User Story 1 — Income Tracker
# ─────────────────────────────────────────────

def add_income(amount: float, description: str):
    """Ajoute un revenu à la liste."""
    entry = {
        "amount": amount,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    data["income"].append(entry)
    print(f"  ✓ Income added: +€{amount:.2f} ({description})")


def show_income():
    """Affiche tous les revenus enregistrés."""
    if not data["income"]:
        print("  No income recorded yet.")
        return
    print("\n  ── Income ──────────────────────")
    for entry in data["income"]:
        print(f"  {entry['date']}  +€{entry['amount']:>8.2f}  {entry['description']}")
    print(f"  {'TOTAL':>22}  €{sum(e['amount'] for e in data['income']):.2f}")


# ─────────────────────────────────────────────
# SPRINT 1 : User Story 2 — Expense Tracker
# ─────────────────────────────────────────────

def add_expense(amount: float, category: str, description: str):
    """Ajoute une dépense à la liste."""
    if category not in CATEGORIES:
        print(f"  ✗ Invalid category. Choose from: {', '.join(CATEGORIES)}")
        return
    entry = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    data["expenses"].append(entry)
    print(f"  ✓ Expense added: -€{amount:.2f} [{category}] ({description})")

    # Sprint 3 : vérification budget
    check_budget(category)


def show_expenses():
    """Affiche toutes les dépenses par catégorie."""
    if not data["expenses"]:
        print("  No expenses recorded yet.")
        return
    print("\n  ── Expenses ────────────────────")
    for cat in CATEGORIES:
        entries = [e for e in data["expenses"] if e["category"] == cat]
        if entries:
            print(f"\n  [{cat}]")
            for entry in entries:
                print(f"  {entry['date']}  -€{entry['amount']:>8.2f}  {entry['description']}")
    print(f"\n  {'TOTAL':>22}  €{sum(e['amount'] for e in data['expenses']):.2f}")


# ─────────────────────────────────────────────
# SPRINT 2 : User Story — Financial Summary
# ─────────────────────────────────────────────

def show_summary():
    """Affiche le résumé financier du mois."""
    total_income = sum(e["amount"] for e in data["income"])
    total_expenses = sum(e["amount"] for e in data["expenses"])
    savings = total_income - total_expenses

    print("\n  ┌─────────────────────────────────┐")
    print("  │       Financial Summary          │")
    print("  ├─────────────────────────────────┤")
    print(f"  │  Total Income   : +€{total_income:>10.2f}  │")
    print(f"  │  Total Expenses :  €{total_expenses:>10.2f}  │")
    print("  ├─────────────────────────────────┤")
    status = "✓ POSITIVE" if savings >= 0 else "✗ NEGATIVE"
    print(f"  │  Balance        :  €{savings:>10.2f}  │")
    print(f"  │  Status         :  {status:<13}  │")
    print("  └─────────────────────────────────┘")


# ─────────────────────────────────────────────
# SPRINT 3 : User Story — Budget Planner
# ─────────────────────────────────────────────

def set_budget(category: str, amount: float):
    """Définit un budget mensuel pour une catégorie."""
    if category not in CATEGORIES:
        print(f"  ✗ Invalid category. Choose from: {', '.join(CATEGORIES)}")
        return
    data["budgets"][category] = amount
    print(f"  ✓ Budget set for {category}: €{amount:.2f}/month")


def check_budget(category: str):
    """Vérifie si les dépenses dépassent le budget d'une catégorie."""
    if category not in data["budgets"]:
        return
    spent = sum(e["amount"] for e in data["expenses"] if e["category"] == category)
    budget = data["budgets"][category]
    if spent > budget:
        print(f"  ⚠ WARNING: {category} budget exceeded! Spent €{spent:.2f} / Budget €{budget:.2f}")
    elif spent > budget * 0.8:
        print(f"  ⚠ ALERT: {category} at {spent/budget*100:.0f}% of budget (€{spent:.2f}/€{budget:.2f})")


def show_budgets():
    """Affiche tous les budgets et leur consommation."""
    if not data["budgets"]:
        print("  No budgets set yet.")
        return
    print("\n  ── Budget Overview ─────────────")
    for cat, budget in data["budgets"].items():
        spent = sum(e["amount"] for e in data["expenses"] if e["category"] == cat)
        pct = (spent / budget * 100) if budget > 0 else 0
        bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
        status = "✓" if spent <= budget else "✗"
        print(f"  {status} {cat:<12} [{bar}] {pct:>5.1f}%  €{spent:.2f}/€{budget:.2f}")


# ─────────────────────────────────────────────
# SPRINT 3 : User Story — Savings Tracker
# ─────────────────────────────────────────────

def show_savings():
    """Affiche les économies du mois."""
    total_income = sum(e["amount"] for e in data["income"])
    total_expenses = sum(e["amount"] for e in data["expenses"])
    savings = total_income - total_expenses
    savings_rate = (savings / total_income * 100) if total_income > 0 else 0

    print("\n  ── Savings Tracker ─────────────")
    print(f"  Monthly Savings  : €{savings:.2f}")
    print(f"  Savings Rate     : {savings_rate:.1f}%")

    if savings_rate >= 20:
        print("  Status: ★ Excellent! Keep it up.")
    elif savings_rate >= 10:
        print("  Status: ✓ Good. Try to reach 20%.")
    elif savings_rate >= 0:
        print("  Status: ⚠ Low savings. Review expenses.")
    else:
        print("  Status: ✗ You're spending more than you earn!")


# ─────────────────────────────────────────────
# MENU PRINCIPAL (CLI)
# ─────────────────────────────────────────────

def print_menu():
    print("\n  ╔══════════════════════════════════╗")
    print("  ║   Personal Finance Tracker       ║")
    print("  ╠══════════════════════════════════╣")
    print("  ║  1. Add income                   ║")
    print("  ║  2. Add expense                  ║")
    print("  ║  3. Set budget                   ║")
    print("  ║  4. Show income                  ║")
    print("  ║  5. Show expenses                ║")
    print("  ║  6. Show budgets                 ║")
    print("  ║  7. Show savings                 ║")
    print("  ║  8. Financial summary            ║")
    print("  ║  0. Save & Exit                  ║")
    print("  ╚══════════════════════════════════╝")
    print("  Choice: ", end="")


def get_float(prompt: str) -> float:
    """Helper pour lire un float avec validation."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  ✗ Please enter a valid number.")


def run():
    """Boucle principale de l'application."""
    load_data()

    while True:
        print_menu()
        choice = input().strip()

        if choice == "1":
            amount = get_float("  Amount (€): ")
            desc = input("  Description: ").strip()
            add_income(amount, desc)

        elif choice == "2":
            amount = get_float("  Amount (€): ")
            print(f"  Categories: {', '.join(CATEGORIES)}")
            cat = input("  Category: ").strip().capitalize()
            desc = input("  Description: ").strip()
            add_expense(amount, cat, desc)

        elif choice == "3":
            print(f"  Categories: {', '.join(CATEGORIES)}")
            cat = input("  Category: ").strip().capitalize()
            amount = get_float("  Monthly budget (€): ")
            set_budget(cat, amount)

        elif choice == "4":
            show_income()

        elif choice == "5":
            show_expenses()

        elif choice == "6":
            show_budgets()

        elif choice == "7":
            show_savings()

        elif choice == "8":
            show_summary()

        elif choice == "0":
            save_data()
            print("  Goodbye!")
            break

        else:
            print("  ✗ Invalid choice. Please try again.")


if __name__ == "__main__":
    run()
