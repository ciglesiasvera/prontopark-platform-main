def global_context(request):

    user_role = request.user.role if request.user.is_authenticated else None

    context = {
        "user_roles": {
            "supervisor": "dashboards:supervisor",
            "admin": "dashboards:admin",
            "concierge": "dashboards:concierge",
            "parking_owner": "dashboards:parking_owner",
            "resident": "dashboards:resident",
            "visit": "dashboards:visit",
        }
    }

    supervisor = {
        "usuarios": [
            {"url": "users:register_resident", "title": "Registrar residente"},
            {
                "url": "users:register_parking_owner",
                "title": "Registrar propietario de estacionamiento",
            },
            {"url": "users:register_concierge", "title": "Registrar conserje"},
            {"url": "users:register_admin", "title": "Registrar administrador"},
            {"url": "users:user_list", "title": "Listar usuarios"},
        ],
        "estacionamientos": [
            {
                "url": "parkings:parking_create",
                "title": "Crear estacionamiento",
            },
            {"url": "parkings:lot_create", "title": "Crear lote"},
            {"url": "parkings:parking_list", "title": "Listar estacionamientos"},
            {"url": "parkings:lot_list", "title": "Listar lotes"},
        ],
        "residencias": [
            {
                "url": "residences:residence_create",
                "title": "Crear residencia",
            },
            {"url": "residences:blockname_create", "title": "Crear bloque"},
            {"url": "residences:residence_list", "title": "Listar residencias"},
            {"url": "residences:blockname_list", "title": "Listar bloques"},
        ],
        "reservas": [
            {
                "url": "reservations:create",
                "title": "Solicitar reserva",
            },
            {"url": "reservations:list", "title": "Listar reservas"},
        ],
    }

    admin = {
        "usuarios": [
            {"url": "users:register_resident", "title": "Registrar residente"},
            {
                "url": "users:register_parking_owner",
                "title": "Registrar propietario de estacionamiento",
            },
            {"url": "users:register_concierge", "title": "Registrar conserje"},
            {"url": "users:user_list", "title": "Listar usuarios"},
        ],
        "estacionamientos": [
            {
                "url": "parkings:parking_create",
                "title": "Crear estacionamiento",
            },
            {"url": "parkings:lot_create", "title": "Crear lote"},
            {"url": "parkings:parking_list", "title": "Listar estacionamientos"},
            {"url": "parkings:lot_list", "title": "Listar lotes"},
        ],
        "residencias": [
            {
                "url": "residences:residence_create",
                "title": "Crear residencia",
            },
            {"url": "residences:blockname_create", "title": "Crear bloque"},
            {"url": "residences:residence_list", "title": "Listar residencias"},
            {"url": "residences:blockname_list", "title": "Listar bloques"},
        ],
        "reservas": [
            {
                "url": "reservations:create",
                "title": "Solicitar reserva",
            },
            {"url": "reservations:list", "title": "Listar reservas"},
        ],
    }

    concierge = {
        "estacionamientos": [
            {
                "url": "parkings:parking_create",
                "title": "Crear estacionamiento",
            },
            {"url": "parkings:parking_list", "title": "Listar estacionamientos"},
            {"url": "parkings:lot_list", "title": "Listar lotes"},
        ],
        "residencias": [
            {"url": "residences:residence_list", "title": "Listar residencias"},
            {"url": "residences:blockname_list", "title": "Listar bloques"},
        ],
        "reservas": [
            {
                "url": "reservations:create",
                "title": "Solicitar reserva",
            },
            {"url": "reservations:list", "title": "Listar reservas"},
        ],
    }

    parking_owner = {
        "estacionamientos": [
            {"url": "parkings:parking_list", "title": "Listar estacionamientos"},
            {"url": "parkings:lot_list", "title": "Listar lotes"},
        ],
        "residencias": [
            {"url": "residences:residence_list", "title": "Listar residencias"},
            {"url": "residences:blockname_list", "title": "Listar bloques"},
        ],
        "reservas": [
            {
                "url": "reservations:create",
                "title": "Solicitar reserva",
            },
            {"url": "reservations:list", "title": "Listar reservas"},
        ],
    }

    resident = {
        "estacionamientos": [
            {"url": "parkings:parking_list", "title": "Listar estacionamientos"},
            {"url": "parkings:lot_list", "title": "Listar lotes"},
        ],
        "residencias": [
            {"url": "residences:residence_list", "title": "Listar residencias"},
            {"url": "residences:blockname_list", "title": "Listar bloques"},
        ],
        "reservas": [
            {
                "url": "reservations:create",
                "title": "Solicitar reserva",
            },
            {"url": "reservations:list", "title": "Listar reservas"},
        ],
    }
    
    visit = {
       
    }

    if user_role == "supervisor":
        context["menu"] = supervisor
    elif user_role == "admin":
        context["menu"] = admin
    elif user_role == "concierge":
        context["menu"] = concierge
    elif user_role == "parking_owner":
        context["menu"] = parking_owner
    elif user_role == "resident":
        context["menu"] = resident
    elif user_role == "visit":
        context["menu"] = visit

    return context
