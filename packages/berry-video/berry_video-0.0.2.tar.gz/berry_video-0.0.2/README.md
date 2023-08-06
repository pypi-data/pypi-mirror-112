# Requisitos

- ## Gestão de Vídeos
    - ### Local
        - Download
            - Gatilho Temporal
                - Configurável
            - Uníco Vídeo
    - ### Servidor
        - Google Drive
- ## Gestão de Acesso
    - Google Drive
- ## Exibição dos Vídeos
    - ### Tipo de Arquivo
        - MP4
    - ### Resolução das telas
        - A Definir iniciar com Full HD
- ## Auto início
- ## Manual Instalação

    - [Instalação do SO](https://www.raspberrypi.org/software/)

    - Instalação da Aplicação
        - Passo 1
            
            Abra o terminal da raspbery e digite os seguintes comandos:

            ```
            pip3 install berry_video
            ```

        - Passo 2
            Caso tenha o arquivo `storage.json` no Drive, vá para o Passo 3

            Use o comando secret como descrito para gerar o arquivo `storage.json` na pasta `/var/tmp/berry/` (Salvar esse arquivo no Drive facilita as próximas instalações)
            ```
            berry secret https://drive.google.com/file/d/1GEmmscw8Gmv_psAn3XzZt33km3JdfLzO/view?usp=sharing
            ```

        - Passo 3
             Use o comando storage para baixar o arquivo `storage.json` na pasta `/var/tmp/berry/`
            ```
            berry secret <Link público do storage.json no Drive>
            ```
        - Passo 4
            Use o comando `start` para iniciar a aplicação.
    
            ```
            berry start
            ```
    
- ## Comandos Principais

    Para os comandos `start` e `update` o atributo minute é opicional, passando ele será registrado o tempo de atualização em minutos, caso não passe o tempo padrão será aplicado (5 minutos).

    - `start` Inicializa a aplicação e já faz o registro no crontab para iniciar após o @reboot. 
    
        ```
        berry start <minute>
        ```

    - `update` Força uma atualização do vídeo e já inicia e atualiza o vídeo em tela.
    
        ```
        berry update <minute>
        ```

    - `secret` Cria o arquivo de autenticação.
    
        ```
        berry secret https://drive.google.com/file/d/1GEmmscw8Gmv_psAn3XzZt33km3JdfLzO/view?usp=sharing
        ```

    - `storage` Atualiza o arquivo de autenticação.
    
        ```
        berry storage https://drive.google.com/file/d/1v-G1tZYIeQ97Xro5xITPfHucyH5ABRpj/view?usp=sharing
        ```
