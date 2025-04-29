from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import IngresoForm, EgresoForm, MetaAhorroForm
from app.models import db, Ingreso, Egreso, MetaAhorro
from sqlalchemy import extract, func

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/nuevo_ingreso', methods=['GET', 'POST'])
def nuevo_ingreso():
    form = IngresoForm()
    if form.validate_on_submit():
        ingreso = Ingreso(
            descripcion=form.descripcion.data,
            cantidad=form.cantidad.data
        )
        db.session.add(ingreso)
        db.session.commit()
        flash('Ingreso registrado exitosamente', 'success')
        return redirect(url_for('main.home'))
    return render_template('nuevo_ingreso.html', form=form)

@main.route('/nuevo_egreso', methods=['GET', 'POST'])
def nuevo_egreso():
    form = EgresoForm()
    if form.validate_on_submit():
        egreso = Egreso(
            descripcion=form.descripcion.data,
            cantidad=form.cantidad.data
        )
        db.session.add(egreso)
        db.session.commit()
        flash('Egreso registrado exitosamente', 'success')
        return redirect(url_for('main.home'))
    return render_template('nuevo_egreso.html', form=form)

@main.route('/nueva_meta', methods=['GET', 'POST'])
def nueva_meta():
    form = MetaAhorroForm()
    if form.validate_on_submit():
        meta = MetaAhorro(
            nombre=form.nombre.data,
            cantidad_objetivo=form.cantidad_objetivo.data,
            fecha_limite=form.fecha_limite.data
        )
        db.session.add(meta)
        db.session.commit()
        flash('Meta de ahorro creada exitosamente', 'success')
        return redirect(url_for('main.home'))
    return render_template('nueva_meta.html', form=form)

@main.route('/metas')
def ver_metas():
    metas = MetaAhorro.query.all()
    return render_template('ver_metas.html', metas=metas)

@main.route('/dashboard')
def dashboard():
    ingresos = Ingreso.query.all()
    egresos = Egreso.query.all()

    total_ingresos = sum(i.cantidad for i in ingresos)
    total_egresos = sum(e.cantidad for e in egresos)
    balance = total_ingresos - total_egresos

    # Para gráfica histórica
    from sqlalchemy import extract, func

    ingresos_mensuales = db.session.query(
        extract('year', Ingreso.fecha).label('anio'),
        extract('month', Ingreso.fecha).label('mes'),
        func.sum(Ingreso.cantidad).label('total')
    ).group_by('anio', 'mes').order_by('anio', 'mes').all()

    egresos_mensuales = db.session.query(
        extract('year', Egreso.fecha).label('anio'),
        extract('month', Egreso.fecha).label('mes'),
        func.sum(Egreso.cantidad).label('total')
    ).group_by('anio', 'mes').order_by('anio', 'mes').all()

    # Procesar datos
    labels = []
    ingresos_data = []
    egresos_data = []
    balance_data = []

    meses_data = {}

    for anio, mes, total in ingresos_mensuales:
        key = f"{int(mes)}/{int(anio)}"
        meses_data[key] = {'ingresos': total, 'egresos': 0}

    for anio, mes, total in egresos_mensuales:
        key = f"{int(mes)}/{int(anio)}"
        if key in meses_data:
            meses_data[key]['egresos'] = total
        else:
            meses_data[key] = {'ingresos': 0, 'egresos': total}

    # Ordenamos por fecha
    meses_data = dict(sorted(meses_data.items(), key=lambda x: (int(x[0].split('/')[1]), int(x[0].split('/')[0]))))

    for fecha, data in meses_data.items():
        labels.append(fecha)
        ingresos_data.append(data['ingresos'])
        egresos_data.append(data['egresos'])
        balance_data.append(data['ingresos'] - data['egresos'])

    return render_template('dashboard.html',
                           total_ingresos=total_ingresos,
                           total_egresos=total_egresos,
                           balance=balance,
                           labels=labels,
                           ingresos_data=ingresos_data,
                           egresos_data=egresos_data,
                           balance_data=balance_data)


@main.route('/editar_meta/<int:meta_id>', methods=['GET', 'POST'])
def editar_meta(meta_id):
    meta = MetaAhorro.query.get_or_404(meta_id)
    form = MetaAhorroForm(obj=meta)

    if form.validate_on_submit():
        meta.nombre = form.nombre.data
        meta.cantidad_objetivo = form.cantidad_objetivo.data
        meta.fecha_limite = form.fecha_limite.data
        db.session.commit()
        flash('Meta actualizada exitosamente', 'success')
        return redirect(url_for('main.ver_metas'))

    return render_template('editar_meta.html', form=form, meta=meta)

@main.route('/eliminar_meta/<int:meta_id>', methods=['POST'])
def eliminar_meta(meta_id):
    meta = MetaAhorro.query.get_or_404(meta_id)
    db.session.delete(meta)
    db.session.commit()
    flash('Meta eliminada exitosamente', 'success')
    return redirect(url_for('main.ver_metas'))

@main.route('/ingresos')
def ver_ingresos():
    ingresos = Ingreso.query.all()
    return render_template('ver_ingresos.html', ingresos=ingresos)

@main.route('/editar_ingreso/<int:ingreso_id>', methods=['GET', 'POST'])
def editar_ingreso(ingreso_id):
    ingreso = Ingreso.query.get_or_404(ingreso_id)
    form = IngresoForm(obj=ingreso)

    if form.validate_on_submit():
        ingreso.descripcion = form.descripcion.data
        ingreso.cantidad = form.cantidad.data
        db.session.commit()
        flash('Ingreso actualizado exitosamente', 'success')
        return redirect(url_for('main.ver_ingresos'))

    return render_template('editar_ingreso.html', form=form, ingreso=ingreso)

@main.route('/eliminar_ingreso/<int:ingreso_id>', methods=['POST'])
def eliminar_ingreso(ingreso_id):
    ingreso = Ingreso.query.get_or_404(ingreso_id)
    db.session.delete(ingreso)
    db.session.commit()
    flash('Ingreso eliminado exitosamente', 'success')
    return redirect(url_for('main.ver_ingresos'))

@main.route('/egresos')
def ver_egresos():
    egresos = Egreso.query.all()
    return render_template('ver_egresos.html', egresos=egresos)

@main.route('/editar_egreso/<int:egreso_id>', methods=['GET', 'POST'])
def editar_egreso(egreso_id):
    egreso = Egreso.query.get_or_404(egreso_id)
    form = EgresoForm(obj=egreso)

    if form.validate_on_submit():
        egreso.descripcion = form.descripcion.data
        egreso.cantidad = form.cantidad.data
        db.session.commit()
        flash('Egreso actualizado exitosamente', 'success')
        return redirect(url_for('main.ver_egresos'))

    return render_template('editar_egreso.html', form=form, egreso=egreso)

@main.route('/eliminar_egreso/<int:egreso_id>', methods=['POST'])
def eliminar_egreso(egreso_id):
    egreso = Egreso.query.get_or_404(egreso_id)
    db.session.delete(egreso)
    db.session.commit()
    flash('Egreso eliminado exitosamente', 'success')
    return redirect(url_for('main.ver_egresos'))



@main.route('/historial')
def historial():
    # Agrupar ingresos por mes
    ingresos_mensuales = db.session.query(
        extract('year', Ingreso.fecha).label('anio'),
        extract('month', Ingreso.fecha).label('mes'),
        func.sum(Ingreso.cantidad).label('total')
    ).group_by('anio', 'mes').order_by('anio', 'mes').all()

    # Agrupar egresos por mes
    egresos_mensuales = db.session.query(
        extract('year', Egreso.fecha).label('anio'),
        extract('month', Egreso.fecha).label('mes'),
        func.sum(Egreso.cantidad).label('total')
    ).group_by('anio', 'mes').order_by('anio', 'mes').all()

    # Organizar la información
    historial_data = {}

    for anio, mes, total in ingresos_mensuales:
        key = f"{int(mes)}/{int(anio)}"
        historial_data.setdefault(key, {})['ingresos'] = total

    for anio, mes, total in egresos_mensuales:
        key = f"{int(mes)}/{int(anio)}"
        historial_data.setdefault(key, {})['egresos'] = total

    # Calcular balances
    for key in historial_data:
        ingresos = historial_data[key].get('ingresos', 0)
        egresos = historial_data[key].get('egresos', 0)
        historial_data[key]['balance'] = ingresos - egresos

    # Ordenar por fecha
    historial_ordenado = dict(sorted(historial_data.items(), key=lambda x: (int(x[0].split('/')[1]), int(x[0].split('/')[0]))))

    return render_template('historial.html', historial=historial_ordenado)
