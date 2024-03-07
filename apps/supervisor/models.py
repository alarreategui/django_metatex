# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cliente(models.Model):
    codcliente = models.CharField(db_column='codCliente', primary_key=True, max_length=191)  # Field name made lowercase.
    descripcion = models.CharField(max_length=191, blank=True, null=True)
    codtipocliente = models.ForeignKey('Tipocliente', models.DO_NOTHING, db_column='codTipoCliente', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'cliente'


class Color(models.Model):
    codcolor = models.CharField(db_column='codColor', primary_key=True, max_length=191)  # Field name made lowercase.
    descripcion = models.CharField(max_length=191, blank=True, null=True)
    gama = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'color'


class Contenedor(models.Model):
    codcontenedor = models.CharField(db_column='codContenedor', primary_key=True, max_length=191)  # Field name made lowercase.
    descripcion = models.CharField(max_length=191, blank=True, null=True)
    codubicacion = models.ForeignKey('Ubicacion', models.DO_NOTHING, db_column='codUbicacion', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'contenedor'


class Disponibilidad(models.Model):
    coddisponibilidad = models.CharField(db_column='codDisponibilidad', primary_key=True, max_length=191)  # Field name made lowercase.
    fechainicio = models.DateTimeField(db_column='fechaInicio', blank=True, null=True)  # Field name made lowercase.
    fechafin = models.DateTimeField(db_column='fechaFin', blank=True, null=True)  # Field name made lowercase.
    codparada = models.ForeignKey('Parada', models.DO_NOTHING, db_column='codParada', blank=True, null=True)  # Field name made lowercase.
    codmaquina = models.ForeignKey('Maquina', models.DO_NOTHING, db_column='codMaquina', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'disponibilidad'


class Maquina(models.Model):
    codmaquina = models.CharField(db_column='codMaquina', primary_key=True, max_length=191)  # Field name made lowercase.
    descripcion = models.CharField(max_length=191, blank=True, null=True)
    tipolinea = models.CharField(db_column='tipoLinea', max_length=191, blank=True, null=True)  # Field name made lowercase.
    paralelo = models.IntegerField(blank=True, null=True)
    codmaquinamaestro = models.CharField(db_column='codMaquinaMaestro', max_length=191, blank=True, null=True)  # Field name made lowercase.
    cantidadminimoreceta = models.DecimalField(db_column='cantidadMinimoReceta', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'maquina'


class Maquinaparada(models.Model):
    codmaquinaparada = models.CharField(db_column='codMaquinaParada', primary_key=True, max_length=191)  # Field name made lowercase.
    fechainicio = models.DateTimeField(db_column='fechaInicio', blank=True, null=True)  # Field name made lowercase.
    fechafin = models.DateTimeField(db_column='fechaFin', blank=True, null=True)  # Field name made lowercase.
    secuencia = models.IntegerField(blank=True, null=True)
    ubicacionparada = models.IntegerField(db_column='ubicacionParada', blank=True, null=True)  # Field name made lowercase.
    codoperario = models.ForeignKey('Operario', models.DO_NOTHING, db_column='codOperario', blank=True, null=True)  # Field name made lowercase.
    codmaquina = models.ForeignKey(Maquina, models.DO_NOTHING, db_column='codMaquina', blank=True, null=True)  # Field name made lowercase.
    codparada = models.ForeignKey('Parada', models.DO_NOTHING, db_column='codParada', blank=True, null=True)  # Field name made lowercase.
    codpartida = models.ForeignKey('Partida', models.DO_NOTHING, db_column='codPartida', blank=True, null=True)  # Field name made lowercase.
    codtela = models.ForeignKey('Tela', models.DO_NOTHING, db_column='codTela', blank=True, null=True)  # Field name made lowercase.
    codcolor = models.ForeignKey(Color, models.DO_NOTHING, db_column='codColor', blank=True, null=True)  # Field name made lowercase.
    codproceso = models.ForeignKey('Proceso', models.DO_NOTHING, db_column='codProceso', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'maquinaparada'


class Motivocambiovalorparametro(models.Model):
    descripcion = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)
    codmotivovalor = models.CharField(db_column='codMotivoValor', primary_key=True, max_length=191)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'motivocambiovalorparametro'


class Motivocambiovalorparametroxpartelcolsecpromaqpar(models.Model):
    codmotivocambiovalorparametropartida = models.AutoField(db_column='codMotivoCambioValorParametroPartida', primary_key=True)  # Field name made lowercase.
    motivocambiovalorparametrocodmotivovalor = models.ForeignKey(Motivocambiovalorparametro, models.DO_NOTHING, db_column='motivoCambioValorParametroCodMotivoValor', blank=True, null=True)  # Field name made lowercase.
    codpartidatelacolorsecuenciaprocesomaquinaparametro = models.ForeignKey('Partidatelacolorsecuenciaprocesomaquinaparametro', models.DO_NOTHING, db_column='codPartidaTelaColorSecuenciaProcesoMaquinaParametro', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'motivocambiovalorparametroxpartelcolsecpromaqpar'


class Motivoprioridad(models.Model):
    codmotivoprioridad = models.CharField(db_column='codMotivoPrioridad', primary_key=True, max_length=191)  # Field name made lowercase.
    descripcion = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'motivoprioridad'


class Motivoprioridadxpartida(models.Model):
    codmotivoprioridadxpartida = models.AutoField(db_column='codMotivoPrioridadxPartida', primary_key=True)  # Field name made lowercase.
    motivoprioridadcodmotivoprioridad = models.ForeignKey(Motivoprioridad, models.DO_NOTHING, db_column='motivoPrioridadCodMotivoPrioridad', blank=True, null=True)  # Field name made lowercase.
    partidacodpartida = models.OneToOneField('Partida', models.DO_NOTHING, db_column='partidaCodPartida', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'motivoprioridadxpartida'


class Operario(models.Model):
    codoperario = models.CharField(db_column='codOperario', primary_key=True, max_length=191)  # Field name made lowercase.
    nombre = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)
    rolcodigo = models.CharField(db_column='rolCodigo', max_length=191, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'operario'


class Operariomaquina(models.Model):
    codoperariomaquina = models.CharField(db_column='codOperarioMaquina', primary_key=True, max_length=191)  # Field name made lowercase.
    codoperario = models.ForeignKey(Operario, models.DO_NOTHING, db_column='codOperario', blank=True, null=True)  # Field name made lowercase.
    codmaquina = models.ForeignKey(Maquina, models.DO_NOTHING, db_column='codMaquina', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'operariomaquina'


class Parada(models.Model):
    codparada = models.CharField(db_column='codParada', primary_key=True, max_length=191)  # Field name made lowercase.
    descripcion = models.CharField(max_length=191, blank=True, null=True)
    tipoparada = models.IntegerField(db_column='tipoParada', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'parada'


class Parametrocalidad(models.Model):
    codparametro = models.CharField(db_column='codParametro', primary_key=True, max_length=191)  # Field name made lowercase.
    descripcion = models.CharField(max_length=191, blank=True, null=True)
    tipodedato = models.CharField(db_column='tipoDeDato', max_length=191, blank=True, null=True)  # Field name made lowercase.
    evaluable = models.IntegerField(blank=True, null=True)
    unidad = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)
    absoluto = models.CharField(max_length=191, blank=True, null=True)
    niveltolerancia1 = models.IntegerField(db_column='nivelTolerancia1', blank=True, null=True)  # Field name made lowercase.
    niveltolerancia2 = models.IntegerField(db_column='nivelTolerancia2', blank=True, null=True)  # Field name made lowercase.
    niveltolerancia3 = models.IntegerField(db_column='nivelTolerancia3', blank=True, null=True)  # Field name made lowercase.
    operacion = models.CharField(max_length=191, blank=True, null=True)
    tipodato = models.CharField(db_column='tipoDato', max_length=191, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'parametrocalidad'


class Parametromaquina(models.Model):
    codparametromaquina = models.CharField(db_column='codParametroMaquina', primary_key=True, max_length=191)  # Field name made lowercase.
    descripcion = models.CharField(max_length=191, blank=True, null=True)
    tipodedato = models.IntegerField(db_column='tipoDeDato', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)
    unidad = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parametromaquina'


class Partida(models.Model):
    codpartida = models.CharField(db_column='codPartida', primary_key=True, max_length=191)  # Field name made lowercase.
    fechalimiteentrega = models.DateTimeField(db_column='fechaLimiteEntrega', blank=True, null=True)  # Field name made lowercase.
    fechafintenido = models.DateTimeField(db_column='fechaFinTenido', blank=True, null=True)  # Field name made lowercase.
    codpedidocomercial = models.ForeignKey('Pedidocomercial', models.DO_NOTHING, db_column='codPedidoComercial', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)
    prioridad = models.IntegerField(blank=True, null=True)
    niveltolerancia = models.IntegerField(db_column='nivelTolerancia', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'partida'


class Partidacontenedor(models.Model):
    codpartidacontenedor = models.CharField(db_column='codPartidaContenedor', primary_key=True, max_length=191)  # Field name made lowercase.
    secuencia = models.IntegerField(blank=True, null=True)
    codcolor = models.ForeignKey(Color, models.DO_NOTHING, db_column='codColor', blank=True, null=True)  # Field name made lowercase.
    codproceso = models.ForeignKey('Proceso', models.DO_NOTHING, db_column='codProceso', blank=True, null=True)  # Field name made lowercase.
    codcontenedor = models.ForeignKey(Contenedor, models.DO_NOTHING, db_column='codContenedor', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)
    codtela = models.ForeignKey('Tela', models.DO_NOTHING, db_column='codTela', blank=True, null=True)  # Field name made lowercase.
    codpartida = models.ForeignKey(Partida, models.DO_NOTHING, db_column='codPartida', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'partidacontenedor'


class Partidatela(models.Model):
    codpartidatela = models.CharField(db_column='codPartidaTela', primary_key=True, max_length=191)  # Field name made lowercase.
    componenteprincipal = models.IntegerField(db_column='componentePrincipal', blank=True, null=True)  # Field name made lowercase.
    cantidadoriginal = models.DecimalField(db_column='cantidadOriginal', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    codcolor = models.ForeignKey(Color, models.DO_NOTHING, db_column='codColor', blank=True, null=True)  # Field name made lowercase.
    codtela = models.ForeignKey('Tela', models.DO_NOTHING, db_column='codTela', blank=True, null=True)  # Field name made lowercase.
    codpartida = models.ForeignKey(Partida, models.DO_NOTHING, db_column='codPartida', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)
    toleranciahumedo = models.TimeField(db_column='toleranciaHumedo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'partidatela'


class Partidatelacolorsecuenciaproceso(models.Model):
    codpartidatelacolorsecuenciaproceso = models.CharField(db_column='codPartidaTelaColorSecuenciaProceso', primary_key=True, max_length=191)  # Field name made lowercase.
    secuencia = models.IntegerField(blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    cantidadkg = models.DecimalField(db_column='cantidadKg', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    cantidadmt = models.DecimalField(db_column='cantidadMt', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    procesoestandar = models.IntegerField(db_column='procesoEstandar', blank=True, null=True)  # Field name made lowercase.
    estadocalidad = models.IntegerField(db_column='estadoCalidad', blank=True, null=True)  # Field name made lowercase.
    estadobloqueo = models.IntegerField(db_column='estadoBloqueo', blank=True, null=True)  # Field name made lowercase.
    codtela = models.ForeignKey('Tela', models.DO_NOTHING, db_column='codTela', blank=True, null=True)  # Field name made lowercase.
    codcolor = models.ForeignKey(Color, models.DO_NOTHING, db_column='codColor', blank=True, null=True)  # Field name made lowercase.
    codproceso = models.ForeignKey('Proceso', models.DO_NOTHING, db_column='codProceso', blank=True, null=True)  # Field name made lowercase.
    codpartida = models.ForeignKey(Partida, models.DO_NOTHING, db_column='codPartida', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)
    cantidadrl = models.IntegerField(db_column='cantidadRl')  # Field name made lowercase.
    prioridad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partidatelacolorsecuenciaproceso'


class Partidatelacolorsecuenciaprocesomaquinaparametro(models.Model):
    codpartidatelacolorsecuenciaprocesomaquinaparametro = models.CharField(db_column='codPartidaTelaColorSecuenciaProcesoMaquinaParametro', primary_key=True, max_length=191)  # Field name made lowercase.
    secuencia = models.IntegerField(blank=True, null=True)
    valornumerico = models.IntegerField(db_column='valorNumerico', blank=True, null=True)  # Field name made lowercase.
    valortexto = models.CharField(db_column='valorTexto', max_length=191, blank=True, null=True)  # Field name made lowercase.
    codpartida = models.ForeignKey(Partida, models.DO_NOTHING, db_column='codPartida', blank=True, null=True)  # Field name made lowercase.
    codtela = models.ForeignKey('Tela', models.DO_NOTHING, db_column='codTela', blank=True, null=True)  # Field name made lowercase.
    codcolor = models.ForeignKey(Color, models.DO_NOTHING, db_column='codColor', blank=True, null=True)  # Field name made lowercase.
    codproceso = models.ForeignKey('Proceso', models.DO_NOTHING, db_column='codProceso', blank=True, null=True)  # Field name made lowercase.
    codmaquina = models.ForeignKey(Maquina, models.DO_NOTHING, db_column='codMaquina', blank=True, null=True)  # Field name made lowercase.
    codparametromaquina = models.ForeignKey(Parametromaquina, models.DO_NOTHING, db_column='codParametroMaquina', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)
    valoractualizado = models.CharField(db_column='valorActualizado', max_length=191, blank=True, null=True)  # Field name made lowercase.
    valorinicial = models.CharField(db_column='valorInicial', max_length=191, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'partidatelacolorsecuenciaprocesomaquinaparametro'


class Partidatelacolorsecuenciaprocesomaquinapendiente(models.Model):
    codpartidatelacolorsecuenciaprocesomaquinapendiente = models.CharField(db_column='codPartidaTelaColorSecuenciaProcesoMaquinaPendiente', primary_key=True, max_length=191)  # Field name made lowercase.
    secuencia = models.IntegerField(blank=True, null=True)
    velocidad = models.IntegerField(blank=True, null=True)
    partidacodpartida = models.ForeignKey(Partida, models.DO_NOTHING, db_column='partidaCodPartida', blank=True, null=True)  # Field name made lowercase.
    colorcodcolor = models.ForeignKey(Color, models.DO_NOTHING, db_column='colorCodColor', blank=True, null=True)  # Field name made lowercase.
    procesocodproceso = models.ForeignKey('Proceso', models.DO_NOTHING, db_column='procesoCodProceso', blank=True, null=True)  # Field name made lowercase.
    maquinacodmaquina = models.ForeignKey(Maquina, models.DO_NOTHING, db_column='maquinaCodMaquina', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)
    codtela = models.ForeignKey('Tela', models.DO_NOTHING, db_column='codTela', blank=True, null=True)  # Field name made lowercase.
    fechafin = models.DateTimeField(db_column='fechaFin', blank=True, null=True)  # Field name made lowercase.
    fechainicio = models.DateTimeField(db_column='fechaInicio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'partidatelacolorsecuenciaprocesomaquinapendiente'


class Partidatelacolorsecuenciaprocesomaquinarealizado(models.Model):
    codpartidatelacolorsecuenciaprocesomaquinarealizado = models.CharField(db_column='codPartidaTelaColorSecuenciaProcesoMaquinaRealizado', primary_key=True, max_length=191)  # Field name made lowercase.
    secuencia = models.IntegerField(blank=True, null=True)
    fechainicio = models.DateTimeField(db_column='fechaInicio', blank=True, null=True)  # Field name made lowercase.
    fechafin = models.DateTimeField(db_column='fechaFin', blank=True, null=True)  # Field name made lowercase.
    fechainicioprogramada = models.DateTimeField(db_column='fechaInicioProgramada', blank=True, null=True)  # Field name made lowercase.
    fechafinprogramada = models.DateTimeField(db_column='fechaFinProgramada', blank=True, null=True)  # Field name made lowercase.
    maquinaprogramada = models.IntegerField(db_column='maquinaProgramada', blank=True, null=True)  # Field name made lowercase.
    fechaprogramada = models.DateTimeField(db_column='fechaProgramada', blank=True, null=True)  # Field name made lowercase.
    partidacodpartida = models.ForeignKey(Partida, models.DO_NOTHING, db_column='partidaCodPartida', blank=True, null=True)  # Field name made lowercase.
    colorcodcolor = models.ForeignKey(Color, models.DO_NOTHING, db_column='colorCodColor', blank=True, null=True)  # Field name made lowercase.
    procesocodproceso = models.ForeignKey('Proceso', models.DO_NOTHING, db_column='procesoCodProceso', blank=True, null=True)  # Field name made lowercase.
    maquinacodmaquina = models.ForeignKey(Maquina, models.DO_NOTHING, db_column='maquinaCodMaquina', blank=True, null=True)  # Field name made lowercase.
    operarioreal = models.ForeignKey(Operario, models.DO_NOTHING, db_column='operarioReal', blank=True, null=True)  # Field name made lowercase.
    operarioprogramado = models.ForeignKey(Operario, models.DO_NOTHING, db_column='operarioProgramado', related_name='partidatelacolorsecuenciaprocesomaquinarealizado_operarioprogramado_set', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)
    codtela = models.ForeignKey('Tela', models.DO_NOTHING, db_column='codTela', blank=True, null=True)  # Field name made lowercase.
    telacodtela = models.CharField(db_column='telaCodTela', max_length=191, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'partidatelacolorsecuenciaprocesomaquinarealizado'


class Partidatelasecuenciaprocesopdf(models.Model):
    codpartidatelasecuenciaprocesopdf = models.CharField(db_column='codPartidaTelaSecuenciaProcesoPdf', primary_key=True, max_length=191)  # Field name made lowercase.
    secuencia = models.IntegerField(blank=True, null=True)
    pdfindicaciones = models.CharField(db_column='pdfIndicaciones', max_length=191, blank=True, null=True)  # Field name made lowercase.
    pdfreceta = models.CharField(db_column='pdfReceta', max_length=191, blank=True, null=True)  # Field name made lowercase.
    pdfrecomendaciones = models.CharField(db_column='pdfRecomendaciones', max_length=191, blank=True, null=True)  # Field name made lowercase.
    obligatorioindicaciones = models.IntegerField(db_column='obligatorioIndicaciones', blank=True, null=True)  # Field name made lowercase.
    obligatorioreceta = models.IntegerField(db_column='obligatorioReceta', blank=True, null=True)  # Field name made lowercase.
    obligatoriorecomendaciones = models.IntegerField(db_column='obligatorioRecomendaciones', blank=True, null=True)  # Field name made lowercase.
    leidoindicaciones = models.IntegerField(db_column='leidoIndicaciones', blank=True, null=True)  # Field name made lowercase.
    leidoreceta = models.IntegerField(db_column='leidoReceta', blank=True, null=True)  # Field name made lowercase.
    leidorecomendaciones = models.IntegerField(db_column='leidoRecomendaciones', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)
    codpartida = models.ForeignKey(Partida, models.DO_NOTHING, db_column='codPartida', blank=True, null=True)  # Field name made lowercase.
    codtela = models.ForeignKey('Tela', models.DO_NOTHING, db_column='codTela', blank=True, null=True)  # Field name made lowercase.
    codproceso = models.ForeignKey('Proceso', models.DO_NOTHING, db_column='codProceso', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'partidatelasecuenciaprocesopdf'


class Pedidocomercial(models.Model):
    codpedidocomercial = models.CharField(db_column='codPedidoComercial', primary_key=True, max_length=191)  # Field name made lowercase.
    fechapedido = models.DateTimeField(db_column='fechaPedido', blank=True, null=True)  # Field name made lowercase.
    codcliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='codCliente', blank=True, null=True)  # Field name made lowercase.
    codtemporada = models.ForeignKey('Temporada', models.DO_NOTHING, db_column='codTemporada', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'pedidocomercial'


class Preferenciaatributomaquina(models.Model):
    codpreferenciaatributomaquina = models.CharField(db_column='codPreferenciaAtributoMaquina', primary_key=True, max_length=191)  # Field name made lowercase.
    valorpreferenciareceta = models.IntegerField(db_column='valorPreferenciaReceta', blank=True, null=True)  # Field name made lowercase.
    valorpreferenciagama = models.IntegerField(db_column='valorPreferenciaGama', blank=True, null=True)  # Field name made lowercase.
    valorcompatibilidadreceta = models.IntegerField(db_column='valorCompatibilidadReceta', blank=True, null=True)  # Field name made lowercase.
    valorcompatibilidadgama = models.IntegerField(db_column='valorCompatibilidadGama', blank=True, null=True)  # Field name made lowercase.
    stocksatisfaccion = models.DecimalField(db_column='stockSatisfaccion', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    codmaquina = models.ForeignKey(Maquina, models.DO_NOTHING, db_column='codMaquina', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'preferenciaatributomaquina'


class Preferenciaparametromaquina(models.Model):
    codpreferenciaparametromaquina = models.CharField(db_column='codPreferenciaParametroMaquina', primary_key=True, max_length=191)  # Field name made lowercase.
    valorpreferido = models.IntegerField(db_column='valorPreferido', blank=True, null=True)  # Field name made lowercase.
    stocksatisfaccion = models.DecimalField(db_column='stockSatisfaccion', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    valorcompatibilidad = models.IntegerField(db_column='valorCompatibilidad', blank=True, null=True)  # Field name made lowercase.
    codmaquina = models.ForeignKey(Maquina, models.DO_NOTHING, db_column='codMaquina', blank=True, null=True)  # Field name made lowercase.
    codparametromaquina = models.ForeignKey(Parametromaquina, models.DO_NOTHING, db_column='codParametroMaquina', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'preferenciaparametromaquina'


class Proceso(models.Model):
    codproceso = models.CharField(db_column='codProceso', primary_key=True, max_length=191)  # Field name made lowercase.
    descripcion = models.CharField(max_length=191, blank=True, null=True)
    tipoproceso = models.CharField(db_column='tipoProceso', max_length=191, blank=True, null=True)  # Field name made lowercase.
    proceso_calidad = models.IntegerField(db_column='proceso_Calidad', blank=True, null=True)  # Field name made lowercase.
    procesohumedo = models.IntegerField(db_column='procesoHumedo', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'proceso'


class Procesocalidad(models.Model):
    codprocesocalidad = models.CharField(db_column='codProcesoCalidad', primary_key=True, max_length=191)  # Field name made lowercase.
    descripcion = models.CharField(max_length=191, blank=True, null=True)
    codparametro = models.CharField(db_column='codParametro', max_length=191, blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)
    codproceso = models.ForeignKey(Proceso, models.DO_NOTHING, db_column='codProceso', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'procesocalidad'


class Tela(models.Model):
    codtela = models.CharField(db_column='codTela', primary_key=True, max_length=191)  # Field name made lowercase.
    descripcion = models.CharField(max_length=191, blank=True, null=True)
    codtipotela = models.ForeignKey('Tipotela', models.DO_NOTHING, db_column='codTipoTela', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)
    tela = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tela'


class Telaprocesocalidad(models.Model):
    codtelaprocesocalidad = models.CharField(db_column='codTelaProcesoCalidad', primary_key=True, max_length=191)  # Field name made lowercase.
    valorestandar = models.DecimalField(db_column='valorEstandar', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    codparametro = models.ForeignKey(Parametrocalidad, models.DO_NOTHING, db_column='codParametro', blank=True, null=True)  # Field name made lowercase.
    codtela = models.ForeignKey(Tela, models.DO_NOTHING, db_column='codTela', blank=True, null=True)  # Field name made lowercase.
    codcolor = models.ForeignKey(Color, models.DO_NOTHING, db_column='codColor', blank=True, null=True)  # Field name made lowercase.
    codproceso = models.ForeignKey(Proceso, models.DO_NOTHING, db_column='codProceso', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)
    resultado = models.IntegerField(blank=True, null=True)
    valor = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'telaprocesocalidad'


class Temporada(models.Model):
    codtemporada = models.CharField(db_column='codTemporada', primary_key=True, max_length=191)  # Field name made lowercase.
    descripcion = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'temporada'


class Tipocliente(models.Model):
    codtipocliente = models.CharField(db_column='codTipoCliente', primary_key=True, max_length=191)  # Field name made lowercase.
    descripcion = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'tipocliente'


class Tipotela(models.Model):
    codtipotela = models.CharField(db_column='codTipoTela', primary_key=True, max_length=191)  # Field name made lowercase.
    descripcion = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'tipotela'


class Ubicacion(models.Model):
    codubicacion = models.CharField(db_column='codUbicacion', primary_key=True, max_length=191)  # Field name made lowercase.
    descripcion = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'ubicacion'


class Usuario(models.Model):
    usuario = models.CharField(primary_key=True, max_length=191)
    codoperario = models.OneToOneField(Operario, models.DO_NOTHING, db_column='codOperario')  # Field name made lowercase.
    nombre = models.CharField(max_length=191, blank=True, null=True)
    clave = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'usuario'


class Valorgama(models.Model):
    codvalorgama = models.CharField(db_column='codValorGama', primary_key=True, max_length=191)  # Field name made lowercase.
    gamaorigen = models.CharField(db_column='gamaOrigen', max_length=191, blank=True, null=True)  # Field name made lowercase.
    gamasiguiente = models.CharField(db_column='gamaSiguiente', max_length=191, blank=True, null=True)  # Field name made lowercase.
    valor = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'valorgama'


class Valorreceta(models.Model):
    codvalorreceta = models.CharField(db_column='codValorReceta', primary_key=True, max_length=191)  # Field name made lowercase.
    recetaorigen = models.CharField(db_column='recetaOrigen', max_length=191, blank=True, null=True)  # Field name made lowercase.
    recetasiguiente = models.CharField(db_column='recetaSiguiente', max_length=191, blank=True, null=True)  # Field name made lowercase.
    valor = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(db_column='createdAt', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updatedAt', auto_now=True)

    class Meta:
        managed = False
        db_table = 'valorreceta'
