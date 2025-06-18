#!/usr/bin/env python3
"""
Applicazione CLI per la gestione delle finanze personali
Personal Finance Management CLI Application
"""

import os
import sys
from datetime import datetime
from models import FinanceManager
from utils import clear_screen, format_currency, validate_amount, validate_date

class PersonalFinanceApp:
    def __init__(self):
        self.finance_manager = FinanceManager()
        
    def display_main_menu(self):
        """Visualizza il menu principale"""
        clear_screen()
        print("=" * 60)
        print("        🏦 GESTIONE FINANZE PERSONALI 🏦")
        print("=" * 60)
        print()
        print("Saldo attuale:", format_currency(self.finance_manager.get_balance()))
        print()
        print("📋 MENU PRINCIPALE:")
        print("1. 📥 Aggiungi Entrata")
        print("2. 📤 Aggiungi Spesa")
        print("3. 💰 Visualizza Saldo")
        print("4. 🗂️  Gestisci Categorie")
        print("5. 📆 Gestisci Budget Mensile")
        print("6. 📊 Report Mensile")
        print("7. 📋 Visualizza Transazioni")
        print("8. ⚙️  Impostazioni")
        print("0. 🚪 Esci")
        print()
        
    def add_income(self):
        """Aggiungi una nuova entrata"""
        clear_screen()
        print("📥 AGGIUNGI ENTRATA")
        print("-" * 30)
        
        try:
            descrizione = input("Descrizione (es: Stipendio, Regalo): ").strip()
            if not descrizione:
                print("❌ La descrizione è obbligatoria!")
                input("Premi INVIO per continuare...")
                return
                
            while True:
                importo_str = input("Importo (€): ").strip()
                importo = validate_amount(importo_str)
                if importo is not None:
                    break
                print("❌ Inserisci un importo valido!")
                
            while True:
                data_str = input("Data (YYYY-MM-DD) o premi INVIO per oggi: ").strip()
                if not data_str:
                    data = datetime.now().strftime("%Y-%m-%d")
                    break
                if validate_date(data_str):
                    data = data_str
                    break
                print("❌ Formato data non valido! Usa YYYY-MM-DD")
                
            self.finance_manager.add_income(descrizione, importo, data)
            print(f"✅ Entrata di {format_currency(importo)} aggiunta con successo!")
            
        except KeyboardInterrupt:
            print("\n❌ Operazione annullata.")
        except Exception as e:
            print(f"❌ Errore: {e}")
            
        input("Premi INVIO per continuare...")
        
    def add_expense(self):
        """Aggiungi una nuova spesa"""
        clear_screen()
        print("📤 AGGIUNGI SPESA")
        print("-" * 30)
        
        try:
            descrizione = input("Descrizione (es: Spesa, Affitto): ").strip()
            if not descrizione:
                print("❌ La descrizione è obbligatoria!")
                input("Premi INVIO per continuare...")
                return
                
            while True:
                importo_str = input("Importo (€): ").strip()
                importo = validate_amount(importo_str)
                if importo is not None:
                    break
                print("❌ Inserisci un importo valido!")
                
            # Mostra categorie disponibili
            categorie = self.finance_manager.get_categories()
            if categorie:
                print("\nCategorie disponibili:")
                for i, cat in enumerate(categorie, 1):
                    print(f"{i}. {cat}")
                print(f"{len(categorie) + 1}. Aggiungi nuova categoria")
                
                while True:
                    try:
                        scelta = int(input("Seleziona categoria (numero): "))
                        if 1 <= scelta <= len(categorie):
                            categoria = categorie[scelta - 1]
                            break
                        elif scelta == len(categorie) + 1:
                            categoria = input("Nome nuova categoria: ").strip()
                            if categoria:
                                self.finance_manager.add_category(categoria)
                                break
                            else:
                                print("❌ Nome categoria non valido!")
                        else:
                            print("❌ Selezione non valida!")
                    except ValueError:
                        print("❌ Inserisci un numero valido!")
            else:
                categoria = input("Categoria: ").strip()
                if categoria:
                    self.finance_manager.add_category(categoria)
                else:
                    categoria = "Generale"
                    
            while True:
                data_str = input("Data (YYYY-MM-DD) o premi INVIO per oggi: ").strip()
                if not data_str:
                    data = datetime.now().strftime("%Y-%m-%d")
                    break
                if validate_date(data_str):
                    data = data_str
                    break
                print("❌ Formato data non valido! Usa YYYY-MM-DD")
                
            self.finance_manager.add_expense(descrizione, importo, data, categoria)
            print(f"✅ Spesa di {format_currency(importo)} aggiunta con successo!")
            
        except KeyboardInterrupt:
            print("\n❌ Operazione annullata.")
        except Exception as e:
            print(f"❌ Errore: {e}")
            
        input("Premi INVIO per continuare...")
        
    def view_balance(self):
        """Visualizza il saldo dettagliato"""
        clear_screen()
        print("💰 SALDO DETTAGLIATO")
        print("-" * 40)
        
        entrate_totali = self.finance_manager.get_total_income()
        spese_totali = self.finance_manager.get_total_expenses()
        saldo = self.finance_manager.get_balance()
        
        print(f"📥 Entrate totali:  {format_currency(entrate_totali)}")
        print(f"📤 Spese totali:    {format_currency(spese_totali)}")
        print("-" * 40)
        if saldo >= 0:
            print(f"💰 Saldo attuale:   {format_currency(saldo)} ✅")
        else:
            print(f"💰 Saldo attuale:   {format_currency(saldo)} ⚠️")
            
        print()
        input("Premi INVIO per continuare...")
        
    def manage_categories(self):
        """Gestisci le categorie"""
        while True:
            clear_screen()
            print("🗂️  GESTIONE CATEGORIE")
            print("-" * 30)
            
            categorie = self.finance_manager.get_categories()
            if categorie:
                print("Categorie esistenti:")
                for i, cat in enumerate(categorie, 1):
                    print(f"{i}. {cat}")
            else:
                print("Nessuna categoria presente.")
                
            print("\nOpzioni:")
            print("1. Aggiungi categoria")
            print("2. Rimuovi categoria")
            print("0. Torna al menu principale")
            
            scelta = input("\nScelta: ").strip()
            
            if scelta == "1":
                nome = input("Nome nuova categoria: ").strip()
                if nome:
                    if self.finance_manager.add_category(nome):
                        print(f"✅ Categoria '{nome}' aggiunta!")
                    else:
                        print(f"❌ Categoria '{nome}' già esistente!")
                else:
                    print("❌ Nome categoria non valido!")
                input("Premi INVIO per continuare...")
                
            elif scelta == "2":
                if not categorie:
                    print("❌ Nessuna categoria da rimuovere!")
                    input("Premi INVIO per continuare...")
                    continue
                    
                try:
                    num = int(input("Numero categoria da rimuovere: "))
                    if 1 <= num <= len(categorie):
                        cat_da_rimuovere = categorie[num - 1]
                        conferma = input(f"Confermi rimozione di '{cat_da_rimuovere}'? (s/n): ")
                        if conferma.lower() == 's':
                            self.finance_manager.remove_category(cat_da_rimuovere)
                            print(f"✅ Categoria '{cat_da_rimuovere}' rimossa!")
                    else:
                        print("❌ Numero non valido!")
                except ValueError:
                    print("❌ Inserisci un numero valido!")
                input("Premi INVIO per continuare...")
                
            elif scelta == "0":
                break
            else:
                print("❌ Scelta non valida!")
                input("Premi INVIO per continuare...")
                
    def manage_budget(self):
        """Gestisci il budget mensile"""
        while True:
            clear_screen()
            print("📆 GESTIONE BUDGET MENSILE")
            print("-" * 35)
            
            budget_attuale = self.finance_manager.get_monthly_budget()
            mese_corrente = datetime.now().strftime("%Y-%m")
            spese_mese = self.finance_manager.get_monthly_expenses(mese_corrente)
            
            if budget_attuale > 0:
                print(f"Budget mensile impostato: {format_currency(budget_attuale)}")
                print(f"Speso questo mese ({mese_corrente}): {format_currency(spese_mese)}")
                rimanente = budget_attuale - spese_mese
                if rimanente >= 0:
                    print(f"Rimanente: {format_currency(rimanente)} ✅")
                else:
                    print(f"Sforamento: {format_currency(abs(rimanente))} ⚠️")
            else:
                print("Nessun budget mensile impostato.")
                
            print("\nOpzioni:")
            print("1. Imposta/Modifica budget mensile")
            print("2. Rimuovi budget mensile")
            print("0. Torna al menu principale")
            
            scelta = input("\nScelta: ").strip()
            
            if scelta == "1":
                while True:
                    budget_str = input("Nuovo budget mensile (€): ").strip()
                    budget = validate_amount(budget_str)
                    if budget is not None and budget > 0:
                        self.finance_manager.set_monthly_budget(budget)
                        print(f"✅ Budget mensile impostato a {format_currency(budget)}!")
                        break
                    print("❌ Inserisci un importo valido maggiore di 0!")
                input("Premi INVIO per continuare...")
                
            elif scelta == "2":
                if budget_attuale > 0:
                    conferma = input("Confermi rimozione del budget mensile? (s/n): ")
                    if conferma.lower() == 's':
                        self.finance_manager.set_monthly_budget(0)
                        print("✅ Budget mensile rimosso!")
                else:
                    print("❌ Nessun budget da rimuovere!")
                input("Premi INVIO per continuare...")
                
            elif scelta == "0":
                break
            else:
                print("❌ Scelta non valida!")
                input("Premi INVIO per continuare...")
                
    def monthly_report(self):
        """Genera report mensile"""
        clear_screen()
        print("📊 REPORT MENSILE")
        print("-" * 25)
        
        # Chiedi il mese per il report
        mese_corrente = datetime.now().strftime("%Y-%m")
        mese = input(f"Mese per il report (YYYY-MM) o INVIO per corrente ({mese_corrente}): ").strip()
        
        if not mese:
            mese = mese_corrente
        elif not validate_date(f"{mese}-01"):
            print("❌ Formato mese non valido!")
            input("Premi INVIO per continuare...")
            return
            
        report = self.finance_manager.get_monthly_report(mese)
        
        print(f"\n📊 REPORT PER {mese}")
        print("=" * 50)
        print(f"📥 Entrate totali:    {format_currency(report['entrate_totali'])}")
        print(f"📤 Spese totali:      {format_currency(report['spese_totali'])}")
        print(f"💰 Saldo del mese:    {format_currency(report['saldo'])}")
        
        budget = self.finance_manager.get_monthly_budget()
        if budget > 0:
            print(f"📆 Budget mensile:    {format_currency(budget)}")
            rimanente = budget - report['spese_totali']
            if rimanente >= 0:
                print(f"💵 Rimanente budget:  {format_currency(rimanente)} ✅")
            else:
                print(f"⚠️  Sforamento budget: {format_currency(abs(rimanente))}")
                
        print("\n📋 SPESE PER CATEGORIA:")
        print("-" * 30)
        if report['spese_per_categoria']:
            for categoria, importo in report['spese_per_categoria'].items():
                percentuale = (importo / report['spese_totali'] * 100) if report['spese_totali'] > 0 else 0
                print(f"{categoria}: {format_currency(importo)} ({percentuale:.1f}%)")
        else:
            print("Nessuna spesa registrata per questo mese.")
            
        print()
        input("Premi INVIO per continuare...")
        
    def view_transactions(self):
        """Visualizza tutte le transazioni"""
        clear_screen()
        print("📋 TRANSAZIONI")
        print("-" * 25)
        
        transazioni = self.finance_manager.get_all_transactions()
        
        if not transazioni:
            print("Nessuna transazione presente.")
        else:
            print(f"Totale transazioni: {len(transazioni)}")
            print("-" * 60)
            
            for trans in transazioni[-20:]:  # Mostra le ultime 20
                tipo_icon = "📥" if trans['tipo'] == 'entrata' else "📤"
                categoria_str = f" [{trans['categoria']}]" if trans['tipo'] == 'spesa' else ""
                print(f"{tipo_icon} {trans['data']} | {trans['descrizione']}{categoria_str}")
                print(f"    {format_currency(trans['importo'])}")
                print()
                
        input("Premi INVIO per continuare...")
        
    def settings(self):
        """Impostazioni applicazione"""
        while True:
            clear_screen()
            print("⚙️  IMPOSTAZIONI")
            print("-" * 20)
            
            print("1. Esporta dati")
            print("2. Importa dati")
            print("3. Reset completo (ATTENZIONE)")
            print("0. Torna al menu principale")
            
            scelta = input("\nScelta: ").strip()
            
            if scelta == "1":
                filename = input("Nome file per esportazione (senza .json): ").strip()
                if not filename:
                    filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    
                if self.finance_manager.export_data(f"{filename}.json"):
                    print(f"✅ Dati esportati in {filename}.json")
                else:
                    print("❌ Errore durante l'esportazione!")
                input("Premi INVIO per continuare...")
                
            elif scelta == "2":
                filename = input("Nome file da importare: ").strip()
                if filename and os.path.exists(filename):
                    conferma = input("ATTENZIONE: Questo sovrascriverà tutti i dati attuali. Continuare? (s/n): ")
                    if conferma.lower() == 's':
                        if self.finance_manager.import_data(filename):
                            print("✅ Dati importati con successo!")
                        else:
                            print("❌ Errore durante l'importazione!")
                else:
                    print("❌ File non trovato!")
                input("Premi INVIO per continuare...")
                
            elif scelta == "3":
                print("⚠️  RESET COMPLETO - QUESTA OPERAZIONE È IRREVERSIBILE!")
                conferma1 = input("Digitare 'RESET' per confermare: ").strip()
                if conferma1 == "RESET":
                    conferma2 = input("Sei sicuro? Digitare 'SI' per confermare: ").strip()
                    if conferma2 == "SI":
                        self.finance_manager.reset_all_data()
                        print("✅ Tutti i dati sono stati cancellati!")
                    else:
                        print("❌ Reset annullato.")
                else:
                    print("❌ Reset annullato.")
                input("Premi INVIO per continuare...")
                
            elif scelta == "0":
                break
            else:
                print("❌ Scelta non valida!")
                input("Premi INVIO per continuare...")
    
    def run(self):
        """Esegui l'applicazione principale"""
        print("🏦 Caricamento Gestione Finanze Personali...")
        
        # Carica i dati all'avvio
        if not self.finance_manager.load_data():
            print("⚠️  Impossibile caricare i dati, iniziando con dati vuoti.")
            
        while True:
            try:
                self.display_main_menu()
                scelta = input("Inserisci la tua scelta: ").strip()
                
                if scelta == "1":
                    self.add_income()
                elif scelta == "2":
                    self.add_expense()
                elif scelta == "3":
                    self.view_balance()
                elif scelta == "4":
                    self.manage_categories()
                elif scelta == "5":
                    self.manage_budget()
                elif scelta == "6":
                    self.monthly_report()
                elif scelta == "7":
                    self.view_transactions()
                elif scelta == "8":
                    self.settings()
                elif scelta == "0":
                    print("\n👋 Arrivederci! I tuoi dati sono stati salvati automaticamente.")
                    break
                else:
                    print("❌ Scelta non valida! Premi INVIO per continuare...")
                    input()
                    
            except KeyboardInterrupt:
                print("\n\n👋 Applicazione interrotta. Arrivederci!")
                break
            except Exception as e:
                print(f"\n❌ Errore imprevisto: {e}")
                print("L'applicazione continuerà a funzionare...")
                input("Premi INVIO per continuare...")

if __name__ == "__main__":
    app = PersonalFinanceApp()
    app.run()
