# MeetRoom_calendar
### Documentação Detalhada do Código de Calendário para Agendamento de Sala de Reunião

---
![image](https://github.com/user-attachments/assets/70d8976c-9e93-4609-ab29-14d9e97369e4)

#### **Backend (Python Flask)**

**1. Definição das Rotas**

O backend do sistema é construído utilizando Flask, um micro-framework para aplicações web em Python. A seguir, estão detalhadas as rotas e funções utilizadas para o gerenciamento de eventos de agendamento de uma sala de reunião.

---

**Rota `/addEventMeetingRoom01`**

- **Métodos Aceitos:** `POST`, `OPTIONS`, `GET`.
- **Descrição:** Esta rota permite a adição de novos eventos ao calendário da sala de reunião. Ela suporta três métodos HTTP: 
  - **OPTIONS:** Retorna uma resposta simples com `{'success': True}` para lidar com as preflight requests do CORS.
  - **POST:** Recebe os dados do evento a partir de uma requisição JSON e insere esses dados no banco de dados.
  - **GET:** Não implementado; opcionalmente pode ser usado para outras finalidades.

**Código da Função:**
```python
@app.route('/addEventMeetingRoom01', methods=['POST', 'OPTIONS', 'GET'])
def add_event01():
```

- **Configuração do Banco de Dados (`db_config`):** Contém as credenciais para conexão com o banco de dados MySQL, como usuário, senha, host, e nome do banco.

```python
db_config = {
    'user': 'user',
    'password': 'password',
    'host': 'host',
    'database': '__db__'
}
```

- **Recebimento de Dados:**
  - Os dados do evento (título, responsável, participantes, hora de início, hora de término, descrição) são extraídos do corpo da requisição JSON.
  - O campo `start` e `end` são concatenados para incluir tanto a data quanto a hora no formato `YYYY-MM-DDTHH:MM`.

```python
data = request.get_json()
title = data['title']
responsible = data['responsible']
participants = data['participants']
start = f"{data['date']}T{data['start']}"
end = f"{data['date']}T{data['end']}"
description = data['description']
created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
```

- **Inserção no Banco de Dados:**
  - A conexão com o banco de dados é aberta e os dados são inseridos na tabela `meetingroom01`.
  - Em caso de sucesso, a transação é confirmada (commit), e a conexão é encerrada.

```python
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
```

**Rota `/consultEventMeetingRoom01`**

- **Método Aceito:** `GET`.
- **Descrição:** Esta rota permite a consulta dos eventos cadastrados no banco de dados para a sala de reunião. Ela retorna todos os eventos na tabela `meetingroom01` em formato JSON.

**Código da Função:**
```python
@app.route('/consultEventMeetingRoom01', methods=['GET'])
def get_events01():
```

- **Consulta ao Banco de Dados:**
  - Conecta ao banco de dados MySQL, executa uma query que seleciona os campos `id`, `title`, `responsible`, `participants`, `START`, `end`, e `description` da tabela `meetingroom01`.
  - Os resultados são retornados em formato JSON, com as datas formatadas no padrão ISO 8601.

```python
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
```

**Estrutura do Banco de Dados:**
- **Tabela `meetingroom01`:** Contém os seguintes campos:
  - `id`: Identificador único do evento.
  - `title`: Título do evento.
  - `responsible`: Nome do responsável pelo evento.
  - `participants`: Lista de participantes.
  - `START`: Data e hora de início do evento.
  - `end`: Data e hora de término do evento.
  - `description`: Descrição do evento.
  - `created_at`: Data e hora de criação do registro.

---

#### **Frontend (HTML e JavaScript)**

**1. Estrutura HTML**

A estrutura HTML define a interface do usuário para visualizar e interagir com o calendário de eventos.

**Elementos Principais:**

- **Calendário:**
  - É utilizado o **FullCalendar**, uma biblioteca JavaScript para a criação e gerenciamento de calendários interativos.

```html
<h1 class="h1Txt">Sala de Reunião Principal</h1>
<div id='calendar'></div>
```

- **Modal para Detalhes do Evento:**
  - Exibe os detalhes completos de um evento quando clicado no calendário. Contém informações como título, responsável, participantes, horário de início e término, e descrição.

```html
<div id="eventDetailsModal">
    <div class="modal-content">
        <span class="close-details">&times;</span>
        <h2>Detalhes do Evento</h2>
        <p><strong>Título:</strong> <span id="detailTitle"></span></p>
        <p><strong>Responsável:</strong> <span id="detailResponsible"></span></p>
        <p><strong>Participantes:</strong> <span id="detailParticipants"></span></p>
        <p><strong>Início:</strong> <span id="detailStart"></span></p>
        <p><strong>Fim:</strong> <span id="detailEnd"></span></p>
        <p><strong>Descrição:</strong> <span id="detailDescription"></span></p>
    </div>
</div>
```

- **Modal para Adicionar Evento:**
  - Um formulário para adicionar novos eventos ao calendário. Contém campos para título, responsável, participantes, horário de início, horário de término, e descrição.

```html
<div id="eventModal">
    <div class="modal-content">
        <span class="close">&times;</span>
        <h2>Adicionar Evento</h2>
        <form id="eventForm">
            <label for="title" class="inputLabel">Título do Evento:</label><br>
            <input type="text" id="title" name="title" required class="inputs"><br><br>
            <label for="responsible" class="inputLabel">Responsável:</label><br>
            <input type="text" id="responsible" name="responsible" required class="inputs"><br><br>
            <label for="participants" class="inputLabel">Demais Participantes:</label><br>
            <input type="text" id="participants" name="participants" class="inputs"><br><br>
            <label for="start" class="inputLabel">Hora de Início:</label><br>
            <input type="time" id="start" name="start" required class="inputs"><br><br>
            <label for="end" class="inputLabel">Hora de Finalização:</label><br>
            <input type="time" id="end" name="end" required class="inputs"><br><br>
            <label for="description" class="inputLabel">Descrição:</label><br>
            <textarea id="description" name="description" class="inputs"></textarea><br><br>


            <button type="submit" id="addEventButton" class="btn btn-lg">Adicionar</button>
        </form>
    </div>
</div>
```

**2. Interações em JavaScript**

**Iniciando o FullCalendar**

- Configura o calendário com a funcionalidade de criar e visualizar eventos.
- Define a funcionalidade de clique para abrir o modal de adição de eventos.

```javascript
document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        selectable: true,
        select: function(info) {
            // Ação quando um dia é selecionado
        },
        eventClick: function(info) {
            // Ação quando um evento é clicado
        }
    });
    calendar.render();
});
```

**Manipulação de Modals**

- **Abrir e Fechar Modals:** Funções para abrir e fechar os modals de detalhes e adição de eventos.
- **Submissão do Formulário de Evento:** Submete os dados para a rota `/addEventMeetingRoom01` via AJAX.

```javascript
document.getElementById('eventForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var eventData = {
        title: document.getElementById('title').value,
        responsible: document.getElementById('responsible').value,
        participants: document.getElementById('participants').value,
        start: document.getElementById('start').value,
        end: document.getElementById('end').value,
        description: document.getElementById('description').value
    };
    fetch('http://localhost:5000/addEventMeetingRoom01', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(eventData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Atualiza o calendário com o novo evento
        }
    });
});
```

**Fechamento dos Modals**

- **Interação com Botões de Fechamento:** Funções que associam o fechamento dos modals ao clique nos botões correspondentes.

```javascript
var modal = document.getElementById('eventModal');
var span = document.getElementsByClassName('close')[0];
span.onclick = function() {
    modal.style.display = 'none';
}
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}
```

---

#### **Observações Finais**

Esta documentação fornece uma visão detalhada das implementações tanto no frontend quanto no backend, destacando a integração entre as tecnologias e o fluxo de dados. A partir desta estrutura, é possível expandir e adaptar o sistema conforme as necessidades específicas da aplicação de agendamento de sala de reunião.

--- 

Caso tenha alguma dúvida ou necessidade de ajustes adicionais, estou à disposição!
