# Het adviesrapport en ethische design patterns

## Het Adviesrapport

Eerste beginnen met probleemanalyse (ishikawa diagram(?)).
Dan de oorzaak van het probleem.
Onderbouwen met prototype dat je hebt gemaakt (prototype = project).
Vervolgens advies geven op basis van ethische design patterns.
In de studiehandleiding staat hoe het rapport wordt getoests, ook staat er een structuur en alles wat ze willen.
terugzien, deze is heel uitgebreid met een hoop vragen die een richtlijn kunne zijn voor het schrijven van het rapport.
Een belangrijk deel is die analyse waarbij je laat zien waaraan je hebt gewerkt en hoe dit aansluit.
Zo een rapport zou eigenlijk geen verassing mogen zijn voor de opdrachtgever, je neemt hem/haar mee in het proces.
Technologien die je hebt onderzocht, alles waarmee je bezig was in het project moeten stevig aan bod komen in het
adviesrapport.

Dark side van het project is onderzoeken wat er verkeerd is met het project, wat allemaal mis gaat, etc. Je moet deze in
verbinding zetten met de lichte kant van het project.
Je moet overtuigend staan in je rapport, je moet goed onderbouwen waarom je bepaalde keuzes hebt gemaakt.

Ontwikkelproces in het document zetten.
Onderbouw keuzes (waarom, hoe, wat).
Vertel welke rollen en perspectieven zijn meegenomen:

- Zorg ervoor dat elke rol goed aan bod komt, zorg ervoor dat per rol duidelijk is wat iedereen heeft gedaan (e.g: AI
  heeft zich beziggehouden met deze AI kiezen, en waarom; Frontend heeft zich beziggehouden met UI, design etc.)

Breng in kaart welke stakehodlers er zijn.
Check goed welke eisen er zijn.

Elk van deze onderwerpen heeft pakweg 200-400 woorden nodig (Staat ook in de template!(DLO))

ONDERBOUWEN!!!

## Ethische matrix

Een framework uit de jaren 80 dat helpt om ethische kwesties in kaart te brengen.

Bepaal je stakeholders: rijen
Kies je waarden: Kolommen
Vul de cellen in: Hoe raakt deze technologie deze stakeholder op deze waarde

Voorbeeld Brightspace:

|                | Transparanite | Archivering        | Autonomie          | Privacy                 |
|----------------|---------------|--------------------|--------------------|-------------------------|
| Docenten       | ---           | ---                | ---                | Zoveel mogelijk data    |
| Student        | ---           | ---                | Weinig zeggenschap | Activiteit is zichtbaar |
| HvA management | ---           | Controle wetgeving | ---                | ---                     |
| Ontwikkelaars  | ---           | ---                | ---                | ---                     |

Tip: De interessantste inzichten zitten vaak bij stakeholders die geen stem hebben in het ontwerp, en bij waarden die
botsen

## Ethische design patterns

Value en sensitivity design
Privacy for design
Provocative prototyping
Bright patterns

## Pattern matching

Scrhijf je ethische dilemma's op.
Beschrijf welke "dark" patterns jullie hebben toegepast.
Kies voor elk dillema ook een of twee "light patterns".

Dit moet ook in je adviesrapport komen.

### GenAI

1. Betrouwbaarheid
    - Uitleggen waarom AI niet betrouwbaar is.
    - Dark patterns die hierbij horen:
        - AI zoekt vaakt patronen die niet waar zijn
        - AI kan bevooroordeeld zijn
        - Er zit bias in de data
            - Claude mag geen vooroordelen op basis van ethniciteit geven
    - Light patterns die hierbij horen:
        - Advies om AI output altijd te controleren
        - Gebruik van meerdere AI modellen om output te vergelijken
        - Transparantie over de beperkingen van AI systemen

2. Privacy
    - In context van het project is dit belangrijk doordat we een fotobooth hebben.
    - Dark patterns die hierbij horen:
        - Gevoelige informatie kan worden blootgesteld
        - AI wordt getrained op gevoelige data zonder toestemming
    - Light patterns die hierbij horen:
        - Anonimisering van data
        - Duidelijke communicatie over welke data wordt gebruikt om de AI te trainen

Bespreken met Marise welke andere ze evt. wilt hebben. In principe is ons project gefocust op betrouwbaarheid van AI.
Privacy evt. ook?