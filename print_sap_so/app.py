from markupsafe import Markup
import json
import urllib.request
from flask import Flask, request, jsonify, render_template
from datetime import datetime
from dateutil.relativedelta import relativedelta
import jinja2
import pdfkit
import os

app = Flask(__name__)
# Configuration
OUTPUT_FOLDER = 'HTML_FORM'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

cf_port = os.getenv("PORT")

@app.route('/printso', methods=['POST'])
def printso():
    data = request.get_json()   
    json_string = json.dumps(data)
    json_loads = json.loads(json_string)

    unique_data_dict = {item["sonumber"]: item for item in json_loads}
    unique_data_list = list(unique_data_dict.values()) 
    json_real = json.dumps(unique_data_list)
    json_pro = json.loads(json_real)

    for item in json_pro:
       sonumber = item["sonumber"]
       clientname = item["clientname"]
       invdate = item["invdate"]
       clientaddr = item["clientaddr"]
       currhdr = item["currhdr"]
       totalamt = item["totalamt"]    
       maturity = datetime.today() + relativedelta(months=1)
       matstr = str(maturity)
       mature = matstr[:10] 
       mature = mature[8:10] + '/' + mature[5:7] + '/' + mature[:4]
       print (mature)
        # Add timestamp
    context = {
            'sonumber': sonumber,
            'clientname': clientname,
            'invdate': invdate,
            'clientaddr': clientaddr,
            'currhdr': currhdr,
            'totalamt': totalamt,
            'items': json_loads,
            'duemature': mature
        }
    # Render template
    rendered_html = render_template('page.html', **context)  
    # Save to file
    filename = f"page_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = os.path.join(OUTPUT_FOLDER, filename)      
    with open(filepath, 'w', encoding='utf-8') as f:
         f.write(rendered_html)
        
    return jsonify({
            'success': True,
            'message': 'HTML file generated successfully',
            'filename': filename,
            'path': os.path.abspath(filepath)
        })
    

#if __name__ == "__main__":
#    app.run()
if __name__ == '__main__':
   if cf_port is None:
       app.run(host='0.0.0.0', port=5000)       
   else:
       app.run(host='0.0.0.0', port=int(cf_port))
       