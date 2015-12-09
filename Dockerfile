FROM rjor2/opencv

# CODE
COPY . /code
WORKDIR /code

CMD ["python /code/pixelator.py"]