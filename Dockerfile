# # FROM alpine:3.20

# # # Instala python3 y pip
# # RUN apk add --no-cache python3-dev \
# #     && pip3 install --upgrade pip
# # WORKDIR /app
# # COPY . /app
# # RUN pip3 --no-cache-dir install -r requirements.txt
# # CMD ["python3","api/app.py"]
# FROM alpine:3.20

# # Instala python3, pip y otras dependencias
# RUN apk add --no-cache python3-dev py3-pip \
#     && pip3 install --upgrade pip

# # Establece el directorio de trabajo
# WORKDIR /app

# # Copia el código de la aplicación
# COPY . /app

# # Instala las dependencias de la aplicación
# RUN pip3 install --no-cache-dir -r requirements.txt

# # Ejecuta la aplicación
# CMD ["python3", "api/app.py"]

FROM alpine:3.20

# Instala python3, pip y otras dependencias necesarias
RUN apk add --no-cache python3-dev py3-pip \
    mariadb-connector-c-dev gcc musl-dev

# Crea y activa un entorno virtual
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Actualiza pip en el entorno virtual
RUN pip install --upgrade pip

# Establece el directorio de trabajo
WORKDIR /app

# Copia el código de la aplicación
COPY . /app

# Instala las dependencias de la aplicación en el entorno virtual
RUN pip install --no-cache-dir -r requirements.txt

# Ejecuta la aplicación
CMD ["python3", "api/app.py"]
