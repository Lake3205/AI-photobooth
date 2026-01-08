# Adviesrapport

## Inhoud

- [Adviesrapport](#adviesrapport)
    - [Inhoud](#inhoud)
    - [Samenvatting](#samenvatting)
    - [Introductie](#introductie)
    - [Analyse](#analyse)
    - [Dark](#dark)
    - [Het dilemma](#het-dilemma)
    - [Light](#light)
    - [Advies](#advies)
    - [Proces en rollen](#proces-en-rollen)
        - [Werkwijze](#werkwijze)
        - [Rolbijdragen](#rolbijdragen)
        - [Stakeholders en betrokkenheid](#stakeholders-en-betrokkenheid)
    - [Reflectie, beperkingen en aanbevelingen](#reflectie-beperkingen-en-aanbevelingen)
        - [Reflectie: Wat zou het team anders doen?](#reflectie-wat-zou-het-team-anders-doen)
        - [Beperkingen van het onderzoek](#beperkingen-van-het-onderzoek)
        - [Aanbevelingen voor vervolgonderzoek](#aanbevelingen-voor-vervolgonderzoek)
    - [Bijlagen](#bijlagen)

## Samenvatting

In dit project hebben we als probleem dat generatieve AI-tools gebruikt worden door niet-tech gebruikers zonder dat zij 
begrijpen hoe deze tools werken en wat de implicaties zijn. Om dit aan te pakken, hebben we een interactief prototype 
ontwikkeld dat gebruikers laat reflecteren op de aannames en gevolgen van generatieve AI. Het prototype is een fotobooth
ervaring waarbij gebruikers in de booth gaan zitten om een foto te maken, waarna verschillende AI-modellen (OpenAI, 
Claude, Gemini) aannames genereren op basis van die afbeelding. De bedoeling voor de fotobooth is naast mensen 
bewuster maken van AI ook om gesprekken op gang te brengen over AI en vooroordelen.

We hebben onderzocht of en hoe dit prototype mensen bewuster maakt van de werking en risico's van AI. Uit 
gebruikerstesten tijdens Society 5.0 en Studio.Next kwamen verschillende inzichten naar voren. Mensen waren vaak geneigd
om de AI-aannames te rechtvaardigen, zelfs als deze onjuist of absurd waren. Dit kan ook goed teruggevonden worden bij 
Society 5.0 waarbij er nog geen AI-aannames waren en de antwoorden random waren. Dit wijst op een vertrouwen in AI dat 
kritisch denken kan ondermijnen. Daarnaast bleek dat het invullen van feedbackformulieren een drempel vormde, wat de 
dataverzameling beperkte.

Ons advies hierbij is om een combinatie van technische en educatieve maatregelen toe te passen om gebruikers bewuster en
kritischer te maken ten opzichte van AI-uitkomsten. Hoewel bias-tests, audits en human-in-the-loop mechanismen 
essentieel zijn, zijn ze op zichzelf niet voldoende. Daarom adviseren wij: AI-systemen in te zetten als leermiddel dat 
hun eigen beperkingen en aannames transparant toont, ruimte te creëren voor reflectie, dialoog en feedback binnen de 
gebruikerservaring, en AI niet alleen efficiënt, maar ook begrijpelijk en bespreekbaar te maken. Voor concrete 
vervolgstappen kan het onderzoek worden uitgebreid door dieper te onderzoeken waarom mensen AI vertrouwen en aannames 
accepteren. Samenwerking met psychologen of gedragswetenschappers kan helpen deze mechanismen beter in kaart te brengen,
zodat het ontwerp verder kan worden geoptimaliseerd om kritisch denken bij gebruikers te stimuleren. Door deze 
maatregelen te combineren kan de opdrachtgever AI-toepassingen ontwikkelen die niet alleen functioneel en innovatief 
zijn, maar ook verantwoord en mensgericht.

link naar de prototype: https://www.parallax-darktech.nl/


## Introductie

In deze opdracht — uitgevoerd in opdracht van onze docent en begeleider Marise — hebben we een interactief prototype
ontwikkeld dat niet-tech gebruikers laat reflecteren op de werking en gevolgen van generatieve AI. De doelgroep bestaat
uit doodgewone mensen die nieuwsgierig zijn naar AI maar geen diep technische achtergrond hebben, ook al zijn deze ook
voorgekomen bij de antwoorden van ons formulier. Ons prototype is een fotobooth-achtige ervaring: gebruikers maken
of uploaden een foto, het systeem genereert op basis van die afbeelding veronderstellingen en toelichtingen afkomstig
van verschillende AI‑modellen (OpenAI, Claude of Gemini). Belangrijke ontwerpkeuzes waren anonimiteit en expliciete
toestemming: foto’s worden alleen tijdelijk verwerkt, en deelnemers kunnen actief instemmen met
deelname en dataretentie (feedbackformulier invullen).

Technisch bestaat de oplossing uit een frontend met realtime gezichtsdetectie en bounding boxes, een backend die
modelvergelijking en reasoning terugstuurt, en eenvoudige database- en formulierenfunctionaliteit om feedback te
verzamelen. Doel was niet om een productierijpe gezichtsherkenner te bouwen, maar een provocatief leermiddel dat laat
zien hoe snel AI aannames maakt, welke risico’s dat met zich meebrengt en hoe gebruikers daarop reageren.

## Analyse

De probleemstelling van onze opdracht is dat generatieve AI-tools zoals ChatGPT, Claude en Midjourney mainstream zijn
geworden. Deze tools worden steeds vaker gebruikt in bijvoorbeeld het onderwijs, werk of privé, alleen weinig mensen
begrijpen hoe deze tools en de AI-systemen erachter precies werken. Vragen zoals "Wat is een LLM?", "Hoe komt een AI tot
een antwoord?" en "Wat zijn de implicaties van het massaal inzetten van deze technologie in het dagelijks leven?" heeft
de gemiddelde gebruiker geen antwoord op.

De voornaamste oorzaak is het gebruik aan publieke AI-literacy, ofwel het vermogen om AI-systemen kritisch te begrijpen
en gebruiken. Er is behoefte aan nieuwe educatieve en ervaringsgerichte manieren om niet-tech experts bewust te maken
van hoe generatieve AI werkt, welke aannames erin zitten, en wat de ethische risico's zijn (denk aan bias,
desinformatie, auteursrecht, vervreemding van creatief werk, of afhankelijkheid van black-box systemen).

Voor deze oorzaak hebben wij het afgelopen semester een interventie bedacht aan de hand van de kernvraag: "Hoe kun je
via een interactief, provocatief prototype het publiek laten reflecteren op de werking, aannames en gevolgen van
generatieve AI-technologieën zoals ChatGPT of Claude?"

Tijdens het project hebben wij verkend hoe wij generatieve AI op een speelse en kritische manier kunnen presenteren aan
niet-tech experts. Hierbij hebben we vooral gebruik gemaakt van de bekendste AI-chatbots zoals ChatGPT, Claude en Gemini
omdat deze in het dagelijks leven het meest gebruikt worden. We hebben in het begin kort overwogen zelf een AI-model te
draaien, maar dit zal voor niet-tech experts mogelijk te complex zijn en wij zagen geen verdere toegevoegde waarde ten
opzichte van AI API's. Hieruit viel verder niet echt iets te leren, maar kan wel helpen bij het overbrengen tot
niet-tech experts omdat zij waarschijnlijk alleen bekend zijn met deze grote AI-systemen.  
We hebben ook verkend wat voor impact de toevoeging van opgevraagde beredenering van AI-antwoorden en de denkwijze van
AI kan hebben op het ondersteunen van het doel van ons project. Hieruit kan je leren dat AI met overtuiging antwoord
geeft dat nergens op gebaseerd is, puur zodat de gebruiker antwoord krijgt op zijn/haar vraag. Dit is een van de
oorzaken waardoor AI onbetrouwbaar is en bijvoorbeeld misinformatie verspreidt.  
Tot slot hebben we ook geleerd dat mensen nog weleens geneigd zijn om de antwoorden van AI goed te praten. Op Society
5.0 deden wij alsof we met foto's van mensen aannames lieten genereren door AI (eigenlijk gewoon random hardcoded
waarden), en toen mensen zagen dat de AI soms rare of onjuiste aannames deed, probeerden ze dit alsnog te verklaren door
bijvoorbeeld lichtinval.

## Dark

Om te beginnen: ons prototype is op zich niet “dark”, maar laat wel zien hoe snel het dark kan worden. AI mag de keuze
niet voor ons maken, maar stuurt die in de praktijk steeds vaker onzichtbaar aan. Wij proberen namelijk mensen bewust te
maken dat AI niet altijd gelijk heeft. Ook kan er bias in zitten; dit houdt in dat het gemanipuleerd is. Als je deze
dingen negeert, is het gebruik van AI binnen een camera-software een zeer slechte morele keuze. Hij zal op sommige
vlakken gelijk hebben, maar hierbij ook keuzes maken die groepen benadelen. Het laatste wat we willen, is dat AI
oordeelt over wat mensen wel en niet mogen doen.

Een dark voorbeeld is het gebruiken van AI om op basis van vooroordelen in een supermarkt te kiezen wie een hogere kans
heeft om te stelen. Dit creëert een sfeer die moreel gezien een slechte keuze is. Hoe zou jij je voelen als je
geselecteerd wordt door een AI die je labelt met een hoge kans op diefstal?

Helaas worden ze wel voor dit doel gebruikt [1], volgens een onderzoek van RTL Nieuws [2]. Hierbij wordt de AI alleen
ingezet op handelingen van de klant, niet op basis van identiteit, leeftijd, afkomst of geslacht. Hierbij wordt alleen
ingegrepen nadat de klant probeert de winkel te verlaten zonder af te rekenen. In principe is het dus alleen een tool
die helpt bij het identificeren van diefstal. Dit kan bij mensen echter wel een gevoel van onrust creëren, omdat je
altijd bekeken wordt.

Ik ben hierna op onderzoek gegaan naar dingen die deze scenario’s tegenhouden: [3] In een wet van de Autoriteit
Persoonsgegevens staat het volgende:

Verboden:

- AI die mensen manipuleert of misleidt
- AI die mensen sociale scores geeft
- Bepaalde vormen van biometrische surveillance

Hoog risico:

- Werving en selectie (HR)
- Kredietverlening
- Onderwijs (toelating, beoordeling)
- Overheidsbesluiten

Beperkt:

- Chatbots
- Deepfakes
- AI-gegenereerde beelden of teksten

Minimaal risico:

- AI in games
- Spamfilters
- Aanbevelingssystemen (zoals “meer zoals dit”)

Deze wetten zijn hard nodig. Zonder duidelijke grenzen loopt AI snel uit de hand en neemt het onze macht en vrijheid van
keuzes over, zonder dat wij hier inspraak in hebben.

Ter informatie:
Ons project valt onder AI die sociale scores en biometrische surveillance gebruikt. Normaal is dit verboden, maar
doordat wij toestemming vragen en geen data opslaan, blijft het legaal. Dit laat zien hoe dun de grens is tussen een
ethisch experiment en technologie die mensen reduceert tot labels en risico’s.

## Het dilemma

Het dilemma dat wij in ons project proberen aan te pakken, is dat mensen vaak te snel vertrouwen op AI. Wanneer een 
AI-systeem informatie of een oordeel geeft, nemen mensen vaak aan dat dit klopt. AI wordt gezien als slim en objectief, 
terwijl dit in de praktijk niet zo is. AI is namelijk gebaseerd op een grote set data die niet altijd perfect is. Hij 
kan beïnvloed zijn (bias) of gaan hallucineren. Toch volgen mensen vaak de uitkomst zonder door te vragen of te 
factchecken.

Dit dilemma is moeilijk op te lossen, omdat er belangrijke waarden met elkaar botsen. Aan de ene kant willen mensen snel
informatie hebben, maar aan de andere kant willen we dat dit ook betrouwbaar en veilig is. Dit zijn twee dingen die 
moeilijk te combineren zijn binnen het gebruik van AI. AI kan inderdaad gebruikt worden om sneller beslissingen te nemen
en om menselijke fouten te verminderen, maar daar tegenover staan gelijkheid, vrijheid en menselijke controle (morele 
keuzes). Mensen willen niet beoordeeld worden door een systeem dat hen labelt of profileert.

Binnen de technologie komt het dilemma naar voren in de keuzes van de ontwikkelaars. Zij bepalen namelijk welke data er 
wordt gebruikt en dus ook wat de uitkomst van de AI is. Als deze keuzes gericht zijn op snelheid en efficiëntie, blijft 
er weinig toezicht over en zullen er snel dingen fout gaan. Hierdoor krijgt AI steeds meer invloed op ons dagelijks 
leven en onze keuzes, zonder dat wij hier echt iets aan kunnen doen of dit zelfs merken. AI zal een technisch hulpmiddel
moeten blijven, maar kan hierdoor helaas wel morele gevolgen hebben.

## Light

Om AI-toepassingen verantwoorder te maken hebben we in het ontwerp een aantal concrete patronen en maatregelen toegepast
en aanbevolen. Ten eerste: transparantie en uitleg — AI-antwoorden worden altijd vergezeld van een korte verklaring van
onzekerheid en een verwijzing naar welke modellen de output produceerden. Ten tweede: geïnformeerde toestemming en
data-minimalisatie — deelnemers kiezen expliciet mee welke beelden gebruikt worden en we
bewaren zo min mogelijk metadata; waar mogelijk anonymiseren we beelden of verwerken we lokaal. Derde patroon:
human‑in‑the‑loop — beslissingen met mogelijke consequenties voor mensen blijven zichtbaar voor en controleerbaar door
een menselijke operator. Verder bevelen we regelmatige bias-tests, model-audits en het gebruik van diverse testsets aan
om systematische fouten
vroeg te detecteren.

Ondanks deze stappen blijven enkele uitdagingen bestaan: het wegnemen van verborgen proxy-variabelen in trainingsdata,
het inbouwen van eerlijke prestatienormen over demografische groepen, en het balanceren van gebruiksvriendelijkheid met
noodzakelijke frictie (bijvoorbeeld extra bevestiging bij risicovolle uitspraken). Daarnaast zijn economische en
organisatorische prikkels vaak sterker dan ethische richtlijnen — technische patronen helpen, maar governance, beleid en
toezicht blijven cruciaal om verantwoorde inzet op schaal af te dwingen.

## Advies

Voor het advies moeten we eerst kijken naar het probleem en hoe wij dit hebben uitvergroot. Het probleem is dat 
generatieve AI-tools zoals ChatGPT, Claude en Gemini mainstream zijn geworden. Deze tools worden steeds vaker gebruikt 
in bijvoorbeeld het onderwijs, werk of privé, alleen weinig mensen begrijpen hoe deze tools en de AI-systemen erachter 
precies werken. Om dit probleem te voorkomen hebben wij een prototype ontwikkeld dat mensen bewust maakt van de werking,
aannames en gevolgen van generatieve AI-technologieën. Dit prototype is een fotobooth-ervaring waarbij gebruikers in de 
booth gaan zitten om een foto te maken, waarna verschillende AI-modellen (OpenAI, Claude, Gemini) assumpties genereren 
op basis van die afbeelding. De bedoeling voor de fotobooth is naast mensen bewuster maken van AI ook om gesprekken op 
gang te brengen over AI en vooroordelen.

Doormiddel van gebruikerstesten [4] tijdens Society 5.0 en Studio.Next hebben wij onderzocht of en hoe dit prototype mensen 
bewuster maakt van de werking en risico's van AI. Uit deze testen kwamen verschillende inzichten naar voren. Mensen 
waren vaak geneigd om de AI-aannames te rechtvaardigen, zelfs als deze onjuist of absurd waren. Dit kan ook goed terug 
gevonden worden bij Society 5.0 waarbij er nog geen AI-aannames waren en de antwoorden volledig willekeurig waren. Dit wijst 
op een vertrouwen in AI dat kritisch denken kan ondermijnen. Daarnaast bleek dat het invullen van feedbackformulieren 
een drempel vormde, wat de dataverzameling beperkte. Om hier conclusies uit te kunnen trekken zie je snel dat mensen 
geneigd zijn om AI te vertrouwen en de antwoorden goed te praten. Dit is een belangrijk inzicht voor het ontwerp van 
AI-systemen en educatieve tools. Hierbij is het cruciaal om mechanismen in te bouwen die kritisch denken stimuleren en 
gebruikers bewust maken van de beperkingen en risico's van AI. Het echte dilemma hierbij is dat AI steeds vaker 
onzichtbaar beslissingen voor ons neemt, zonder dat wij hier controle over hebben. Hoe kunnen we Gen-AI beter benutten 
zonder dat menselijke autonomie en keuzevrijheid langzaam worden overgenomen door het systeem?

Als we kijken naar de donkere en lichte kant en de impact die dit heeft op de maatschappij, zien we dat AI zowel 
positieve als negatieve gevolgen kan hebben. Bij de donkere kant is het belangrijk om duidelijke grenzen te stellen
aan het gebruik van AI, vooral wanneer het gaat om sociale scores en biometrische surveillance. Zonder deze grenzen kan 
AI snel uit de hand lopen en onze macht en vrijheid van keuzes overnemen. Aan de lichte kant kunnen we AI verantwoorder 
maken door transparantie, geïnformeerde toestemming, human-in-the-loop beslissingen en regelmatige bias-tests toe te 
passen. Deze maatregelen kunnen helpen om de negatieve gevolgen van AI te beperken en ervoor te zorgen dat AI-systemen 
op een ethische manier worden ingezet. Zelfs met transparantie en menselijke controle blijft AI keuzes beïnvloeden op 
een manier die moeilijk zichtbaar is voor gebruikers. Subtiele framing, waarschijnlijkheidsuitspraken en schaalvoordelen
zorgen ervoor dat AI-adviezen alsnog richtinggevend worden, waardoor echte keuzevrijheid onder druk kan komen te staan.

Waarom dit relevant is voor onze opdrachtgever? Omdat ontwerp- en ontwikkelkeuzes direct bepalen hoe AI-systemen invloed
uitoefenen op gebruikers. Ons onderzoek laat zien dat mensen AI-uitkomsten snel vertrouwen en rationaliseren, zelfs 
wanneer deze onjuist zijn. Dit betekent dat slecht ontworpen AI niet neutraal is, maar actief bijdraagt aan het 
ondermijnen van kritisch denken en autonomie. 

Juist daarom ligt er bij ontwerpers en ontwikkelaars een duidelijke verantwoordelijkheid. Door bewust rekening te houden
met de risico’s en ethische implicaties van Gen-AI, kan de opdrachtgever AI-toepassingen ontwikkelen die transparant, 
controleerbaar en mensgericht zijn. Dit verkleint maatschappelijke risico’s, vergroot vertrouwen bij gebruikers en 
draagt bij aan duurzame en verantwoorde innovatie.

Voor concrete aanbevelingen kan het onderzoek uitgebreid worden door bijvoorbeeld meer diepgang te zoeken in de 
psychologische aspecten van waarom mensen AI vertrouwen en deze aannames accepteren. In dit vervolgonderzoek kan er 
misschien samengewerkt worden met psychologen of gedragswetenschappers om dit beter in kaart te brengen. Met behulp van 
deze inzichten kan het ontwerp worden aangepast om kritischer denken te stimuleren.

Een andere aanbeveling betreft de combinatie van technische en educatieve maatregelen. Hoewel bias-tests, audits en 
human-in-the-loop mechanismen essentieel zijn, zijn ze op zichzelf niet voldoende. Ons onderzoek laat zien dat educatief
en ervaringsgericht ontwerp een cruciale rol speelt in het vergroten van AI‑literacy. Daarom adviseren wij:

- AI-systemen te gebruiken als leermiddel dat hun eigen tekortkomingen laat zien.
- Ruimte te creëren voor reflectie, gesprek en feedback binnen de gebruikerservaring. 
- AI niet alleen efficiënt, maar ook begrijpelijk en bespreekbaar te maken.

## Proces en rollen

### Werkwijze

Het team heeft gewerkt volgens de scrum-methodiek. We hebben elke sprint user stories opgesteld en deze verdeeld over de
teamleden. De voortgang werd bijgehouden via een sprintboard in GitLab.

Wekelijks kwamen we op maandag om 11:30 uur bij elkaar voor voortgangsbespreking en planning, dit is ook wanneer we de
sprintplanningen uitvoerden. Tijdens deze sprintplanning kwam elk teamlid met minimaal 3 user stories, wat zorgde voor
voldoende werk en betrokkenheid van iedereen. Vanaf sprint 3 begonnen we met een wisselende Scrum Master rol om de
verantwoordelijkheid gelijk te verdelen over het team. Alle documentatie werd bijgehouden in de docs-map van de
Git-repository, wat zorgde voor een centrale en toegankelijke kennisbank. Hier staan de technische aspecten, maar ook
het proces en feedbackmomenten. Om de focus tijdens meetings te behouden werd de notulist aangewezen om te waarschuwen
wanneer de groep afdwaalde van de agenda.

### Rolbijdragen

Binnen de Dark Tech studio zijn er verschillende richtingen gekozen per teamlid. Wij hebben 3 van deze richtingen binnen
het team, namelijk AI-engineer (Jay, Sjoerd en Tom), Creative technologist (Senna) en Frontend developer (Borys).
Hieronder een overzicht van de belangrijkste bijdragen per teamlid.

Jay richtte zich voornamelijk op de installatie van de VPS en de deployment van de applicatie naar deze server. Ook
heeft hij een domeinnaam gekoppeld en beveiligd met een SSL-certificaat. Daarnaast was hij verantwoordelijk voor de
integratie van de OpenAI API en ontwikkelde hij de AI-model vergelijkingsfunctionaliteit, waarmee gebruikers de output
van verschillende AI-modellen kunnen vergelijken.

Sjoerd heeft zich beziggehouden met de integratie van de Gemini API en hier extra functionaliteiten aan toegevoegd,
zoals de AI reasoning/explanation functionaliteit. Hij werkte samen met Tom aan de backend structuur, deze opzet bestaat
uit een controller en service laag. Ook richtte hij zich vaak op het behoud van deze structuur tijdens de ontwikkeling.
Daarnaast deed hij onderzoek naar Computer Vision technieken die toegepast konden worden binnen het project.

Tom nam als derde AI-engineer de rol op zich om de AI-architectuur op te zetten en werkte samen met Sjoerd aan de
backend structuur. Samen met Senna ontwierp en implementeerde hij de database in PHPMyAdmin en backend. Hij was
verantwoordelijk voor de integratie van de Claude API en ontwikkelde de enquête functionaliteit en formulierverwerking.
Daarnaast zette hij de A/B testing op voor Studio.Next en ontwierp en bouwde hij de fysieke photobooth constructie.

Senna focuste op de technische infrastructuur en beveiliging. Hij implementeerde beveiligingsmaatregelen zoals firewall
en CORS op de VPS. De database installeerde hij met PHPMyAdmin op de VPS voor eenvoudig database management. Samen met
Tom ontwierp en implementeerde hij deze database. Ook heeft Senna gewerkt aan de QR-code functionaliteit voor de
fotobooth en heeft zich verdiept in de Raspberry Pi implementatie, inclusief de werking van de webcam en camera op de
site.

Borys zorgde voor het visuele aspect van het project. Hij werkte aan het frontend design en de UI/UX verbetering om de
gebruikerservaring te verbeteren. Hij zorgde voor visuele consistentie over alle pagina's heen en verbeterde het design
van gemaakte websites. Ook implementeerde hij een bounding box rond gedetecteerde gezichten, wat voor een betere
immersie en impact zorgt tijdens de fotobooth ervaring.

### Stakeholders en betrokkenheid

Marise, onze docent en begeleider, was de opdrachtgever en primaire stakeholder dit project. Zij gaf ons feedback
tijdens sprint reviews en op losse momenten in de les. Daarnaast hielp zij ons met ideevorming en het bepalen van de
projectrichting. Tijdens het project hebben we regelmatig gedeeld wat onze ideeën waren en welke kant we op wilden gaan.

De eindgebruikers van ons project hebben ook een grote rol gespeeld als stakeholders. We hebben verschillende
gebruikerstesten uitgevoerd om feedback te verzamelen en onze aannames te valideren. Deze gebruikerstesten vonden plaats
tijdens Society 5.0 op 21 oktober en Studio.Next. De feedback van deze gebruikers is gebruikt om ons prototype te
verbeteren en nieuwe inzichten te krijgen over hoe mensen omgaan met AI-aannames. Feedback werd verzameld via
formulieren, directe observaties en gesprekken met de gebruikers.

## Reflectie, beperkingen en aanbevelingen

### Reflectie: Wat zou het team anders doen?

Terugkijkend op het project zijn er verschillende aspecten waarbij het team anders te werk zou gaan. Bij de
gebruikerstesten merkten we dat zowel bij Society 5.0 als Studio.Next minder mensen dan gehoopt het feedbackformulier
invulden. Het invullen van een formulier is vaak een drempel voor bezoekers. De stimulans van de AI reasoning bleek niet
genoeg om ook de enquête in te vullen. De A/B test bij Studio.Next leverde ook onvoldoende data op om harde conclusies
te trekken. In een volgend project zouden we daarom eerder kiezen voor de vragenlijst mondeling te verwerken of bij een
grotere groep mensen te testen. Bij Society 5.0 hadden als eerste evenement beter kunnen inzetten op er concreet achter
komen waarom mensen AI gebruiken en hoe we ze hier kritischer naar kunnen laten kijken. We hebben nu vooral gemeten wat
mensen doen, maar niet waarom ze dat doen.

### Beperkingen van het onderzoek

Onze onderzoeksopzet had verschillende beperkingen die de resultaten en conclusies beïnvloedden.

De schaal van het onderzoek was op Society 5.0 prima, alleen was hier het prototype nog niet ver in ontwikkeling wegens
de korte ontwikkelperiode. Bij Studio.Next hadden we een beter uitgewerkt prototype, maar was het aantal deelnemers
kleiner en waren wij niet het primaire doel van het evenement. Hierdoor was de betrokkenheid van deelnemers lager en
minder aandacht voor het onderwerp, ook waren de gebruikers hier minder divers en niet representatief voor de doelgroep
van AI-gebruikers in het algemeen.

Technische beperkingen speelden ook een rol in wat we konden realiseren. Het gebruik van Claude en OpenAI was beperkt
door de kosten en creditcard vereisten voor API toegang, waardoor grootschalig testen niet mogelijk was. De vergelijking
tussen AI-modellen bleef daardoor oppervlakkig. Uit eigen ervaring en gebruik van de verschillende AI's concludeerden we
dat Gemini wat assertiever is dan OpenAI en Claude, maar dit werd niet systematisch gemeten of gevalideerd. De keuze
voor geanonimiseerde opslag van data betekende dat grotere diepgang in analyse van de foto's niet mogelijk was. Wel
voorkomt dit privacyproblemen en ethische dilemma's rondom gezichtsdata.

We hadden graag een groot overzicht willen maken van verschillende AI-modellen en hun aannames, maar dit was helaas niet
haalbaar binnen de tijd en middelen van dit project. Hierdoor bleef de analyse beperkt tot een paar modellen en konden
we geen brede generalisaties maken over AI-aannames in het algemeen.

### Aanbevelingen voor vervolgonderzoek

Voor een volgend team dat dit onderzoek wil voortzetten zijn er verschillende richtingen waarin het project uitgebreid
en verbeterd kan worden.

Het onderzoek kan uitgebreid worden door bijvoorbeeld meer diepgang te zoeken in de psychologische aspecten van waarom
mensen AI vertrouwen en deze aannames accepteren. In dit vervolgonderzoek kan er misschien samengewerkt worden met
psychologen of gedragswetenschappers om dit beter in kaart te brengen. Met behulp van deze inzichten kan het ontwerp
worden aangepast om kritischer denken te stimuleren.

In het algemeen is het aan te raden om een grotere en meer diverse groep deelnemers te gebruiken bij het testen. Dit kan
helpen om meer representatieve data te verzamelen en opent ook deuren naar het onderzoeken van verschillen tussen
verschillende groepen mensen. Een voorbeeld hiervan zou kunnen zijn dat er gekeken wordt naar de verschillen in reacties
op AI-aannames tussen mannen en vrouwen.

Ook kan er onderzocht worden wanneer en waarom de AI-output als betrouwbaar wordt gezien. Dit kan bijvoorbeeld door te
variëren in de manier waarop de AI zijn antwoorden formuleert (zekerheid vs. waarschijnlijkheid) en te meten of
gebruikers hier eerder kritisch op reageren.

**Mogelijke vervolgvragen:**

- Welke rol speelt culturele achtergrond in het accepteren van AI antwoorden?
- Verschillen mannen en vrouwen in hoe ze AI-aannames over uiterlijk evalueren?
- Welke formulering van AI-output (zeker vs. waarschijnlijk) leidt tot meest kritische houding?

## Bijlagen

[1] https://privacy-web.nl/nieuws/supermarkten-installeren-cameras-met-ai-tegen-winkeldiefstal/
[2] https://www.rtl.nl/nieuws/artikel/5435132/supermarkten-pakken-winkeldieven-met-slimme-cameras`
[3] https://www.autoriteitpersoonsgegevens.nl/actueel/ai-verordening-gaat-in-werk-aan-de-winkel-voor-ontwikkelaars-en-gebruikers
[4] https://docs.google.com/spreadsheets/d/1R6vBBvVR3SH3v7ZQED2n-C4D2KTi3C9rxXEZDQL9Ro4/edit?resourcekey=&gid=1316423657#gid=1316423657