import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='../templates')

# --- FACTORY DATA ---
EMPLOYEES = [
    {"name": "โอ่ง", "daily_wage": 350, "night_wage": 50},
    {"name": "สุ", "daily_wage": 290, "night_wage": 50},
    {"name": "สาย", "daily_wage": 320, "night_wage": 50},
    {"name": "แยม", "daily_wage": 270, "night_wage": 50},
    {"name": "คนไทย", "daily_wage": 280, "night_wage": 50},
    {"name": "พม่า1", "daily_wage": 270, "night_wage": 50},
    {"name": "พม่า2", "daily_wage": 270, "night_wage": 50},
    {"name": "พม่า3", "daily_wage": 270, "night_wage": 50},
    {"name": "พม่า4", "daily_wage": 270, "night_wage": 50},
    {"name": "พม่า5", "daily_wage": 270, "night_wage": 50},
    {"name": "พม่า6", "daily_wage": 270, "night_wage": 50}
]

PRODUCTS = [
    {"name": "มือจับ", "unit": "อัน", "price": 0.6},
    {"name": "ด้าม", "unit": "อัน", "price": 0.6},
    {"name": "กลอน", "unit": "อัน", "price": 1.0},
    {"name": "พลั่ว", "unit": "ชิ้น", "price": 0.6},
    {"name": "พลั่วหนีบ", "unit": "ชิ้น", "price": 6.0},
    {"name": "พลั่ว (เก่ง)", "unit": "โหล", "price": 20.0},
    {"name": "น้ำ", "unit": "ถัง", "price": 15.0},
    {"name": "พลั่วตัดใบ", "unit": "โหล", "price": 12.0},
    {"name": "พลั่วพ่น", "unit": "โหล", "price": 20.0},
    {"name": "บานพับ", "unit": "อัน", "price": 0.5},
    {"name": "บานพับ (สอน)", "unit": "มัด", "price": 0.6},
    {"name": "สมอสั้น", "unit": "อัน", "price": 2.0},
    {"name": "สมอยาว", "unit": "อัน", "price": 2.0},
    {"name": "ปักร่มอ๊อก", "unit": "อัน", "price": 2.0},
    {"name": "ปักร่มใส่ห่วง", "unit": "อัน", "price": 2.0},
    {"name": "ปักร่มปั๊ม", "unit": "อัน", "price": 0.6},
    {"name": "คราดอ๊อก", "unit": "อัน", "price": 2.0},
    {"name": "คราดบวกด้าม", "unit": "อัน", "price": 2.0},
    {"name": "คราดปั๊ม", "unit": "อัน", "price": 0.6},
    {"name": "กุญแจดัดเหล็ก 2x3", "unit": "อัน", "price": 3.0},
    {"name": "กุญแจดัดเหล็ก 3x4", "unit": "อัน", "price": 4.0},
    {"name": "กุญแจดัดเหล็ก 4x5", "unit": "อัน", "price": 4.0},
    {"name": "กุญแจดัดเหล็ก 5x6", "unit": "อัน", "price": 4.0},
    {"name": "แชลง", "unit": "อัน", "price": 2.0},
    {"name": "รอก", "unit": "อัน", "price": 1.0}
]

@app.route('/')
def index():
    current_date = datetime.now().strftime("%d/%m/%Y")
    doc_id = f"WAGE-{datetime.now().strftime('%Y%m%d%H%M')}"
    return render_template(
        'index.html', 
        employees=EMPLOYEES, 
        products=PRODUCTS, 
        current_date=current_date, 
        doc_id=doc_id
    )

@app.route('/calculate', methods=['POST'])
def calculate():
    req_json = request.get_json() or {}
    input_rows = req_json.get('data', [])
    
    emp_lookup = {e['name']: e for e in EMPLOYEES}
    prod_lookup = {p['name']: p for p in PRODUCTS}
    
    calculated_results = []
    grand_total = 0.0
    
    for row in input_rows:
        name = row.get('emp_name', '').strip()
        days = float(row.get('days_worked', 0))
        p_name = row.get('prod_name', '').strip()
        qty = float(row.get('prod_qty', 0))
        
        base_wage = emp_lookup.get(name, {}).get('daily_wage', 0)
        base_total = days * base_wage
        
        prod_info = prod_lookup.get(p_name, {})
        unit = prod_info.get('unit', '')
        rate = prod_info.get('price', 0.0)
        prod_total = qty * rate
        
        sub_total = base_total + prod_total
        grand_total += sub_total
        
        calculated_results.append({
            "emp_name": name,
            "days_worked": days,
            "base_wage": base_wage,
            "prod_name": p_name,
            "prod_qty": qty,
            "unit": unit,
            "prod_total": prod_total,
            "sub_total": sub_total
        })
        
    return jsonify({
        "results": calculated_results,
        "grand_total": grand_total,
        "total_employees": len(calculated_results)
    })