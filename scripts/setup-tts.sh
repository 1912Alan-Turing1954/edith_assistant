echo "Installing Coqui - TTS"
git clone https://github.com/coqui-ai/TTS/ scripts/
cd TTS
make system-deps  # only on Linux systems.
make install