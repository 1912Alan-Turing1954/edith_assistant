#!/bin/bash
echo "Installing Coqui - TTS"
git clone https://github.com/coqui-ai/TTS/ edith/TTS
cd edith/TTS
make system-deps  # only on Linux systems.
make install

git lfs install
git clone https://huggingface.co/facebook/wav2vec2-base-960h edith/models/wav2vec2