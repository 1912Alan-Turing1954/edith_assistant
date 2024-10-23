echo "Installing Coqui - TTS"
git clone https://github.com/coqui-ai/TTS/ edith/TTS
cd edith/TTS
make system-deps  # only on Linux systems.
make install