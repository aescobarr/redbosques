from django.core.exceptions import ValidationError
from redbosques_main.models import TeIndicador
from django.contrib import messages


'''def validate_numesparb(value):
    numesparb = TeIndicador.filter(variable_rodal='numesparb').values('val_minimo', 'val_alerta', 'val_maximo')

    numesparb_limits = []
    for i in numesparb:
        numesparb_limits.append({'min': i.val_minimo, 'alerta': i.val_alerta, 'max': i.val_maximo})

    if value < numesparb_limits.min:
        raise ValidationError("El valor es inferior al permitido.")
    elif value == numesparb_limits.alerta:
        messages.warning(value, 'OJO CUIDAO !!')
    elif value > numesparb_limits.max:
        raise ValidationError("El valor es mayor al permitido.")
    else:
        return value'''
