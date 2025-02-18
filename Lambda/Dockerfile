# Stage 1: Copy LLM file
FROM public.ecr.aws/lambda/python:3.10 AS builder

# Stage 2: Final image
FROM public.ecr.aws/lambda/python:3.10
 
# Copy the dependencies file to the working directory
COPY req.txt ${LAMBDA_TASK_ROOT} 

RUN yum -y update && \
    yum -y install yum-utils && \
    yum clean all
 
# Add the custom repository for Tesseract
RUN yum-config-manager --add-repo https://download.opensuse.org/repositories/home:/Alexander_Pozdnyakov/CentOS_7/
 
# Import the public GPG key to trust the repository
RUN rpm --import https://build.opensuse.org/projects/home:Alexander_Pozdnyakov/signing_keys/download?kind=gpg
 
# Update the system repositories after adding the new one
RUN yum -y update
 
# Install Tesseract and the German language pack
RUN yum install -y mesa-libGL && \
    yum -y install tesseract && \
    yum -y install tesseract-langpack-deu 
    

 
# Ensure the system is clean after installation
RUN yum clean all && \
    rm -rf /var/cache/yum
 
# Add Tesseract to the PATH environment variable
ENV PATH="/usr/local/bin:${PATH}"



# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r req.txt

COPY PDF_uploads_integration /tmp

COPY . ${LAMBDA_TASK_ROOT} 

CMD ["lambda_function.lambda_handler"]

