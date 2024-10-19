FROM public.ecr.aws/lambda/python:3.12

RUN yum install -y gcc libxml2-devel libxslt-devel libffi-devel openssl-devel

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . /var/task/

CMD [ "lambda_function.lambda_handler" ]