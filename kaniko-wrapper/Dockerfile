FROM alpine:latest

# Voeg een shell toe
RUN apk add --no-cache bash curl

# Kopieer Kaniko binaries
COPY --from=gcr.io/kaniko-project/executor:latest /kaniko /kaniko

# Zet een shell als entrypoint
ENTRYPOINT ["/bin/bash"]
