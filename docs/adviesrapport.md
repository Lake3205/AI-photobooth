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
  - [Analyse](#analyse-1)
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

## Introductie

## Analyse

## Dark

## Het dilemma

## Light

## Analyse

De probleemstelling van onze opdracht is dat generatieve AI-tools zoals ChatGPT, Claude en Midjourney mainstream zijn geworden. Deze tools worden steeds vaker gebruikt in bijvoorbeeld het onderwijs, werk of privé, alleen weinig mensen begrijpen hoe deze tools en de AI-systemen erachter precies werken. Vragen zoals "Wat is een LLM?", "Hoe komt een AI tot een antwoord?" en "Wat zijn de implicaties van het massaal inzetten van deze technologie in het dagelijks leven?" heeft de gemiddelde gebruiker geen antwoord op.

De voornaamste oorzaak is het gebruik aan publieke AI-literacy, ofwel het vermogen om AI-systemen kritisch te begrijpen en gebruiken. Er is behoefte aan nieuwe educatieve en ervaringsgerichte manieren om niet-tech experts bewust te maken van hoe generatieve AI werkt, welke aannames erin zitten, en wat de ethische risico's zijn (denk aan bias, desinformatie, auteursrecht, vervreemding van creatief werk, of afhankelijkheid van black-box systemen).

Voor deze oorzaak hebben wij het afgelopen semester een interventie bedacht aan de hand van de kernvraag: "Hoe kun je via een interactief, provocatief prototype het publiek laten reflecteren op de werking, aannames en gevolgen van generatieve AI-technologieën zoals ChatGPT of Claude?"

Tijdens het project hebben wij verkend hoe wij generatieve AI op een speelse en kritische manier kunnen presenteren aan niet-tech experts. Hierbij hebben we vooral gebruik gemaakt van de bekendste AI-chatbots zoals ChatGPT, Claude en Gemini omdat deze in het dagelijks leven het meest gebruikt worden. We hebben in het begin kort overwogen zelf een AI-model te draaien, maar dit zal voor niet-tech experts mogelijk te complex zijn en wij zagen geen verdere toegevoegde waarde ten opzichte van AI API's. Hieruit viel verder niet echt iets te leren, maar kan wel helpen bij het overbrengen tot niet-tech experts omdat zij waarschijnlijk alleen bekend zijn met deze grote AI-systemen.  
We hebben ook verkend wat voor impact de toevoeging van opgevraagde beredenering van AI-antwoorden en de denkwijze van AI kan hebben op het ondersteunen van het doel van ons project. Hieruit kan je leren dat AI met overtuiging antwoord geeft dat nergens op gebaseerd is, puur zodat de gebruiker antwoord krijgt op zijn/haar vraag. Dit is een van de oorzaken dat AI onbetrouwbaar is en bijvoorbeeld misinformatie verspreidt.  
Tot slot hebben we ook geleerd dat mensen nog weleens geneigd zijn om de antwoorden van AI goed te praten. Op Society 5.0 deden wij alsof we met foto's van mensen aannames lieten genereren door AI (eigenlijk gewoon random hardcoded waarden), en toen mensen zagen dat de AI soms rare of onjuiste aannames deed, probeerden ze dit alsnog te verklaren door bijvoorbeeld lichtinval.

## Proces en rollen

### Werkwijze

Het team heeft gewerkt volgens de scrum-methodiek. We hebben elke sprint user stories opgesteld en deze verdeeld over de teamleden. De voortgang werd bijgehouden via een sprintboard in GitLab. 

Wekelijks kwamen we op maandag om 11:30 uur bij elkaar voor voortgangsbespreking en planning, dit is ook wanneer we de sprintplanningen uitvoerden. Tijdens deze sprintplanning kwam elk teamlid met minimaal 3 user stories, wat zorgde voor voldoende werk en betrokkenheid van iedereen. Vanaf sprint 3 begonnen we met een wisselende Scrum Master rol om de verantwoordelijkheid gelijk te verdelen over het team. Alle documentatie werd bijgehouden in de docs-map van de Git-repository, wat zorgde voor een centrale en toegankelijke kennisbank. Hier staat de technische aspecten, maar ook het proces en feedbackmomenten. Om de focus tijdens meetings te behouden werd de notulist aangewezen om te waarschuwen wanneer de groep afdwaalde van de agenda.

### Rolbijdragen

Binnen de Dark Tech studio zijn er verschillende richtingen gekozen per teamlid. Wij hebben 3 van deze richtingen binnen het team, namelijk AI-engineer (Jay, Sjoerd en Tom), Creative technologist (Senna) en Frontend developer (Borys). Hieronder een overzicht van de belangrijkste bijdragen per teamlid.

Jay richtte zich voornamelijk op de installatie van de VPS en de deployment van de applicatie naar deze server. Ook heeft hij een domeinnaam gekoppeld en beveiligd met een SSL-certificaat. Daarnaast was hij verantwoordelijk voor de integratie van de OpenAI API en ontwikkelde hij de AI model vergelijkingsfunctionaliteit, waarmee gebruikers de output van verschillende AI-modellen kunnen vergelijken.

Sjoerd heeft zich beziggehouden met de integratie van de Gemini API en hier extra functionaliteiten aan toegevoegd, zoals de AI reasoning/explanation functionaliteit. Hij werkte samen met Tom aan de backend structuur, deze opzet bestaat uit een controller en service laag. Ook richtte hij zich vaak op het behoud van deze structuur tijdens de ontwikkeling. Daarnaast deed hij onderzoek naar Computer Vision technieken die toegepast konden worden binnen het project.

Tom nam als derde AI-engineer de rol op zich om de AI-architectuur op te zetten en werkte samen met Sjoerd aan de backend structuur. Samen met Senna ontwierp en implementeerde hij de database in PHPMyAdmin en backend. Hij was verantwoordelijk voor de integratie van de Claude API en ontwikkelde de enquête functionaliteit en formulierverwerking. Daarnaast zette hij de A/B testing op voor Studio.Next en ontwierp en bouwde hij de fysieke photobooth constructie.

Senna focuste op de technische infrastructuur en beveiliging. Hij implementeerde beveiligingsmaatregelen zoals firewall en CORS op de VPS. De database installeerde hij met PHPMyAdmin op de VPS voor eenvoudig database management. Samen met Tom ontwierp en implementeerde hij deze database. Ook heeft Senna gewerkt aan de QR-code functionaliteit voor de fotobooth en heeft zich verdiept in de Raspberry Pi implementatie, inclusief de werking van de webcam en camera op de site.

Borys zorgde voor het visuele aspect van het project. Hij werkte aan het frontend design en de UI/UX verbetering om de gebruikerservaring te verbeteren. Hij zorgde voor visuele consistentie over alle pagina's heen en verbeterde het design van gemaakte websites. Ook implementeerde hij een bounding box rond gedetecteerde gezichten, wat voor een betere immersie en impact zorgt tijdens de fotobooth ervaring.

### Stakeholders en betrokkenheid

Marise, onze docent en begeleider, was de opdrachtgever en primaire stakeholder dit project. Zij gaf ons feedback tijdens sprint reviews en op losse momenten in de les. Daarnaast hielp zij ons met ideevorming en het bepalen van de projectrichting. Tijdens het project hebben we regelmatig gedeeld wat onze ideeën waren en welke kant we op wilden gaan. 

De eindgebruikers van ons project hebben ook een grote rol gespeeld als stakeholders. We hebben verschillende gebruikerstesten uitgevoerd om feedback te verzamelen en onze aannames te valideren. Deze gebruikerstesten vonden plaats tijdens Society 5.0 op 21 oktober en Studio.Next. De feedback van deze gebruikers is gebruikt om ons prototype te verbeteren en nieuwe inzichten te krijgen over hoe mensen omgaan met AI-aannames. Feedback werd verzameld via formulieren, directe observaties en gesprekken met de gebruikers.

## Reflectie, beperkingen en aanbevelingen

### Reflectie: Wat zou het team anders doen?

Terugkijkend op het project zijn er verschillende aspecten waarbij het team anders te werk zou gaan. Bij de gebruikerstesten merkten we dat zowel bij Society 5.0 als Studio.Next minder mensen dan gehoopt het feedbackformulier invulden. Het invullen van een formulier is vaak een drempel voor bezoekers. De stimulans van de AI reasoning bleek niet genoeg om ook de enquête in te vullen. De A/B test bij Studio.Next leverde ook onvoldoende data op om harde conclusies te trekken. In een volgend project zouden we daarom eerder kiezen voor de vragenlijst mondeling te verwerken of bij een grotere groep mensen te testen. Bij Society 5.0 hadden als eerste evenement beter kunnen inzetten op er concreet achter komen waarom mensen AI gebruiken en hoe we ze hier kritischer naar kunnen laten kijken. We hebben nu vooral gemeten wat mensen doen, maar niet waarom ze dat doen. 

### Beperkingen van het onderzoek

Onze onderzoeksopzet had verschillende beperkingen die de resultaten en conclusies beïnvloedden.

De schaal van het onderzoek was op Society 5.0 prima, alleen was hier het prototype nog niet ver in ontwikkeling wegens de korte ontwikkelperiode. Bij Studio.Next hadden we een beter uitgewerkt prototype, maar was het aantal deelnemers kleiner en waren wij niet het primaire doel van het evenement. Hierdoor was de betrokkenheid van deelnemers lager en minder aandacht voor het onderwerp, ook waren de gebruikers hier minder divers en niet representatief voor de doelgroep van AI-gebruikers in het algemeen. 

Technische beperkingen speelden ook een rol in wat we konden realiseren. Het gebruik van Claude en OpenAI was beperkt door de kosten en creditcard vereisten voor API toegang, waardoor grootschalig testen niet mogelijk was. De vergelijking tussen AI-modellen bleef daardoor oppervlakkig. Uit eigen ervaring en gebruik van de verschillende AI's concludeerde we dat Gemini wat assertiever is dan OpenAI en Claude, maar dit werd niet systematisch gemeten of gevalideerd. De keuze voor geanonimiseerde opslag van data betekende dat grotere diepgang in analyse van de foto's niet mogelijk was. Wel voorkomt dit privacyproblemen en ethische dilemma's rondom gezichtsdata.

We hadden graag een groot overzicht willen maken van verschillende AI-modellen en hun aannames, maar dit was helaas niet haalbaar binnen de tijd en middelen van dit project. Hierdoor bleef de analyse beperkt tot een paar modellen en konden we geen brede generalisaties maken over AI-aannames in het algemeen. 

### Aanbevelingen voor vervolgonderzoek

Voor een volgend team dat dit onderzoek wil voortzetten zijn er verschillende richtingen waarin het project uitgebreid en verbeterd kan worden.

Het onderzoek kan uitgebreid worden door bijvoorbeeld meer diepgang te zoeken in de psychologische aspecten van waarom mensen AI vertrouwen en deze aannames accepteren. In dit vervolgonderzoek kan er misschien samengewerkt worden met psychologen of gedragswetenschappers om dit beter in kaart te brengen. Met behulp van deze inzichten kan het ontwerp worden aangepast om kritischer denken te stimuleren. 

In het algemeen is het aan te raden om een grotere en meer diverse groep deelnemers te gebruiken bij het testen. Dit kan helpen om meer representatieve data te verzamelen en opent ook deuren naar het onderzoeken van verschillen tussen verschillende groepen mensen. Een voorbeeld hiervan zou kunnen zijn dat er gekeken wordt naar de verschillen in reacties op AI-aannames tussen mannen en vrouwen. 

Ook kan er onderzocht worden wanneer en waarom de AI-output als betrouwbaar wordt gezien. Dit kan bijvoorbeeld door te variëren in de manier waarop de AI zijn antwoorden formuleert (zekerheid vs. waarschijnlijkheid) en te meten of gebruikers hier eerder kritisch op reageren.

**Mogelijke vervolgvragen:**

- Welke rol speelt culturele achtergrond in het accepteren van AI antwoorden?
- Verschillen mannen en vrouwen in hoe ze AI-aannames over uiterlijk evalueren?
- Welke formulering van AI-output (zeker vs. waarschijnlijk) leidt tot meest kritische houding?

## Bijlagen