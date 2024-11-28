import re 
import wave
from werkzeug.utils import secure_filename
from io import BytesIO

def validate_required_fields(data, required_fields):
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Faltan los siguientes campos: {', '.join(missing_fields)}"
    return True, ""

def validate_non_blank_fields(data, fields_to_check):
    blank_fields = [
        field for field in fields_to_check
        if field in data and isinstance(data[field], str) and data[field].strip() == ''
    ]
    if blank_fields:
        return False, f"Los siguientes campos no pueden estar vacíos: {', '.join(blank_fields)}"
    return True, ""

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return False, "El formato del correo electrónico no es válido"
    return True, ""

def validate_personal_ID(personal_ID):
    if len(str(personal_ID)) < 6 or not int(personal_ID):
        return False, "El formato del DNI no es válido"
    return True, ""

def validate_phone_number(phone_number):
    if not isinstance(phone_number, str):
        return False, "El número de teléfono debe ser una cadena."
    
    phone_regex = r'^[\d\-\(\)]{6,16}$'
    if not re.match(phone_regex, phone_number):
        return False, "El número de teléfono debe tener entre 6 y 16 caracteres, y solo puede contener dígitos, guiones o paréntesis."
    return True, ""

def validate_user_type(user_type):
    valid_types = ['creator', 'buyer']
    if user_type not in valid_types:
        return False, f"El tipo de usuario debe ser uno de los siguientes: {', '.join(valid_types)}"
    return True, ""

def validate_account_type(user_type):
    valid_types = ['cbu', 'cvu']
    if user_type not in valid_types:
        return False, f"El tipo de cuenta bancaria debe ser uno de los siguientes: {', '.join(valid_types)}"
    return True, ""

@staticmethod
def validate_user(data, action="create"):
    required_fields = ["pwd", "personal_ID", "phone_number", "type", "username", "full_name"]

    if action == "create":
        required_fields.append("email")

    valid, message = validate_required_fields(data, required_fields)
    if not valid:
        return False, message
    
    valid, message = validate_non_blank_fields(data, required_fields)
    if not valid:
        return False, message
    
    if action == "create":
        valid, message = validate_email(data.get("email"))
        if not valid:
            return False, message
    
    valid, message = validate_phone_number(data.get("phone_number"))
    if not valid:
        return False, message
    
    valid, message = validate_personal_ID(data.get("personal_ID"))
    if not valid:
        return False, message
    
    valid, message = validate_user_type(data.get("type"))
    if not valid:
        return False, message
    
    return True, ""
    
@staticmethod
def validate_creator(data):
    required_fields = ["profile", "subscription_ID", "personal_account_ID","account_type"]

    valid, message = validate_required_fields(data, required_fields)
    if not valid:
        return False, message
    
    valid, message = validate_non_blank_fields(data, required_fields)
    if not valid:
        return False, message
    
    valid, message = validate_account_type(data.get("account_type"))
    if not valid:
        return False, message
    
    return True, ""

def validate_BPM(bpm):
    if bpm is None or (isinstance(bpm, str) and len(bpm) <= 0) or not int(bpm) or int(bpm) < 0 or int(bpm) > 350:
        return False, "El valor del BPM no es válido"
    return True, ""

def validate_audio_file(file):
    ALLOWED_EXTENSIONS = {'wav'}
    MAX_FILE_SIZE = 4_300_000
    filename = secure_filename(file.filename)
    if not ('.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
        return False, "El formato del archivo no es válido, sólo se permite .WAV"
    
    file.seek(0, 2)  # Ir al final del archivo para obtener el tamaño
    file_size = file.tell()
    if file_size > MAX_FILE_SIZE:
        return False, "El archivo excede el tamaño máximo permitido de 4 MB"

    file.seek(0) # Resetear el puntero del archivo
    
    file_data = BytesIO(file.read())
    file.seek(0)  # Resetear el puntero del archivo 
    with wave.open(file_data, 'rb') as wav_file:
        params = wav_file.getparams()
        if params.nchannels < 1 or params.framerate <= 0:
            return False, "El formato del archivo no es válido, sólo se permite .WAV"
    
    return True, ""

def validate_audio(data, file, action="create"):
    required_fields = ['audio_name', 'category', 'genre', 'BPM', 'tone', 'length', 'size', 'description', 'price', 'creator_ID']

    valid, message = validate_required_fields(data, required_fields)
    if not valid:
        return False, message
    
    valid, message = validate_non_blank_fields(data, required_fields)
    if not valid:
        return False, message
        
    valid, message = validate_BPM(data.get("BPM"))
    if not valid:
        return False, message
    
    if(action=='create'):
        valid, message = validate_audio_file(file)
        if not valid:
            return False, message
    
    return True, ""

def validate_purchase(data):
    required_fields = ["buyer_ID", "flow_type", "payment_method", "items"]

    valid, message = validate_required_fields(data, required_fields)
    if not valid:
        return False, message
    
    valid, message = validate_non_blank_fields(data, required_fields)
    if not valid:
        return False, message

    for item in data.get("items", []):
        item_required_fields = ["item_ID", "audio_ID", "creator_ID", "price"]
        
        valid, message = validate_required_fields(item, item_required_fields)
        if not valid:
            return False, message
        
        valid, message = validate_non_blank_fields(item, item_required_fields)
        if not valid:
            return False, message    
    
    return True, ""