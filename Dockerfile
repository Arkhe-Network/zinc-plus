FROM ubuntu:22.04

# Install necessary tools
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Clone llama.cpp repository
WORKDIR /app
RUN git clone https://github.com/ggerganov/llama.cpp.git

# Build llama-server
WORKDIR /app/llama.cpp
RUN cmake -B build
RUN cmake --build build --config Release -t llama-server

# Copy the GGUF model into the container
# Note: Ensure arkhe-os.gguf is generated and exists in the build context
COPY arkhe-os.gguf /app/arkhe-os.gguf

# Expose the default server port
EXPOSE 8080

# Command to serve the model via llama-server
CMD ["/app/llama.cpp/build/bin/llama-server", "-m", "/app/arkhe-os.gguf", "--host", "0.0.0.0", "--port", "8080"]
