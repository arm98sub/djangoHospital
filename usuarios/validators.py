from django.core.validators import RegexValidator, FileExtensionValidator

rfc_validador = RegexValidator(
    regex='^([A-ZÑ&]{3,4}) ?(?:- ?)?(\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])) ?(?:- ?)?([A-Z\d]{2})([A\d])$',
    message='El RFC no tiene un formato valido',
    code = 'rfc_invalido'
)

foto_validador = FileExtensionValidator(
    allowed_extensions= ['png', 'gif'],
    message= 'Solo se permiten imagenes png, gif',
    code= 'imagen_invalida'
)