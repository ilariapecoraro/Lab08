from database.impianto_DAO import ImpiantoDAO
from datetime import datetime

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self._lista_media = []
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        self._lista_media = []
        for impianto in self._impianti:
            consumi = impianto.get_consumi()
            consumi_mese = []
            for consumo in consumi:
                if consumo.data.month == mese:
                    consumi_mese.append(consumo.kwh)
            n = len(consumi_mese)
            if n > 0:
                media = sum(consumi_mese) / n
                self._lista_media.append((impianto.nome, media))
        return self._lista_media



        # TODO

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = 0
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        costo_ottimo = [0] # modo per passare le variabili per riferimento di memoria e non per valore
        self.__ricorsione(self.__sequenza_ottima, 1, None, costo_ottimo, consumi_settimana)

        self.__costo_ottimo = costo_ottimo[0]
        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """
        if giorno > 7:
            return
        costo_minore = 0
        impianto_minore = None
        for impianto_id in consumi_settimana:
            costo_giornaliero = consumi_settimana[impianto_id][giorno - 1]
            if impianto_id != ultimo_impianto:
                costo_giornaliero += 5
            if costo_giornaliero < costo_minore or costo_minore == 0:
                costo_minore = costo_giornaliero
                impianto_minore = impianto_id
        sequenza_parziale.append(impianto_minore)
        costo_corrente[0] += costo_minore
        self.__ricorsione(sequenza_parziale,giorno + 1, impianto_minore, costo_corrente, consumi_settimana)

        # TODO

    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        consumi_settimana = {}
        for impianto in self._impianti:
            consumi = impianto.get_consumi()
            consumi_settimana_mese = []
            for consumo in consumi:
                if consumo.data.month == mese and consumo.data.day <= 7:
                    consumi_settimana_mese.append(consumo.kwh)
            consumi_settimana[impianto.id] = consumi_settimana_mese
        return consumi_settimana

        # TODO

