FROM linuxserver/ffmpeg

# Install fontconfig
RUN apt-get update && \
    apt-get install -y --no-install-recommends fontconfig && \
    rm -rf /var/lib/apt/lists/*

# Copy Arial font files into the container
COPY fonts/ /usr/share/fonts/truetype/custom/

# Update font cache
RUN fc-cache -f -v