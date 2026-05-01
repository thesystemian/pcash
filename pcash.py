#!/usr/bin/env python3
import json
import os
from datetime import datetime
from pathlib import Path

EUR_TO_MUR = 54.18
DATA_FILE = Path.home() / ".pcash_data.json"
CATEGORIES_FILE = Path.home() / ".pcash_categories.json"

class PCashAgent:
    def __init__(self):
        self.expenses = self.load_expenses()
        self.categories = self.load_categories()
    
    def load_expenses(self):
        if DATA_FILE.exists():
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return []
    
    def load_categories(self):
        if CATEGORIES_FILE.exists():
            with open(CATEGORIES_FILE, 'r') as f:
                return json.load(f)
        return ["tabac", "fume", "snack", "course", "biere", "transport", "pharmacie", "resto", "autre"]
    
    def save_expenses(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self.expenses, f, indent=2)
    
    def save_categories(self):
        with open(CATEGORIES_FILE, 'w') as f:
            json.dump(self.categories, f, indent=2)
    
    def add_expense(self, amount: int, category: str):
        if amount <= 0:
            return {"success": False, "error": "Montant > 0"}
        if category not in self.categories:
            return {"success": False, "error": f"Cat '{category}' n'existe pas"}
        
        expense = {"amount": amount, "category": category, "date": datetime.now().isoformat()}
        self.expenses.append(expense)
        self.save_expenses()
        return {"success": True, "message": f"✅ {amount} ₨ ({category})", "total_mur": self.get_total_mur(), "total_eur": self.get_total_eur()}
    
    def get_total_mur(self):
        return sum(e["amount"] for e in self.expenses)
    
    def get_total_eur(self):
        return round(self.get_total_mur() / EUR_TO_MUR, 2)
    
    def list_expenses(self, limit=5):
        recent = self.expenses[-limit:] if self.expenses else []
        return [{"category": e["category"], "amount": e["amount"], "date": datetime.fromisoformat(e["date"]).strftime("%d/%m %H:%M"), "eur": round(e["amount"] / EUR_TO_MUR, 2)} for e in recent]
    
    def display_dashboard(self):
        print("\n" + "="*50)
        print("P•CASH — Expense Tracker")
        print("="*50)
        print(f"\n💰 TOTALS: {self.get_total_mur()} ₨ / {self.get_total_eur()} €")
        if self.expenses:
            print(f"\n📝 DÉPENSES RÉCENTES:")
            for i, exp in enumerate(self.list_expenses(5)):
                print(f"   [{i}] {exp['category']:12} → {exp['amount']:4} ₨ ({exp['eur']} €) — {exp['date']}")
        else:
            print(f"\n📝 Panier vide")
        print(f"\n📂 CATÉGORIES: {', '.join(self.categories)}")
        print("="*50)
    
    def run_interactive(self):
        self.display_dashboard()
        while True:
            print("\n> ", end="")
            cmd = input().strip()
            if not cmd: continue
            parts = cmd.split()
            action = parts[0].lower()
            
            if action == "add" and len(parts) >= 3:
                try:
                    amount = int(parts[1])
                    category = parts[2]
                    result = self.add_expense(amount, category)
                    print(f"   {result['message']} — Total: {result['total_mur']} ₨ / {result['total_eur']} €")
                except: print("   ❌ Erreur")
            elif action == "quit": break
            else: self.display_dashboard()

if __name__ == "__main__":
    agent = PCashAgent()
    agent.run_interactive()
