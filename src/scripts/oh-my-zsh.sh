#!/usr/bin/env bash

USUARIO=$(logname);
HOME_USUARIO=/home/$USUARIO

apt install -y wget python3-pygments chroma

su -l $USUARIO -c "sh -c \"\$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)\""
    echo -e "\n\nPara listar temas:"
    echo -e "omz theme list\n"
    echo "Para definir um tema(bureau):"
    echo -e "omz theme set bureau\n"
    echo "Para ativar plugins(git asdf python pip colored-man-pages colorize docker docker-compose ufw):"
    echo -e "omz plugin enable git asdf python pip colored-man-pages colorize docker docker-compose ufw\n"

