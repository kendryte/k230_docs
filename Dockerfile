FROM alpine:3.20
COPY ./docs /app/docs
CMD ["tail", "-f", "/dev/null"]
