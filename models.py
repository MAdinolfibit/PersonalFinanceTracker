"""
Modelli dati per l'applicazione di gestione finanze personali
Data models for personal finance management application
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

class FinanceManager:
    def __init__(self, data_file: str = "data.json"):
        self.data_file = data_file
        self.data = {
            "entrate": [],
            "spese": [],
            "categorie": ["Cibo", "Casa", "Trasporti", "Salute", "Intrattenimento", "Abbigliamento", "Altro"],
            "budget_mensile": 0.0,
            "impostazioni": {
                "valuta": "EUR",
                "formato_data": "%Y-%m-%d"
            }
        }
        
    def load_data(self) -> bool:
        """Carica i dati dal file JSON"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    
                # Merge dei dati mantenendo la struttura di default
                for key in self.data:
                    if key in loaded_data:
                        self.data[key] = loaded_data[key]
                        
                return True
            else:
                # Se il file non esiste, salva la struttura di default
                return self.save_data()
        except Exception as e:
            print(f"Errore durante il caricamento dei dati: {e}")
            return False
            
    def save_data(self) -> bool:
        """Salva i dati nel file JSON"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Errore durante il salvataggio dei dati: {e}")
            return False
            
    def add_income(self, descrizione: str, importo: float, data: str) -> bool:
        """Aggiungi una nuova entrata"""
        try:
            entrata = {
                "id": self._generate_id(),
                "descrizione": descrizione,
                "importo": round(importo, 2),
                "data": data,
                "tipo": "entrata",
                "timestamp": datetime.now().isoformat()
            }
            
            self.data["entrate"].append(entrata)
            return self.save_data()
        except Exception as e:
            print(f"Errore durante l'aggiunta dell'entrata: {e}")
            return False
            
    def add_expense(self, descrizione: str, importo: float, data: str, categoria: str) -> bool:
        """Aggiungi una nuova spesa"""
        try:
            # Assicurati che la categoria esista
            if categoria not in self.data["categorie"]:
                self.data["categorie"].append(categoria)
                
            spesa = {
                "id": self._generate_id(),
                "descrizione": descrizione,
                "importo": round(importo, 2),
                "data": data,
                "categoria": categoria,
                "tipo": "spesa",
                "timestamp": datetime.now().isoformat()
            }
            
            self.data["spese"].append(spesa)
            return self.save_data()
        except Exception as e:
            print(f"Errore durante l'aggiunta della spesa: {e}")
            return False
            
    def get_total_income(self) -> float:
        """Calcola il totale delle entrate"""
        return sum(entrata["importo"] for entrata in self.data["entrate"])
        
    def get_total_expenses(self) -> float:
        """Calcola il totale delle spese"""
        return sum(spesa["importo"] for spesa in self.data["spese"])
        
    def get_balance(self) -> float:
        """Calcola il saldo attuale"""
        return round(self.get_total_income() - self.get_total_expenses(), 2)
        
    def get_categories(self) -> List[str]:
        """Ottieni la lista delle categorie"""
        return self.data["categorie"].copy()
        
    def add_category(self, categoria: str) -> bool:
        """Aggiungi una nuova categoria"""
        categoria = categoria.strip()
        if categoria and categoria not in self.data["categorie"]:
            self.data["categorie"].append(categoria)
            return self.save_data()
        return False
        
    def remove_category(self, categoria: str) -> bool:
        """Rimuovi una categoria (le spese esistenti mantengono la categoria)"""
        if categoria in self.data["categorie"]:
            self.data["categorie"].remove(categoria)
            return self.save_data()
        return False
        
    def get_monthly_budget(self) -> float:
        """Ottieni il budget mensile"""
        return self.data["budget_mensile"]
        
    def set_monthly_budget(self, budget: float) -> bool:
        """Imposta il budget mensile"""
        try:
            self.data["budget_mensile"] = round(budget, 2)
            return self.save_data()
        except Exception as e:
            print(f"Errore durante l'impostazione del budget: {e}")
            return False
            
    def get_monthly_expenses(self, mese: str) -> float:
        """Calcola le spese per un mese specifico (formato YYYY-MM)"""
        spese_mese = [
            spesa for spesa in self.data["spese"]
            if spesa["data"].startswith(mese)
        ]
        return sum(spesa["importo"] for spesa in spese_mese)
        
    def get_monthly_income(self, mese: str) -> float:
        """Calcola le entrate per un mese specifico (formato YYYY-MM)"""
        entrate_mese = [
            entrata for entrata in self.data["entrate"]
            if entrata["data"].startswith(mese)
        ]
        return sum(entrata["importo"] for entrata in entrate_mese)
        
    def get_monthly_report(self, mese: str) -> Dict[str, Any]:
        """Genera un report mensile completo"""
        spese_mese = [
            spesa for spesa in self.data["spese"]
            if spesa["data"].startswith(mese)
        ]
        
        entrate_mese = [
            entrata for entrata in self.data["entrate"]
            if entrata["data"].startswith(mese)
        ]
        
        # Calcola spese per categoria
        spese_per_categoria = {}
        for spesa in spese_mese:
            categoria = spesa["categoria"]
            if categoria not in spese_per_categoria:
                spese_per_categoria[categoria] = 0
            spese_per_categoria[categoria] += spesa["importo"]
            
        # Ordina le categorie per importo decrescente
        spese_per_categoria = dict(
            sorted(spese_per_categoria.items(), key=lambda x: x[1], reverse=True)
        )
        
        entrate_totali = sum(entrata["importo"] for entrata in entrate_mese)
        spese_totali = sum(spesa["importo"] for spesa in spese_mese)
        
        return {
            "mese": mese,
            "entrate_totali": round(entrate_totali, 2),
            "spese_totali": round(spese_totali, 2),
            "saldo": round(entrate_totali - spese_totali, 2),
            "spese_per_categoria": spese_per_categoria,
            "numero_transazioni": len(spese_mese) + len(entrate_mese),
            "budget_mensile": self.data["budget_mensile"]
        }
        
    def get_all_transactions(self) -> List[Dict[str, Any]]:
        """Ottieni tutte le transazioni ordinate per data"""
        tutte_transazioni = []
        
        # Aggiungi entrate
        for entrata in self.data["entrate"]:
            tutte_transazioni.append({
                **entrata,
                "categoria": None  # Le entrate non hanno categoria
            })
            
        # Aggiungi spese
        for spesa in self.data["spese"]:
            tutte_transazioni.append(spesa)
            
        # Ordina per data (più recenti prima)
        tutte_transazioni.sort(key=lambda x: x["data"], reverse=True)
        
        return tutte_transazioni
        
    def export_data(self, filename: str) -> bool:
        """Esporta i dati in un file"""
        try:
            export_data = {
                **self.data,
                "export_info": {
                    "data_export": datetime.now().isoformat(),
                    "versione": "1.0"
                }
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Errore durante l'esportazione: {e}")
            return False
            
    def import_data(self, filename: str) -> bool:
        """Importa i dati da un file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
                
            # Valida i dati importati
            required_keys = ["entrate", "spese", "categorie"]
            for key in required_keys:
                if key not in imported_data:
                    print(f"File non valido: manca la chiave '{key}'")
                    return False
                    
            # Importa i dati mantenendo la struttura
            self.data = {
                "entrate": imported_data.get("entrate", []),
                "spese": imported_data.get("spese", []),
                "categorie": imported_data.get("categorie", self.data["categorie"]),
                "budget_mensile": imported_data.get("budget_mensile", 0.0),
                "impostazioni": imported_data.get("impostazioni", self.data["impostazioni"])
            }
            
            return self.save_data()
        except Exception as e:
            print(f"Errore durante l'importazione: {e}")
            return False
            
    def reset_all_data(self) -> bool:
        """Reset completo di tutti i dati"""
        try:
            self.data = {
                "entrate": [],
                "spese": [],
                "categorie": ["Cibo", "Casa", "Trasporti", "Salute", "Intrattenimento", "Abbigliamento", "Altro"],
                "budget_mensile": 0.0,
                "impostazioni": {
                    "valuta": "EUR",
                    "formato_data": "%Y-%m-%d"
                }
            }
            return self.save_data()
        except Exception as e:
            print(f"Errore durante il reset: {e}")
            return False
            
    def get_statistics(self) -> Dict[str, Any]:
        """Ottieni statistiche generali"""
        return {
            "totale_entrate": len(self.data["entrate"]),
            "totale_spese": len(self.data["spese"]),
            "totale_categorie": len(self.data["categorie"]),
            "importo_entrate": self.get_total_income(),
            "importo_spese": self.get_total_expenses(),
            "saldo": self.get_balance(),
            "budget_mensile": self.data["budget_mensile"]
        }
        
    def _generate_id(self) -> str:
        """Genera un ID univoco per le transazioni"""
        timestamp = datetime.now().isoformat()
        return f"{timestamp}_{len(self.data['entrate']) + len(self.data['spese'])}"
        
    def search_transactions(self, query: str) -> List[Dict[str, Any]]:
        """Cerca transazioni per descrizione"""
        query = query.lower().strip()
        risultati = []
        
        for entrata in self.data["entrate"]:
            if query in entrata["descrizione"].lower():
                risultati.append({**entrata, "categoria": None})
                
        for spesa in self.data["spese"]:
            if query in spesa["descrizione"].lower() or query in spesa["categoria"].lower():
                risultati.append(spesa)
                
        return sorted(risultati, key=lambda x: x["data"], reverse=True)
