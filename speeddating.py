import sys 
import string
import math
import time
import itertools as it
import more_itertools as mit

anzahl_teilnehmer = int(sys.argv[1])
anzahl_tische = int(sys.argv[2])

starttime = time.time()

# Symbolische Namen für die Teilnehmer generieren.
L = len(string.ascii_uppercase)
if anzahl_teilnehmer <= L:
    teilnehmer = [string.ascii_uppercase[x] for x in range(anzahl_teilnehmer)]
elif anzahl_teilnehmer <= L*L:
    teilnehmer = [string.ascii_uppercase[x//L] + string.ascii_uppercase[x%L] for x in range(anzahl_teilnehmer)]
else:
    print("Zu viele Teilnehmer, Namen sind nur zweistellig")
    quit()

print (f'{len(teilnehmer)} Teilnehmer an {anzahl_tische} Tischen:')

runden = []
kennengelernte_paare = set()

teilnehmer_pro_tisch = len(teilnehmer) // anzahl_tische

partitions = 0
for part in mit.set_partitions(teilnehmer, anzahl_tische):
    partitions += 1
    balanced = all(map(lambda a: len(a) >= teilnehmer_pro_tisch, part))
    if balanced:        
        paare = set()
        for a in part:
            paare = paare.union(set(it.combinations(a, 2)))
        
        if any(x in kennengelernte_paare for x in paare):
            # print(f'{["".join(p) for p in part]} - doppelte Paarung')
            pass
        else:
            print(f'{["".join(p) for p in part]}')
            runden.append(part)
            kennengelernte_paare = kennengelernte_paare.union(paare)
    else:
        #print(f'{["".join(p) for p in part]} - Nicht balanciert')
        pass

alle_paare = set(it.combinations(teilnehmer, 2))
fehlende_paare = alle_paare.difference(kennengelernte_paare)

if fehlende_paare:
    print('--')

    print(f'{len(fehlende_paare)} Paare fehlen:')
    print(fehlende_paare)

    for part in mit.set_partitions(teilnehmer, anzahl_tische):
        balanced = all(map(lambda a: len(a) >= teilnehmer_pro_tisch, part))
        if balanced:
            paare = set()
            for a in part:
                paare = paare.union(set(it.combinations(a, 2)))
            
            if any(x not in kennengelernte_paare for x in paare):
                print(f'{["".join(p) for p in part]}')
                runden.append(part)
                kennengelernte_paare = kennengelernte_paare.union(paare)
            else:
                # print(f'{["".join(p) for p in part]} - Kein neues Paar')
                pass

if False:
    for n in range(len(runden)):
        print(f'Runde {n+1}: {["".join(p) for p in runden[n]]}')
        
alle_paare = set(it.combinations(teilnehmer, 2))
fehlende_paare = alle_paare.difference(kennengelernte_paare)

if fehlende_paare:
    print(f'{len(fehlende_paare)} Paare fehlen:')
    print(fehlende_paare)
else:
    print(f'Alle Paare treffen sich nach {len(runden)} Runden')

if True:
    for t in teilnehmer:
        tischnummern = []
        for runde in runden:
            for tisch in range(len(runde)):
                if t in runde[tisch]:
                    tischnummern.append(tisch)

        print(f'Teilnehmer {t}: {"-".join(str(tn) for tn in tischnummern)}')

endtime = time.time()
print(f'{partitions} Partitionen geprüft in {math.ceil(endtime-starttime)}s')