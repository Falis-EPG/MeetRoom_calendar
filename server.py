from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from datetime import datetime
import re



app = Flask(__name__)
CORS(app)

##########################################################################################################################

@app.route('/addEventMeetingRoom01', methods=['POST', 'OPTIONS', 'GET'])
def add_event01():

    if request.method =='OPTIONS':
        return jsonify({'success': True})

    if request.method == 'POST':
        db_config = {
            'user': 'user',
            'password': 'password',
            'host': 'host',
            'database': '__db__'
        }

        data = request.get_json()
        title = data['title']
        responsible = data['responsible']
        participants = data['participants']
        start = f"{data['date']}T{data['start']}"
        end = f"{data['date']}T{data['end']}"
        description = data['description']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO meetingroom01 (title, responsible, participants, START, end, description, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (title, responsible, participants, start, end, description, created_at))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True})
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            return jsonify({'success': False})
        
@app.route('/consultEventMeetingRoom01', methods=['GET'])
def get_events01():
    if request.method == 'OPTIONS':
        return jsonify({'success': True})

    if request.method == 'GET':
        print("connected")
        try:
            db_config = {
            'user': 'user',
            'password': 'password',
            'host': 'host',
            'database': '__db__'
        }
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, title, responsible, participants, START, end, description FROM meetingroom01")
            events = cursor.fetchall()
            cursor.close()
            conn.close()

            # Convertendo datas para formato ISO 8601
            for event in events:
                event['START'] = event['START'].isoformat()
                event['end'] = event['end'].isoformat()

            print(events)
            return jsonify(events)
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            return jsonify([])
        
#################################################################################################################

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
