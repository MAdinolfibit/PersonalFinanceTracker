"""
Funzioni di utilità per l'applicazione di gestione finanze personali
Utility functions for personal finance management application
"""

import os
import sys
from datetime import datetime
from typing import Optional

def clear_screen():
    """Pulisce lo schermo del terminale"""
    os.system('cls' if os.name == 'nt' else 'clear')

def format_currency(amount: float, currency: str = "€") -> str:
    """Formatta un importo come valuta"""
    return f"{amount:,.2f} {currency}".replace(",", ".")

def validate_amount(amount_str: str) -> Optional[float]:
    """Valida e converte un importo in float"""
    try:
        # Sostituisce virgola con punto per il parsing
        amount_str = amount_str.replace(",", ".")
        amount = float(amount_str)
        
        if amount < 0:
            print("❌ L'importo non può essere negativo!")
            return None
        if amount > 999999999:
            print("❌ L'importo è troppo grande!")
            return None
            
        return round(amount, 2)
    except ValueError:
        return None

def validate_date(date_str: str) -> bool:
    """Valida una data nel formato YYYY-MM-DD"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def format_date(date_str: str, format_in: str = "%Y-%m-%d", format_out: str = "%d/%m/%Y") -> str:
    """Converte una data da un formato all'altro"""
    try:
        date_obj = datetime.strptime(date_str, format_in)
        return date_obj.strftime(format_out)
    except ValueError:
        return date_str

def get_month_name(month_str: str) -> str:
    """Converte YYYY-MM in nome del mese"""
    month_names = {
        "01": "Gennaio", "02": "Febbraio", "03": "Marzo", "04": "Aprile",
        "05": "Maggio", "06": "Giugno", "07": "Luglio", "08": "Agosto",
        "09": "Settembre", "10": "Ottobre", "11": "Novembre", "12": "Dicembre"
    }
    
    try:
        year, month = month_str.split("-")
        return f"{month_names.get(month, month)} {year}"
    except (ValueError, KeyError):
        return month_str

def calculate_percentage(part: float, total: float) -> float:
    """Calcola la percentuale"""
    if total == 0:
        return 0.0
    return round((part / total) * 100, 1)

def format_percentage(percentage: float) -> str:
    """Formatta una percentuale"""
    return f"{percentage:.1f}%"

def get_current_month() -> str:
    """Ottieni il mese corrente nel formato YYYY-MM"""
    return datetime.now().strftime("%Y-%m")

def get_current_date() -> str:
    """Ottieni la data corrente nel formato YYYY-MM-DD"""
    return datetime.now().strftime("%Y-%m-%d")

def validate_month(month_str: str) -> bool:
    """Valida un mese nel formato YYYY-MM"""
    try:
        datetime.strptime(f"{month_str}-01", "%Y-%m-%d")
        return True
    except ValueError:
        return False

def safe_input(prompt: str, default: str = "") -> str:
    """Input sicuro con gestione delle eccezioni"""
    try:
        result = input(prompt).strip()
        return result if result else default
    except (KeyboardInterrupt, EOFError):
        return default

def format_transaction_summary(transactions: list) -> str:
    """Formatta un riassunto delle transazioni"""
    if not transactions:
        return "Nessuna transazione"
        
    total_income = sum(t["importo"] for t in transactions if t["tipo"] == "entrata")
    total_expenses = sum(t["importo"] for t in transactions if t["tipo"] == "spesa")
    
    return f"Entrate: {format_currency(total_income)} | Spese: {format_currency(total_expenses)}"

def create_progress_bar(current: float, total: float, width: int = 20) -> str:
    """Crea una barra di progresso testuale"""
    if total == 0:
        return "█" * width
        
    percentage = min(current / total, 1.0)
    filled = int(percentage * width)
    bar = "█" * filled + "░" * (width - filled)
    
    return f"[{bar}] {format_percentage(percentage * 100)}"

def format_file_size(size_bytes: int) -> str:
    """Formatta la dimensione di un file"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
        
    return f"{size_bytes:.1f} {size_names[i]}"

def get_file_info(filename: str) -> dict:
    """Ottieni informazioni su un file"""
    try:
        if os.path.exists(filename):
            stat = os.stat(filename)
            return {
                "exists": True,
                "size": stat.st_size,
                "size_formatted": format_file_size(stat.st_size),
                "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            return {"exists": False}
    except Exception as e:
        return {"exists": False, "error": str(e)}

def backup_file(filename: str) -> bool:
    """Crea un backup di un file"""
    try:
        if os.path.exists(filename):
            backup_name = f"{filename}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            with open(filename, 'r', encoding='utf-8') as original:
                with open(backup_name, 'w', encoding='utf-8') as backup:
                    backup.write(original.read())
            return True
        return False
    except Exception as e:
        print(f"Errore durante la creazione del backup: {e}")
        return False

def print_header(title: str, width: int = 60):
    """Stampa un'intestazione formattata"""
    print("=" * width)
    print(f"{title:^{width}}")
    print("=" * width)

def print_separator(char: str = "-", width: int = 60):
    """Stampa un separatore"""
    print(char * width)

def wait_for_input(message: str = "Premi INVIO per continuare..."):
    """Aspetta l'input dell'utente"""
    try:
        input(message)
    except KeyboardInterrupt:
        pass

def confirm_action(message: str, default: bool = False) -> bool:
    """Richiede conferma per un'azione"""
    suffix = " (s/N): " if not default else " (S/n): "
    try:
        response = input(message + suffix).strip().lower()
        if not response:
            return default
        return response in ['s', 'si', 'sì', 'y', 'yes']
    except KeyboardInterrupt:
        return False

def display_table(headers: list, rows: list, max_width: int = 80):
    """Visualizza una tabella formattata"""
    if not rows:
        print("Nessun dato da visualizzare")
        return
        
    # Calcola la larghezza delle colonne
    col_widths = [len(str(header)) for header in headers]
    
    for row in rows:
        for i, cell in enumerate(row[:len(col_widths)]):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Limita la larghezza totale
    total_width = sum(col_widths) + len(headers) * 3 - 1
    if total_width > max_width:
        # Ridimensiona le colonne proporzionalmente
        scale_factor = (max_width - len(headers) * 3 + 1) / total_width
        col_widths = [max(8, int(w * scale_factor)) for w in col_widths]
    
    # Stampa l'intestazione
    header_row = " | ".join(str(header)[:width].ljust(width) 
                           for header, width in zip(headers, col_widths))
    print(header_row)
    print("-" * len(header_row))
    
    # Stampa le righe
    for row in rows:
        data_row = " | ".join(str(cell)[:width].ljust(width) 
                             for cell, width in zip(row[:len(col_widths)], col_widths))
        print(data_row)

def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Tronca un testo se è troppo lungo"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
