{% for guia in guias %}
* [{{guia.nombre}}]({{guia.url}}). {% if guia.ejercicios %}Ejercicios {{guia.ejercicios}}.{% endif %}
{% endfor %}
