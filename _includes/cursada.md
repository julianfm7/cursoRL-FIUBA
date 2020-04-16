{% assign clases = cursada | sort %}
{% for clase_hash in clases reversed %}
{% assign numero_clase = clase_hash[0] | plus:0 %}
{% assign clase = clase_hash[1] %}

## [Clase {{numero_clase}}](#clase-{{numero_clase}}){: .titulo-clase}
{{clase.descripcion}}

{% if clase.entrega %}

### Para entregar
{% assign fecha = clase.entrega.fecha %}
La fecha límite para la entrega de esta clase es el <strong>{% include fecha-formato-humano.md fecha=fecha %}</strong>.

{% assign ejercicios = clase.entrega.ejercicios %}
{% if ejercicios %}
{% include ejercicios-github.html ejercicios=ejercicios %}
{% endif %}

{% assign guias = clase.entrega.mumuki %}
{% if guias %}
**Mumuki**
{% include ejercicios-mumuki.md guias=guias %}
{% endif %}

{{clase.entrega.descripcion}}

{% endif %}

{% if clase.ejercicios %}

### Ejercicios para trabajar en clase
{% assign ejercicios = clase.ejercicios %}
{% include ejercicios-github.html ejercicios=ejercicios %}

{% if clase.textoEjercicios %}
{{clase.textoEjercicios}}
{% endif %}

{% endif %}

{% if clase.mumuki %}

### Mumuki

Te recomendamos resolver las guías:
{% assign guias = clase.mumuki %}
{% include ejercicios-mumuki.md guias=guias %}

{% endif %}

{% if forloop.last == false %}
<hr class="titulo-clase">
{% endif %}

{% endfor %}
