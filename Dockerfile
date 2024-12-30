# Usa una imagen base compatible con AWS Lambda para Python 3.11
FROM public.ecr.aws/lambda/python:3.11

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /var/task

# Copia los archivos necesarios al contenedor
COPY requirements.txt ./
COPY main.py ./
COPY src ./src

# Instala las dependencias en el directorio /var/task/dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt -t /var/task/dependencies

# Empaqueta las dependencias junto con el código
RUN cd /var/task && \
    zip -r lambda_package.zip main.py dependencies src

# Define el punto de entrada del contenedor
CMD ["lambda_function.handler"]
