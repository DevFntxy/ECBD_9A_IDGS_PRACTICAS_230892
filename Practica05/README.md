## Objetivo general
Generar un dataset clínico simulado de 5,000 pacientes del estado de Puebla que sirva como base para prácticas de clasificación, visualización y análisis supervisado sobre riesgo cardiovascular.

## Descripción
Datos ficticios y de uso exclusivamente académico. No contiene información real ni datos personales identificables.

## Atributos del dataset
Cada registro representa un paciente y contiene las siguientes columnas:
- patient_id: identificador único (string)
- sexo: Masculino / Femenino
- edad: años (18 - 99)
- municipio: municipio de residencia (Puebla)
- localidad: tipo de localidad (Urbana / Rural)
- latitud: coordenada (aprox. Puebla)
- longitud: coordenada (aprox. Puebla)
- peso_kg: peso en kilogramos (40 - 160)
- estatura_cm: estatura en centímetros (140 - 210)
- imc: índice de masa corporal (calculado)
- presion_sistolica: mmHg (90 - 220)
- presion_diastolica: mmHg (60 - 140)
- glucosa_mg_dl: mg/dL en ayunas (60 - 300)
- colesterol_mg_dl: mg/dL (100 - 350)
- colesterol_hdl: mg/dL (20 - 100)
- colesterol_ldl: mg/dL (30 - 250)
- fuma: Sí / No
- actividad_fisica: Baja / Moderada / Alta
- diabetes: Sí / No
- hipertension: Sí / No
- antecedentes_familiares: Sí / No
- medicacion: Sí / No (medicación cardiovascular relevante)
- riesgo_cardio: Bajo / Medio / Alto (variable objetivo multiclasificadora)

## Reglas de generación de datos (resumen)
- Edad: distribución realista centrada en adultos (18-99).
- Peso/estatura: rangos realistas; IMC = peso_kg / (estatura_m)^2.
- Presión arterial, glucosa y lípidos: valores dentro de rangos clínicos plausibles; introducir ruido y casos extremos simulados.
- Variables categóricas: asignadas por probabilidades que dependan de edad y comorbilidades (ej. mayor edad -> mayor probabilidad de hipertensión).
- Riesgo cardiovascular: calculado mediante reglas heurísticas combinando IMC, presión, glucosa, colesterol, tabaquismo, diabetes e hipertensión para clasificar en Bajo/Medio/Alto.


## Validaciones y limpieza (a realizar en notebook)
- Confirmar dimensiones: 5000 filas x N columnas
- Verificar nombres de columnas y tipos de datos
- Detectar y manejar nulos
- Eliminar duplicados
- Validar rangos clínicos y corregir valores fuera de rango
- Verificar correspondencia geográfica con Puebla

