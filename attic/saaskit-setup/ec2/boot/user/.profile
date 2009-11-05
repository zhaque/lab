# ~/.profile: executed by Bourne-compatible login shells.

if [ "$BASH" ]; then
  if [ -f ~/.bashrc ]; then
    . ~/.bashrc
  fi

  if [ -d ~/bin ] ; then
      PATH=~/bin:"${PATH}"
  fi
fi
