#!/bin/bash
set -e

sudo chown -R vscode:vscode /home/vscode/.claude /home/vscode/.tmux

curl -fsSL https://claude.ai/install.sh | bash

if [ ! -d ~/.tmux/plugins/tpm ]; then
  git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
fi