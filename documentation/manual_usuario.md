# Manual de usuario

## 1. Objetivo

Este manual lo hicimos para que cualquier integrante del grupo pueda ejecutar **Bayes Web Diagnosis** sin enredarse.

El sistema recibe sintomas observados (evidencia) y calcula probabilidades posteriores de una causa, por ejemplo:

`P(BaseDatosCaida | evidencia)`

---

## 2. Requisitos

- Python 3.8 o superior (recomendado 3.10+)
- Terminal (macOS, Linux o Windows)
- Archivos del proyecto descargados

No se requieren librerias externas.

---

## 3. Archivos necesarios para ejecutar

Asegura que existan estos archivos en la raiz del proyecto:

- `main.py`
- `model.py`
- `inference.py`
- `bayesian_network.py`
- `node.py`
- `scenarios.py`
- `utils.py`

---

## 4. Ejecucion del programa

Desde la carpeta del proyecto:

```bash
python3 main.py
```

En Windows, si `python3` no existe:

```bash
python main.py
```

---

## 5. Menu principal

Al iniciar, se muestra este menu:

1. Ejecutar consulta manual
2. Ejecutar escenarios de prueba
3. Mostrar estructura de la red
4. Salir

### Opcion 1: Ejecutar consulta manual

Permite elegir una variable de consulta e ingresar evidencia variable por variable.

Reglas de entrada:

- `s` = si (True)
- `n` = no (False)
- `d` = desconocido (se ignora esa variable)

Tambien acepta equivalentes como `si`, `no`, `true`, `false`, `1`, `0`, `?`.

### Opcion 2: Ejecutar escenarios de prueba

Ejecuta automaticamente los escenarios definidos en `scenarios.py`.

### Opcion 3: Mostrar estructura de la red

Muestra cada nodo y sus padres para validar dependencias causales.

### Opcion 4: Salir

Cierra la aplicacion.

---

## 6. Flujo recomendado de uso (paso a paso)

1. Ejecutar el programa.
2. Elegir `3` para revisar la estructura de la red.
3. Volver al menu y elegir `2` para ver resultados de escenarios base.
4. Volver al menu y elegir `1` para consultas personalizadas.
5. Seleccionar variable de consulta.
6. Ingresar evidencia con `s`, `n` o `d`.
7. Leer probabilidades para el caso `si` y `no`.
8. Repetir con nuevas evidencias para comparar comportamiento.

Nota rapida:
Si estas probando para exponer, primero corre escenarios y luego haz una consulta manual corta.

---

## 7. Ejemplo completo de consulta manual

Entrada:

- Consulta: `BaseDatosCaida`
- Evidencia:
  - `Error500 = si`
  - `LatenciaAlta = si`
  - `LoginFallido = no`
  - Resto: `desconocido`

Salida esperada (aprox):

- `P(BaseDatosCaida=si | evidencia) = 0.2824`
- `P(BaseDatosCaida=no | evidencia) = 0.7176`

Interpretacion:

- La evidencia aumenta la probabilidad de una falla interna, pero con esta configuracion de CPT todavia predomina el estado `no`.

---

## 8. Como interpretar resultados

El sistema siempre devuelve una distribucion valida:

- `P(variable=si | evidencia)`
- `P(variable=no | evidencia)`

Estas dos probabilidades suman 1.0.

Interpretacion rapida:

- Si `P(si)` esta cerca de 1: causa altamente probable.
- Si `P(si)` esta cerca de 0.5: evidencia ambigua o no concluyente.
- Si `P(si)` esta cerca de 0: causa poco probable con esa evidencia.

---

## 9. Manejo de entradas invalidas

El menu ahora valida entradas y muestra mensajes claros.

Casos contemplados:

- Opcion fuera del menu: muestra `Opcion invalida`.
- Variable de consulta fuera de rango: solicita de nuevo.
- Evidencia invalida (ej. `abc`): solicita de nuevo esa variable.
- Consulta cancelada: en seleccion de variable usar `0` para volver.

---

## 10. Problemas frecuentes y solucion

### El programa no inicia

- Verifica version de Python con `python3 --version`.
- Ejecuta desde la carpeta raiz del proyecto.

### Error de modulo no encontrado

- Asegura que todos los archivos `.py` esten en la raiz.
- No cambies nombres de archivos sin ajustar imports.

### Resultados inesperados

- Revisa que la evidencia se haya ingresado correctamente.
- Revisa valores de CPT en `model.py`.
- Compara con escenarios predefinidos en `scenarios.py`.

---

## 11. Checklist rapido para demostracion

Antes de exponer:

1. Ejecutar `python3 main.py`.
2. Mostrar opcion `3` (estructura de la red).
3. Ejecutar opcion `2` (escenarios).
4. Ejecutar al menos una consulta manual (opcion `1`).
5. Explicar brevemente por que la probabilidad sube o baja segun evidencia.

Con este flujo, la demostracion queda clara y ordenada para profesor y companeros.
