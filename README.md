# IliadBot

**iliadbot** è un bot telegram che permette di conoscere soglie e credito della tua SIM Iliad. Il bot non è ufficiale e non conserva o salva le tue credenziali di accesso, tuttavia queste potrebbero rimanere sui server di Telegram. Utilizza il bot consapevolmente!

Il codice sorgente è rilasciato sotto licenza AGPL 3.0.

<p align="center">
<img src="../master/resources/screenshots/example_soglie_italia.jpg" width="250">
<img src="../master/resources/screenshots/example_info_sim.jpg" width="250">
</p>

Di seguito le istruzioni per eseguire la tua istanza personale di questo bot.

## Linux

Per eseguire la tua istanza di questo bot su un sistema Linux usa le seguenti istruzioni:

```
virtualenv -p python3 iliadbotenv 
iliadbotenv/bin/pip install https://github.com/doublegized/iliadbot/archive/master.zip
iliadbotenv/bin/iliadbot path/config.yaml
```

Per fare un upgrade del bot:

```
iliadbotenv/bin/pip install --upgrade https://github.com/doublegized/iliadbot/archive/master.zip
```

Per eliminare l'installazione:

```
cd ..
rm -rf iliadbotenv
```

**NOTA BENE**: Il primo parametro dell'eseguibile è il file `config.yaml`. Un esempio di file è presente in `config/config.example.yaml`: sovrascrivi i parametri con le tue impostazioni.


## Docker

Il bot può essere eseguito anche su un container docker. Di seguito i comandi per la build e per l'esecuzione:

```
docker image build -t iliadbot:1.0 .
docker run -it -v /host/path/localdb:/app/localdb iliadbot:1.0
```

Il database viene salvato tramite *volumes* in modo da non perdere le statistiche in caso di stop del container. Non è tuttavia necessario utilizzare lo stesso database *sqlite*, dato che il bot è per sua natura stateless.



## Comandi supportati

```
/info - permette di conoscere stato soglie e credito`
/help - mostra un messaggio di aiuto
```
