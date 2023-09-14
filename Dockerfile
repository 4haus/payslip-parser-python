FROM --platform=linux/amd64,linux/arm64 python:3.11-slim-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends libmagic-dev locales \
    && sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY / .
RUN pip install -r requirements.txt

EXPOSE 8000

# Run the application:
CMD ["python", "server.py"]
