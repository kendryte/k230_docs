FROM ai.b-bug.org:5000/debian:11
COPY ./docs /app/docs
CMD ["tail", "-f", "/dev/null"]
