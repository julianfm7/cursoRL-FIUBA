---
items:
  - nombre: Markov chain
    descripcion: bla bla
  - nombre: Markov decision process
    descripcion: (completar)
  - nombre: Value function
    descripcion: (completar)
---

# Glosario

{% for item in page.items %}
* **{{item.nombre}}:** {{item.descripcion}}
{% endfor %}
