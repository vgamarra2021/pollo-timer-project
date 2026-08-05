from db.models.session import Session

def create_action(session: Session, type: str):
    #Insertar en BD la action relacionada a la session pasada como parámetro
    pass

def create_session():
    #Insertar nueva session en la BD y devolverla
    pass

def get_last_session():
    #Hacer un select y traer la última session de la BD
    pass

def complete_session(session: Session):
    #Actualizar la session pasada como parámetro en la BD, seteando is_active a False y finish_at a la fecha actual
    pass

def process_action(type: str):
    
    last_session = get_last_session()
    
    if(type) == "play":
        if(last_session is None or not last_session.is_active):
            session = create_session()
            create_action(session, type)
        else: # Cuando se reanuda luego de una pausa
            create_action(last_session, type)

    elif(type) == "pause":
        create_action(last_session, type)

    elif(type) == "stop":
        create_action(last_session, type)
        complete_session(last_session)
