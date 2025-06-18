from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import FinanceManager
from utils import format_currency, validate_amount, validate_date, get_current_date, get_current_month
from datetime import datetime
import json

app = Flask(__name__)
finance_manager = FinanceManager()
finance_manager.load_data()

@app.route('/')
def index():
    """Homepage con dashboard principale"""
    stats = finance_manager.get_statistics()
    current_month = get_current_month()
    monthly_report = finance_manager.get_monthly_report(current_month)
    recent_transactions = finance_manager.get_all_transactions()[:5]
    
    return render_template('index.html', 
                         stats=stats, 
                         monthly_report=monthly_report,
                         recent_transactions=recent_transactions,
                         current_month=current_month)

@app.route('/add_income', methods=['GET', 'POST'])
def add_income():
    """Aggiungi entrata"""
    if request.method == 'POST':
        data = request.get_json()
        
        descrizione = data.get('descrizione', '').strip()
        importo_str = data.get('importo', '')
        data_str = data.get('data', get_current_date())
        
        if not descrizione:
            return jsonify({'success': False, 'error': 'Descrizione obbligatoria'})
            
        importo = validate_amount(importo_str)
        if importo is None:
            return jsonify({'success': False, 'error': 'Importo non valido'})
            
        if not validate_date(data_str):
            return jsonify({'success': False, 'error': 'Data non valida'})
            
        success = finance_manager.add_income(descrizione, importo, data_str)
        
        if success:
            return jsonify({'success': True, 'message': f'Entrata di {format_currency(importo)} aggiunta!'})
        else:
            return jsonify({'success': False, 'error': 'Errore durante il salvataggio'})
    
    return render_template('add_income.html')

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    """Aggiungi spesa"""
    if request.method == 'POST':
        data = request.get_json()
        
        descrizione = data.get('descrizione', '').strip()
        importo_str = data.get('importo', '')
        categoria = data.get('categoria', '').strip()
        data_str = data.get('data', get_current_date())
        
        if not descrizione:
            return jsonify({'success': False, 'error': 'Descrizione obbligatoria'})
            
        if not categoria:
            return jsonify({'success': False, 'error': 'Categoria obbligatoria'})
            
        importo = validate_amount(importo_str)
        if importo is None:
            return jsonify({'success': False, 'error': 'Importo non valido'})
            
        if not validate_date(data_str):
            return jsonify({'success': False, 'error': 'Data non valida'})
            
        success = finance_manager.add_expense(descrizione, importo, data_str, categoria)
        
        if success:
            return jsonify({'success': True, 'message': f'Spesa di {format_currency(importo)} aggiunta!'})
        else:
            return jsonify({'success': False, 'error': 'Errore durante il salvataggio'})
    
    categories = finance_manager.get_categories()
    return render_template('add_expense.html', categories=categories)

@app.route('/transactions')
def transactions():
    """Visualizza tutte le transazioni"""
    all_transactions = finance_manager.get_all_transactions()
    return render_template('transactions.html', transactions=all_transactions)

@app.route('/budget')
def budget():
    """Gestione budget"""
    current_month = get_current_month()
    monthly_budget = finance_manager.get_monthly_budget()
    monthly_expenses = finance_manager.get_monthly_expenses(current_month)
    
    budget_data = {
        'budget': monthly_budget,
        'spent': monthly_expenses,
        'remaining': monthly_budget - monthly_expenses if monthly_budget > 0 else 0,
        'percentage': (monthly_expenses / monthly_budget * 100) if monthly_budget > 0 else 0
    }
    
    return render_template('budget.html', budget_data=budget_data, current_month=current_month)

@app.route('/set_budget', methods=['POST'])
def set_budget():
    """Imposta budget mensile"""
    data = request.get_json()
    budget_str = data.get('budget', '')
    
    budget = validate_amount(budget_str)
    if budget is None or budget <= 0:
        return jsonify({'success': False, 'error': 'Budget non valido'})
    
    success = finance_manager.set_monthly_budget(budget)
    
    if success:
        return jsonify({'success': True, 'message': f'Budget di {format_currency(budget)} impostato!'})
    else:
        return jsonify({'success': False, 'error': 'Errore durante il salvataggio'})

@app.route('/reports')
def reports():
    """Report mensili"""
    current_month = get_current_month()
    report = finance_manager.get_monthly_report(current_month)
    
    # Prepara dati per il grafico
    categories_data = []
    for categoria, importo in report['spese_per_categoria'].items():
        percentage = (importo / report['spese_totali'] * 100) if report['spese_totali'] > 0 else 0
        categories_data.append({
            'name': categoria,
            'amount': importo,
            'percentage': round(percentage, 1)
        })
    
    return render_template('reports.html', 
                         report=report, 
                         categories_data=categories_data,
                         current_month=current_month)

@app.route('/categories')
def categories():
    """Gestione categorie"""
    all_categories = finance_manager.get_categories()
    return render_template('categories.html', categories=all_categories)

@app.route('/add_category', methods=['POST'])
def add_category():
    """Aggiungi categoria"""
    data = request.get_json()
    categoria = data.get('categoria', '').strip()
    
    if not categoria:
        return jsonify({'success': False, 'error': 'Nome categoria obbligatorio'})
    
    success = finance_manager.add_category(categoria)
    
    if success:
        return jsonify({'success': True, 'message': f'Categoria "{categoria}" aggiunta!'})
    else:
        return jsonify({'success': False, 'error': 'Categoria già esistente'})

@app.route('/remove_category', methods=['POST'])
def remove_category():
    """Rimuovi categoria"""
    data = request.get_json()
    categoria = data.get('categoria', '').strip()
    
    if not categoria:
        return jsonify({'success': False, 'error': 'Nome categoria obbligatorio'})
    
    success = finance_manager.remove_category(categoria)
    
    if success:
        return jsonify({'success': True, 'message': f'Categoria "{categoria}" rimossa!'})
    else:
        return jsonify({'success': False, 'error': 'Errore durante la rimozione'})

@app.route('/api/dashboard_data')
def dashboard_data():
    """API per dati dashboard (per aggiornamenti real-time)"""
    stats = finance_manager.get_statistics()
    current_month = get_current_month()
    monthly_report = finance_manager.get_monthly_report(current_month)
    
    return jsonify({
        'stats': stats,
        'monthly_report': monthly_report,
        'current_month': current_month
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)