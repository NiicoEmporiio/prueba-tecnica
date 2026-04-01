# 🧪 Prueba Técnica DevOps – HESK + Zabbix + CI/CD

## 📌 Descripción general

Este proyecto implementa una **plataforma DevOps mínima funcional (POC)** que integra:

* Sistema de tickets **HESK**
* Monitoreo con **Zabbix**
* Automatización de categorías mediante **CI/CD**
* Infraestructura definida con **Docker Compose**

---

## 🧠 Arquitectura

La solución está compuesta por los siguientes servicios:

* **HESK Web** → sistema de tickets
* **MariaDB (HESK)** → base de datos de HESK
* **Zabbix Server** → motor de monitoreo
* **Zabbix Web** → interfaz de monitoreo
* **MySQL (Zabbix)** → base de datos de Zabbix
* **Zabbix Agent** → agente para métricas del sistema

Todos los servicios corren en una **red Docker interna** con volúmenes persistentes.

---

## 🐳 Despliegue

### Requisitos

* Docker
* Docker Compose
* Git

### Levantar el entorno

```bash
docker compose up -d --build
```

### Verificar estado

```bash
docker ps
```

---

## 🌐 Accesos

### HESK

* URL: http://localhost:8080
* Usuario: admin
* Password: 116882

### Zabbix

* URL: http://localhost:8081
* Usuario: Admin
* Password: zabbix

---

## 📊 Monitoreo (Zabbix)

Se configuró monitoreo sobre la URL de HESK.

### Indicador 1: Disponibilidad HTTP

* Valida código HTTP = 200
* Trigger:

```text
last(/HESK/web.test.fail[HESK Web Check])<>0
```

### Indicador 2: Tiempo de respuesta

* Mide tiempo de respuesta
* Trigger:

```text
last(/HESK/web.test.time[HESK Web Check,Home,resp])>2
```

### Validaciones

* Visualización de código HTTP ✔
* Métricas históricas ✔
* Gráficos ✔
* Alertas ante caída ✔
* Recuperación automática ✔

---

## 🔄 Automatización CI/CD

### Archivo declarativo

```
categories.txt
```

Ejemplo:

```
Infraestructura
Aplicaciones
Redes
Seguridad
```

---

### Flujo

1. Editar `categories.txt`
2. Hacer commit y push
3. Se ejecuta GitHub Actions automáticamente
4. El pipeline:

   * Lee el archivo
   * Compara con la DB
   * Inserta solo nuevas categorías
   * Evita duplicados (idempotente)

---

### Script utilizado

```
scripts/sync_categories.py
```

### Características

* Idempotente ✔
* No duplica datos ✔
* Inserta solo nuevas categorías ✔
* Log detallado ✔

---

### Ejemplo de log

```
Categorías leídas: 19
Existentes: 18
Nuevas: 1
Insertadas correctamente
```

---

## ⚙️ Variables de entorno

Se utilizan variables en `docker-compose.yml`:

* MYSQL_DATABASE
* MYSQL_USER
* MYSQL_PASSWORD
* MYSQL_ROOT_PASSWORD
* ZABBIX_DB_NAME
* ZABBIX_DB_USER
* ZABBIX_DB_PASSWORD

⚠️ No se hardcodean credenciales en el código.

---

## ❤️ Healthchecks

Servicios con healthcheck:

* HESK Web → HTTP check
* MariaDB → mysqladmin ping
* MySQL → mysqladmin ping
* Zabbix Web → HTTP check

Permiten validar disponibilidad de servicios automáticamente.

---

## 🧪 Validación en vivo (cumple requisitos)

Se puede demostrar:

✔ Edición de `categories.txt`
✔ Commit y push
✔ Ejecución del pipeline
✔ Creación automática en HESK
✔ Visualización en Zabbix
✔ Caída del servicio y alerta
✔ Recuperación automática

---

## 🏁 Decisiones técnicas

* Uso de Docker Compose para portabilidad
* Separación de bases de datos
* Automatización vía script Python
* Monitoreo basado en Web Scenarios
* Pipeline con GitHub Actions + runner propio

---

## 📦 Estructura del proyecto

```
.
├── docker-compose.yml
├── categories.txt
├── scripts/
│   └── sync_categories.py
├── hesk/
├── logs/
├── .github/workflows/
└── README.md
```

---

## 📌 Supuestos

* HESK ya está instalado en el contenedor
* Acceso a base de datos disponible desde el script
* Runner de GitHub configurado correctamente
* Red Docker interna funcional

---

## ✅ Resultado final

La solución cumple con:

* Infraestructura reproducible
* Automatización real
* Idempotencia
* Observabilidad
* Integración completa DevOps

---
