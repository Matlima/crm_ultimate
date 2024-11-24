from flask import render_template, request, redirect, session, flash, url_for
from application import app, db
from models.models import Activity, User, Customer, Prospect
from helpers.forms_helpers import FormActivity, is_admin
from helpers.validation_helpers import type_user
from datetime import datetime

## Method Router Principal:

@app.route('/')
def index():
    lista = Activity.query.order_by(Activity.id)
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('index')))
    grupo = type_user()
    activities = db.session.query(Activity).join(User).all()
    form = FormActivity()
    return render_template('menu/main-menu.html',
                           titulo='Menu Principal',
                           atividades=activities,
                           # admin=admin,
                           form=form,
                           grupo=grupo
                           )


## Method Routes:

@app.route('/activities')
def activity():
    lista = Activity.query.order_by(Activity.id)
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('activity')))
    adm = is_admin()
    # activities = db.session.query(Activity).join(User).all()
    form = FormActivity()
    page = request.args.get('page', 1, type=int)
    activities = (
        db.session.query(Activity)
        .join(User)
        .order_by(Activity.data_inicio.desc())  # Ordena pelo campo 'data' em ordem decrescente
        .paginate(page=page, per_page=10)
    )

    return render_template('activities/activities.html',
                           titulo='Atividades',
                           atividades=activities,
                           clientes=Customer.query.all(),
                           prospects=Prospect.query.all(),
                           is_admin=adm,
                           form=form
                           )

@app.route('/activities/my-activities')
def my_activity():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))

    form = FormActivity()
    usuario_id = session["usuario_id"]

    # Adicionando paginação
    page = request.args.get('page', 1, type=int)

    # Consulta que faz join tanto com Customer quanto com Prospect
    activities = db.session.query(Activity, Customer, Prospect) \
        .outerjoin(Customer, Activity.cliente_id == Customer.id) \
        .outerjoin(Prospect, Activity.prospect_id == Prospect.id) \
        .filter(Activity.usuario_id == usuario_id) \
        .order_by(Activity.data_inicio.desc()) \
        .paginate(page=page, per_page=10)  # Define 10 atividades por página

    return render_template('activities/my_activities.html',
                           activities=activities,
                           form=form,
                           clientes=Customer.query.all(),
                           prospects=Prospect.query.all(),
                           page=page
                           )

@app.route('/activities/new')
def new_activity():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormActivity()
    usuario_id = session["usuario_id"]
    adm = is_admin()
    # grupo = type_user()
    return render_template('activities/add_activity.html',
                           titulo='Nova atividade',
                           form=form,
                           clientes=Customer.query.all(),
                           prospects=Prospect.query.all(),
                           usuarios=User.query.all(),
                           is_admin=adm
                           )

@app.route('/activities/info/<int:id>/<string:action>')
def info_activity(id, action):
    activity = Activity.query.filter_by(id=id).first()

    form = FormActivity()
    # Preenchendo dados do SelectField na view
    form.usuario_id.choices = [(user.id, user.nome) for user in User.query.all()]
    form.cliente_id.choices = [(customer.id, customer.razao_social) for customer in Customer.query.all()]
    # Definindo o usuário selecionado
    form.usuario_id.default = activity.usuario_id
    form.cliente_id.default = activity.cliente_id
    # Processando definições para a view
    form.process()
    form.data_inicio.data = activity.data_inicio
    form.data_fim.data = activity.data_fim
    form.titulo.data = activity.titulo
    form.descricao.data = activity.descricao
    form.tipo.data = activity.tipo
    form.status.data = activity.status

    return render_template('activities/info_activity.html',
                           titulo="Informações da atividade",
                           id=id,
                           form=form,
                           action=action
                           )



## Methods Actions:

@app.route('/activities/add', methods=['POST'])
def created_activity():
    form = FormActivity(request.form)
    form.cliente_id.choices = [(cliente.id, cliente.razao_social) for cliente in Customer.query.all()]
    form.usuario_id.choices = [(usuario.id, usuario.nome) for usuario in User.query.all()]

    data_inicio = datetime.now()
    data_fim = form.data_fim.data
    titulo = form.titulo.data
    descricao = form.descricao.data
    tipo = form.tipo.data
    status = form.status.data
    cliente_id = form.cliente_id.data
    prospect_id = form.prospect_id.data
    usuario_id = session["usuario_id"]

    new_activity = Activity(
        data_inicio=data_inicio,
        data_fim = data_fim,
        titulo = titulo,
        descricao = descricao,
        tipo = tipo,
        status = status,
        cliente_id = cliente_id,
        usuario_id = usuario_id,
        prospect_id=prospect_id
    )
    db.session.add(new_activity)
    db.session.commit()
    flash('Atividade adicionada com sucesso!')
    return redirect(url_for('my_activity'))

@app.route('/activities/delete/<int:id>')
def delete_activity(id):
    usuario_id = session['usuario_id']
    usuario = User.query.filter_by(id=usuario_id).first()
    activity = Activity.query.filter_by(id=id).first()

    if usuario.grupo == 'administrador':
        Activity.query.filter_by(id=id).delete()
        db.session.commit()
        flash('Atividade excluida com sucesso!')
    else:
        if usuario_id == activity.usuario_id:
            Activity.query.filter_by(id=id).delete()
            db.session.commit()
            flash('Atividade excluida com sucesso!')
        else:
            flash('O usuário logado não é responsavel pela atividade')
    return redirect(url_for('activity'))

@app.route('/activities/sucess/<int:id>', methods=['POST'])
def complete_activity(id):
    activity = Activity.query.filter_by(id=id).first()
    form = FormActivity(request.form)
    if activity:
        activity.status = 'Concluído'
        activity.data_fim = datetime.now()
        db.session.commit()
        flash('Atividade concluída com sucesso!')
    else:
        flash('Atividade não encontrada')
    return redirect(url_for('activity'))
