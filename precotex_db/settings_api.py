from apps.authentication.models import Role, Employee, User
from apps.kanban import models as kb
from apps.tareo import models as tr
from apps.seleccion import models as sl
from apps.capacidad import models as cp

URL = 'http://200.48.88.134:8050'

REQUESTS = {
    '/api/Empleado/ConsultaRoles' :  {
        'model': Role,
        'attributes': {
            'cod_Rol': 'code',
            'nom_Rol': 'description',
        }
    },
    '/api/Empleado/ConsultaEmpleados' :  {
        'model': Employee,
        'attributes': {
            'cod_Empleado': 'code',
            'cod_Rol': {
                'model': Role,
                'value': 'role_code',
                'pk': 'code'
            },
            'cod_Usuario': {
                'model': User,
                'value': 'user',
                'pk': 'username'
            },
            'nom_Empleado': 'name',
        }
    },
    '/api/Calidad/ConsultaTipoCalidad' :  {
        'model': kb.QualityType,
        'attributes': {
            'cod_TipoCalidad': 'code',
            'des_TipoCalidad': 'name',
        }
    },
    '/api/Calidad/ConsultaCampoCalidad' :  {
        'model': kb.QualityField,
        'attributes': {
            'cod_TipoCalidadDet': 'code',
            'nom_TipoCalidadDet': 'name',
            'cod_TipoCalidad': {
                'model': kb.QualityType,
                'value': 'type_quality_code',
                'pk': 'code'
            },
            'des_TipoCalidadDet': 'description',
            'valorEstandar': 'standard_value',
            'minimoAprobacion': 'min_approval',
            'maximoAprobacion': 'max_approval',
            'minimoAlerta': 'min_alert',
            'maximoAlerta': 'max_alert',
            'evaluable': 'evaluable',
        }
    },
    '/api/Cliente/ConsultaClientes' :  {
        'model': kb.Client,
        'attributes': {
            'cod_Cliente': 'code',
            'correo': 'email',
            'nom_Cliente': 'name',
            'telefono': 'phone',
            'direccion': 'address',
        }
    },
    '/api/Partida/ConsultaPedido' :  {
        'model': kb.Order,
        'attributes': {
            'cod_Pedido': 'code',
            'cod_Cliente': {
                'model': kb.Client,
                'value': 'client_code',
                'pk': 'code'
            },
        }
    },
    '/api/Partida/ConsultaPartida' :  {
        'model': kb.Item,
        'attributes': {
            'cod_Partida': 'code',
            'cod_Pedido': {
                'model': kb.Order,
                'value': 'order_code',
                'pk': 'code'
            },
            'fec_Limite_Entrega': 'delivery_deadline',
        }
    },
    '/api/Tela/ConsultaTipoTejido' :  {
        'model': kb.FabricType,
        'attributes': {
            'cod_Tipo_Tejido': 'code',
            'des_Tipo_Tejido': 'description',
        }
    },
    '/api/Tela/ConsultaFamiliaTejido' :  {
        'model': kb.FabricFamily,
        'attributes': {
            'cod_Fam_Tejido': 'code',
            'des_Fam_Tejido': 'description',
        }
    },  
    '/api/Tela/ConsultaRuta' :  {
        'model': kb.Route,
        'attributes': {
            'cod_Ruta': 'code',
            'nom_Ruta': 'name',
        }
    },
    '/api/Color/ConsultaColor' :  {
        'model': kb.Color,
        'attributes': {
            'cod_Color': 'code',
            'des_Color': 'description',
        }
    },
    '/api/Tela/ConsultaTelas' :  {
        'model': kb.Fabric,
        'attributes': {
            'cod_Tela': 'code',
            'des_Tela': 'description',
            'cod_Color': {
                'model': kb.Color,
                'value': 'color_code',
                'pk': 'code'
            },
            'cod_Tipo_Tejido': {
                'model': kb.FabricType,
                'value': 'fabric_type_code',
                'pk': 'code'
            },
            'cod_Fam_Tejido': {
                'model': kb.FabricFamily,
                'value': 'fabric_family_code',
                'pk': 'code'
            },
            'cod_Ruta': {
                'model': kb.Route,
                'value': 'route_code',
                'pk': 'code'
            },
        }
    },
    '/api/Maquina/ConsultaRazon' :  {
        'model': kb.Reason,
        'attributes': {
            'cod_Razon': 'code',
            'descripcion': 'description',
        }
    },
    '/api/Partida/ConsultaPartidaTela' :  {
        'model': kb.FabricBatch,
        'attributes': {
            'cod_Partida': {
                'model': kb.Item,
                'value': 'batch_code',
                'pk': 'code'
            },
            'cod_Tela': {
                'model': kb.Fabric,
                'value': 'fabric_code',
                'pk': 'code'
            },
            'cant_Procesar': 'process_quantity',
            'unid_Medida': 'unit_of_measure',
            'fec_Limite_Entrega': 'target_date',
            'tipo_Destino': 'destination_type',
            'tipo_Embalaje': 'packaging_type',
            'tipo_Produccion': 'production_type',
            'observaciones': 'observations',
        }
    },
    '/api/Tela/ConsultaProcesos' :  {
        'model': kb.Process,
        'attributes': {
            'cod_Proceso': 'code',
            'nom_Proceso': 'name',
        }
    },
    '/api/Maquina/ConsultaMaquinas' :  {
        'model': tr.Machinery,
        'attributes': {
            'cod_Maquina': 'code',
            'des_Maquina': 'description',
            "linea": "line",
            "maq_base": {
                'model': tr.BaseMachinery,
                'value': 'base_machinery_code',
                'pk': 'code'
            },
        }
    },
    '/api/Tela/ConsultaProcesoTela' :  {
        'model': kb.FabricProcess,
        'attributes': {
            'cod_Proceso': {
                'model': kb.Process,
                'value': 'process_code',
                'pk': 'code'
            },
            'cod_Tela': {
                'model': kb.Fabric,
                'value': 'fabric_code',
                'pk': 'code'
            },
        }
    },
    '/api/Maquina/ConsultaParadas' :  {
        'model': kb.Stop,
        'attributes': {
            'cod_Maquina': {
                'model': kb.Machinery,
                'value': 'machinery_code',
                'pk': 'code'
            },
            'cod_Razon': {
                'model': kb.Reason,
                'value': 'reason_code',
                'pk': 'code'
            },
            'fec_Hora_Inicio': 'start_datetime',
            'fec_Hora_Fin': 'real_completion_datetime',
        }
    },
    '/api/Tela/ConsultaRutaProceso' :  {
        'model': kb.RoutePoint,
        'attributes': {
            'cod_Proceso': {
                'model': kb.Process,
                'value': 'process_code',
                'pk': 'code'
            },
            'cod_Ruta': {
                'model': kb.Route,
                'value': 'route_code',
                'pk': 'code'
            },
            'secuencia': 'sequence',
        }
    },
     '/api/Tela/ConsultaRolloTela' :  {
        'model': kb.FabricRoll,
        'attributes': {
            'cod_Rollo': 'code',
            'cod_Partida': {
                'model': kb.FabricBatch,
                'value': 'fabric_batch_code',
                'pk': [
                    ['cod_Partida', 'batch_code'],
                    ['cod_Tela', 'fabric_code'],
                ]
            },
            'kilos': 'kilograms'
        }
    },
}