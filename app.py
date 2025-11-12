from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests

app = Flask(__name__)
app.secret_key = 'mimo'

FIREBASE_URL = 'https://petcare-734c7-default-rtdb.firebaseio.com/'

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        resposta = requests.get(FIREBASE_URL + 'usuarios.json')
        usuarios = resposta.json() or {}

        if username in usuarios:
            flash('Usuário já existe!', 'warning')
            return redirect(url_for('cadastro'))

        usuarios[username] = {'senha': password}
        requests.put(FIREBASE_URL + 'usuarios.json', json=usuarios)

        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))

    return render_template('cadastro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    next_page = request.args.get('next')
    if 'username' in session:
        flash(f'Você já está logado como {session["username"]}.', 'info')
        return redirect(next_page or url_for('bem_vindo', username=session['username']))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        resposta = requests.get(FIREBASE_URL + 'usuarios.json')
        usuarios = resposta.json() or {}

        if username in usuarios and usuarios[username]['senha'] == password:
            session['username'] = username
            flash('Login efetuado com sucesso!', 'success')
            return redirect(next_page or url_for('bem_vindo', username=username))
        else:
            flash('Credenciais inválidas.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('login'))

@app.route('/agendar/consulta', methods=['GET', 'POST'])
def agendar_consulta():
    if 'username' not in session:
        flash('Você precisa estar logado para agendar uma consulta.', 'warning')
        return redirect(url_for('login', next=url_for('agendar_consulta')))

    if request.method == 'POST':
        dados = {
            "tutor": session['username'],
            "nomeTutor": request.form.get("nomeTutor"),
            "cpfTutor": request.form.get("cpfTutor"),
            "telefone": request.form.get("telefone"),
            "email": request.form.get("email"),
            "endereco": request.form.get("endereco"),
            "nomeAnimal": request.form.get("nomeAnimal"),
            "especie": request.form.get("especie"),
            "raca": request.form.get("raca"),
            "sexo": request.form.get("sexo"),
            "idade": request.form.get("idade"),
            "peso": request.form.get("peso"),
            "motivo": request.form.get("motivo"),
            "observacoes": request.form.get("observacoes"),
            "dataConsulta": request.form.get("dataConsulta"),
            "horaConsulta": request.form.get("horaConsulta"),
        }

        requests.post(FIREBASE_URL + 'consultas.json', json=dados)
        flash('Consulta agendada com sucesso!', 'success')
        return redirect(url_for('sucesso'))

    return render_template('agendarConsulta.html')

@app.route('/minhas/consultas', methods=['GET'])
def consultas():
    if 'username' not in session:
        flash('Faça login para acessar.', 'warning')
        return redirect(url_for('login', next=url_for('consultas')))

    resposta = requests.get(FIREBASE_URL + 'consultas.json')
    todas_consultas = resposta.json() or {}

    consultas_usuario = [consulta for consulta in todas_consultas.values() if consulta['tutor'] == session['username']]

    return render_template('consultas.html', consultas=consultas_usuario)

@app.route('/sucesso', methods=['GET'])
def sucesso():
    return render_template('sucesso.html')


@app.route('/bemvindo/<username>', methods=['GET'])
def bem_vindo(username):
    if 'username' not in session:
        flash('Você precisa estar logado para acessar essa página.', 'warning')
        return redirect(url_for('login'))

    if session['username'] != username:
        flash('Você só pode acessar a sua própria página.', 'danger')
        return redirect(url_for('bem_vindo', username=session['username']))

    return render_template('bemvindo.html', usuario=username)


if __name__ == '__main__':
    app.run(debug=True)
