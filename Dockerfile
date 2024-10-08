FROM python:3.12-slim-bullseye as requirements-stage

WORKDIR /tmp

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install pdm
RUN pdm config pypi.url https://pypi.tuna.tsinghua.edu.cn/simple

COPY ./pyproject.toml ./pdm.lock* /tmp/
RUN pdm export -f requirements --output requirements.txt --without-hashes --prod


FROM python:3.12-slim-bullseye

WORKDIR /app

# 拷贝requirements.txt
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

# 安装依赖
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./coc /app/coc
COPY ./migrations /app/migrations

CMD ["uvicorn", "coc.main:app", "--host", "0.0.0.0", "--port", "8000"]
