from flask import Flask, render_template, request, redirect, url_for,session,flash
app = Flask(__name__)
app.secret_key = 'segredo_super_importante'  # necessário para usar session
import mysql.connector
import time


# ========= CONEXÃO COM BANCO ==========
def conectar():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",  # coloque sua senha do MySQL
        database="cifra_music_cadastro"
    )

# ========= ROTAS ==========
@app.route('/')
def login():
    if session.get('logado'):
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        conexao = conectar()
        cursor = conexao.cursor(buffered=True, dictionary=True)
        cursor.execute(
            "SELECT * FROM tb_usuario WHERE nm_login=%s AND ds_senha=%s",
            (usuario, senha)
        )
        user = cursor.fetchone()
        cursor.close()
        conexao.close()

        if user:
            session['logado'] = True
            session['usuario'] = user['nm_usuario']
            session['id_usuario'] = user['id']
            session['inadmin'] = user['inadmin']

            if str(user['inadmin']) == "1":
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    
    return render_template('login.html')

#Listagem de usuários
@app.route('/listusuario')
def listusuario():
    if not session.get('logado'):
        return redirect(url_for('login'))

    conexao = conectar()
    cursor = conexao.cursor(buffered=True, dictionary=True)
    cursor.execute("""
        SELECT *  from tb_usuario 
    """)
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()

    return render_template('admin/listarusuario.html', dados=dados)

# ========= CADASTRAR USUÁRIO ==========
@app.route('/usuario_cliente', methods=['GET', 'POST'])
def usuario_cliente():
    # if not session.get('logado'):
    #     return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        login = request.form.get('login')
        senha = request.form.get('senha')
        inadmin = "1"  # "1" = admin, "2" = normal

        if login and senha:
            conexao = conectar()
            cursor = conexao.cursor(buffered=True)
            sql = "INSERT INTO tb_usuario (nm_usuario, nm_login, ds_senha, inadmin) VALUES (%s, %s, %s, %s)"
            valores = (nome, login, senha, inadmin)
            cursor.execute(sql, valores)
            conexao.commit()
            cursor.close()
            conexao.close()
            flash('Usuário cadastrado com sucesso!', 'sucesso')
            return redirect(url_for('login'))



    return render_template('usuario.html')
#Rota para editar usuário
@app.route('/usuario/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    if not session.get('logado'):
        return redirect(url_for('login'))

    conexao = conectar()
    cursor = conexao.cursor(buffered=True, dictionary=True)

    if request.method == 'POST':
        nome = request.form.get('nome')
        login = request.form.get('login')
        inadmin = request.form.get('inadmin')

        sql = "UPDATE tb_usuario SET nm_usuario=%s, nm_login=%s, inadmin=%s WHERE id=%s"
        valores = (nome, login, inadmin, id)
        cursor.execute(sql, valores)
        conexao.commit()
        cursor.close()
        conexao.close()

        flash('Usuário atualizado com sucesso!', 'sucesso')
        return redirect(url_for('listusuario'))

    cursor.execute("SELECT * FROM tb_usuario WHERE id=%s", (id,))
    usuario = cursor.fetchone()
    cursor.close()
    conexao.close()

    return render_template('admin/editar_usuario.html', usuario=usuario)
#Fim da rota para editar usuário

#Rota para excluir usuário
@app.route('/usuario/excluir/<int:id>')
def excluir_usuario(id):
    if not session.get('logado'):
        return redirect(url_for('login'))

    conexao = conectar()
    cursor = conexao.cursor(buffered=True)
    cursor.execute("DELETE FROM tb_usuario WHERE id=%s", (id,))
    conexao.commit()
    cursor.close()
    conexao.close()

    flash('Usuário excluído com sucesso!', 'sucesso')
    return redirect(url_for('listusuario'))

#Fim da rota para excluir usuário

@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('login'))

@app.route('/index')
def index():
    if not session.get('logado'):
        return redirect(url_for('login'))
    return render_template('index.html', usuario=session['usuario'])

@app.route('/excluir/<int:id>')
def excluir(id):
    if not session.get('logado'):
        return redirect(url_for('login'))

    conexao = conectar()
    cursor = conexao.cursor(buffered=True)
    cursor.execute("DELETE FROM tb_cliente WHERE id = %s", (id,))
    conexao.commit()
    cursor.close()
    conexao.close()

    flash('Cliente excluído com sucesso!', 'info')
    return redirect(url_for('listar'))

dados_pessoais = [0]

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    return render_template('cadastrar.html', dados=dados_pessoais)

@app.route('/listar')
def listar():
    return render_template('admin/listar.html', dados=dados_pessoais)

@app.route('/admin')
def admin():
    return render_template('admin/index.html', dados=dados_pessoais)

@app.route('/logs')
def registro_logs():
    return render_template('admin/logs.html', dados=dados_pessoais)

@app.route("/carrinho")
def carrinho():
    return render_template("carrinho.html")


@app.route('/violoes')
def violoes():

    return render_template('violoes.html', dados=dados_pessoais)

@app.route('/guitarras')
def guitaras():

    return render_template('guitarras.html', dados=dados_pessoais)

@app.route('/acessorios')
def acessorios():

    return render_template('acessorios.html', dados=dados_pessoais)

@app.route('/violaotakamine')
def violaotakamine():

    return render_template('violoes/violaotakamine.html', dados=dados_pessoais)

@app.route('/violaomartin')
def violaomartin():

    return render_template('violoes/violaomartin.html', dados=dados_pessoais)

    
@app.route('/violaoacofolk')
def violaoacofolk():
    
    return render_template('violoes/violaoacofolk.html', dados=dados_pessoais)

@app.route('/violaogibson')
def violaogibson():
    
    return render_template('violoes/violaogibson.html', dados=dados_pessoais)

@app.route('/violaotaylor')
def violaotaylor():
    
    return render_template('violoes/violaotaylor.html', dados=dados_pessoais)

@app.route('/guitarracort')
def guitarracort():
    
    return render_template('guitarras/guitarracort.html', dados=dados_pessoais)

@app.route('/guitarrafender')
def guitarrafender():
    
    return render_template('guitarras/guitarrafender.html', dados=dados_pessoais)

@app.route('/guitarratagima')
def guitarratagima():
    
    return render_template('guitarras/guitarratagima.html', dados=dados_pessoais)

@app.route('/guitarrasuhr')
def guitarrasuhr():
    
    return render_template('guitarras/guitarrasuhr.html', dados=dados_pessoais)

@app.route('/guitarragretsch')
def guitarragretsch():

    return render_template('guitarras/guitarragretsch.html', dados=dados_pessoais)

@app.route('/capotraste')
def capotraste():

    return render_template('acessorios/capotraste.html', dados=dados_pessoais)

@app.route('/palhetaguitarra')
def palhetaguitarra():

    return render_template('acessorios/palhetaguitarra.html', dados=dados_pessoais)

@app.route('/palhetafender')
def palhetafender():
    return render_template('acessorios/palhetafender.html', dados=dados_pessoais)

@app.route('/caseviolao')
def caseviolao():

    return render_template('acessorios/caseviolao.html', dados=dados_pessoais)

@app.route('/caseguitarra')
def caseguitarra():

    return render_template('acessorios/caseguitarra.html', dados=dados_pessoais)






















# @app.route('/excluir/<int:indice>')
# def excluir(indice):


#     # Verifica se o índice existe na lista
#     if 0 <= indice < len(dados_pessoais):
#         del dados_pessoais[indice]
#     return redirect(url_for('listar'))

# @app.route('/editar/<int:indice>', methods=['GET', 'POST'])
# def editar(indice):


#     # Verifica se o índice existe
#     if 0 <= indice < len(dados_pessoais):
#         if request.method == 'POST':
#             nome = request.form.get('nome')
#             email = request.form.get('email')
#             telefone = request.form.get('telefone')
#             idade = request.form.get('idade')

#             # Atualiza os dados
#             dados_pessoais[indice]['nome'] = nome
#             dados_pessoais[indice]['email'] = email
#             dados_pessoais[indice]['telefone'] = telefone
#             dados_pessoais[indice]['idade'] = idade

#             return redirect(url_for('listar'))

#         # GET → mostra o formulário com os dados preenchidos
#         item = dados_pessoais[indice]
#         return render_template('editar.html', item=item, indice=indice)
#     else:
#         return redirect(url_for('listar'))



if __name__ == '__main__':
    app.run(debug=True)