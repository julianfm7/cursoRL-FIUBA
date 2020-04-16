# Sitio de Reinforcememt Learning - FIUBA - 2020 cuat. 1

Este sitio está construido utilizando [Jekyll](https://jekyllrb.com/), un pequeño motor que compila el sitio antes de publicarlo y nos permite "programar" algunas pequeñas cosas: usar variables, foreach, templates, vistas parciales, etc.

<!---
Se explican debajo algunas particularidades para poder agregar información al sitio.

### Cómo agregar clases en la cursada

La descripción de las clases que aparecen en la sección "Cursada" se genera a partir de los archivos que están en la carpeta `_data/clases`, aprovechando la funcionalidad de [data files](https://jekyllrb.com/docs/datafiles/) que ofrece Jekyll.

Para crear una clase nueva hay que agregar un archivo con extensión `yml`, con un formato particular y nombrado según la clase que representa (ej: `1.yml` para la primera clase, `2.yml` para la segunda, etc.).

La recomendación es mirar alguno que ya exista, pero va una explicación de qué contiene:

```yml
descripcion: |
  Todo lo que esté acá va a aparecer como descripción. Vale **usar Markdown**.
  Todos los campos son opcionales, incluido este.

ejercicios:         # Se pueden poner varios, notar el guión antes de cada item
  - name: Sueldo de Pepe (inicial)                        # nombre del ejercicio
    repo: obj1-unahur/sueldo-pepe-inicial                 # slug del repo GitHub (o sea, lo que viene después de github.com/...)
    classroom: https://classroom.github.com/a/K5Q_OYMF    # URL de GitHub Classroom
  - name: Multipepita                                     
    repo: wollok/multipepita
    classroom: https://classroom.github.com/a/4pxDNIhk

mumuki:             # Se puede poner solo una
  guia: Personas y barrios - qué anda, qué no, cuánto da
  url: https://mumuki.io/wollok-obj1/lessons/482-objetos-y-mensajes-personas-y-barrios-que-anda-que-no-cuanto-da
```
--->