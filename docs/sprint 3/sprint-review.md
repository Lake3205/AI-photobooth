## Sprint review – Sprint 3

In deze sprint lag de focus minder op het opleveren van nieuwe, zichtbare functionaliteiten en meer op het stabiliseren,
opschonen en voorbereiden van het product voor gebruikerstesten en de eindexpo. Een belangrijk moment binnen deze sprint
was onze aanwezigheid op Studio.Next, waar we ons prototype hebben getest met bezoekers.

Tijdens Studio.Next is het prototype door een aantal mensen bekeken en gebruikt. Het geïntegreerde formulier werd
echter minder vaak ingevuld dan gehoopt, waardoor onze geplande A/B-test (met en zonder reasoning/explanation) niet
voldoende data heeft opgeleverd om harde conclusies te trekken. Uit deze beperkte dataset kunnen we wel concluderen
dat het invullen van het formulier voor gebruikers te veel frictie oplevert. Dit inzicht nemen we mee als belangrijk
actiepunt voor de volgende sprint.

In de resterende tijd van deze sprint hebben we voornamelijk gewerkt aan de technische basis van het product. De backend
is verder opgeschoond en gestabiliseerd, error handling is verbeterd (onder andere rondom rate limiting) en er is
gewerkt
aan het voorkomen van crashes binnen de applicatie. Daarnaast is besloten om de website te draaien op een Raspberry Pi
in plaats van deze lokaal te runnen, om zo dichter bij de uiteindelijke opstelling voor de expo te komen.

De grootste functionele toevoeging binnen deze sprint is de explanation/reasoning en het geïntegreerde formulier. De
reasoning is momenteel nog opgezet als een conclusie met bijbehorende uitleg. Uit feedback blijkt dat het mogelijk
logischer en inzichtelijker is om deze volgorde om te draaien: eerst de stappen die het model neemt, gevolgd door een
conclusie met een zekerheidspercentage. Dit wordt meegenomen als verbeterpunt voor de volgende sprint. Daarnaast is het
idee ontstaan om verschillen tussen meerdere AI-modellen inzichtelijk te maken, zodat gebruikers beter begrijpen hoe
verschillende modellen tot uiteenlopende aannames kunnen komen.

Binnen het team zijn de werkzaamheden verdeeld met het oog op de laatste sprint. Er wordt gewerkt aan het tonen van de
denk- en redeneerstappen van de AI, het verbeteren van de frontend en formulier-vragen, het vergelijken van
verschillende
AI-modellen, het op orde brengen van overdrachtsdocumentatie en het verder opzetten van de hardware-opstelling met de
Raspberry Pi en camera. Tegelijkertijd is afgesproken dat er vanaf de volgende sprint serieus gestart wordt met het
adviesrapport en de overdracht.

Deze sprint heeft duidelijk gemaakt dat de prioriteit voor de laatste sprint moet liggen op usability, validatie en
afwerking, in plaats van het toevoegen van nieuwe features. De inzichten uit Studio.Next vormen hierbij een belangrijke
leidraad, zodat er voldoende tijd overblijft om het product expo-klaar te maken en de puntjes op de i te zetten.

### Verschillen tussen gebruikte AI-modellen

Voor het genereren van aannames maken wij gebruik van meerdere, veelgebruikte AI-modellen: OpenAI, Gemini en Claude. Elk
van deze modellen heeft zijn eigen karakteristieken, wat resulteert in verschillen in toon, detailniveau en manier van
redeneren. Door meerdere modellen te gebruiken kunnen we deze verschillen zichtbaar maken en beter begrijpen hoe
aannames tot stand komen.

**OpenAI en Claude**  
OpenAI en Claude hadden moeite met het formuleren van sterke aannames op basis van de beperkte input die zij kregen. Zo
lag de diefstalratio die door deze modellen werd gegenereerd relatief laag. Beide modellen neigen naar het geven van
algemenere en voorzichtige aannames, waarbij zij minder snel tot specifieke conclusies komen zonder voldoende bewijs.

**Gemini**  
Gemini daarentegen toonde zich zelfverzekerder in het formuleren van aannames. Het model genereerde hogere
diefstalratio’s en kwam met meer gedetailleerde en specifieke conclusies. Gemini lijkt beter in staat om verbanden te
leggen en risico’s in te schatten, waardoor het overtuigender overkomt in zijn aannames.

Door deze modellen naast elkaar te gebruiken, zien we dat aannames niet objectief of eenduidig zijn, maar sterk worden
beïnvloed door de manier waarop een model redeneert en formuleert. Dit inzicht is waardevol voor gebruikers, omdat het
hen bewust maakt van de subjectiviteit achter AI-gegenereerde conclusies.
