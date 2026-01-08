### Sprint 4 - Sprint Review

Deze sprint hebben we de laatste loodjes gelegd voor het eindproduct. We zijn begonnen met onze backlog doorlopen en bepalen welke user stories we daadwerkelijk nog op gaan pakken deze sprint. Omdat we de laatste week van de expo vrij wilden houden voor fixes en het adviesrapport hebben we een hoop stories geschrapt die niet het doel van het project direct ondersteunen. Uiteindelijk hebben we gewerkt aan het implementeren van de denkstappen van Gemini op te slaan en deze te weergeven op de website, bounding boxes rondom gezichten toevoegen aan de webcam feed, de verschillende uitkomsten van de 3 AI-modellen Gemini, Claude en ChatGPT te vergelijken op de website en het installeren van een camera aan de Raspberry Pi zodat we deze in de photobooth kunnen gebruiken. De rest van de sprint hebben we benut om wat fixes door te voeren en het adviesrapport te schrijven.


### Eindproduct

Het eindproduct bestaat uit een website die live draait op onze VPS op het adres https://parallax-darktech.nl. Op de website wordt de gebruiker gelijk ontvangen door de selfie pagina waar zij een foto kunnen maken met hun webcam na het accepteren van de gebruikersvoorwaarden.
![Webcam page](webcam.png)

Zodra de gebruiker een foto heeft gemaakt, wordt de AI aangeroepen om aannames te genereren op basis van de foto. Na een paar seconden zal dit klaar zijn en worden getoond op de website.
![Assumptions page](assumptions.png)

De gebruiker kan vervolgens doorklikken naar de formulierpagina waar zij nog een keer een overzicht van hun aannames kunnen inzien met bijbehorende beredeneringen van de AI. Ook staan hier de thinking steps van Gemini. Bij het gebruik van de fysieke photobooth zal er een QR-code staan bij de aannames die de gebruiker kan scannen om naar deze pagina te gaan.
![Form page](form.png)

Tot slot kan je op deze pagina ook de vergelijking vinden tussen de drie AI-modellen Gemini, Claude en ChatGPT tussen hun aannames en beredeneringen.
![Comparison page](comparison.png)


Naast de website is er ook een fysieke photobooth gebouwd, waarin de gebruiker een foto kan laten maken met een camera via Raspberry Pi. Ook is de photobooth voorzien van een scherm waarop de gebruiker zichzelf en de aannames kan bekijken, met een QR-code om de website te openen op hun telefoon waar ze naast de aannames ook de beredeneringen, thinking steps en vergelijkingen tussen modellen kunnen zien. De binnenkant van de photobooth is te zien in de bijgevoegde video's.
<div style="display: flex; gap: 10px;">
  <img src="booth.png" alt="Photobooth" style="width: 48%;"/>
  <img src="screen.png" alt="Achterkant scherm photobooth" style="width: 48%;"/>
</div>

Aan de zijkant van de photobooth hangt een lijst met de gebruikersvoorwaarden van onze website, en die van Gemini, Claude en ChatGPT. Bij het plaatsnemen in de photobooth stemt de gebruiker hiermee in.
<div style="display: flex; gap: 10px;">
  <img src="terms-of-use.png" alt="Gebruikersvoorwaarden" style="width: 48%;"/>
  <img src="terms-of-use-2.png" alt="Gebruikersvoorwaarden" style="width: 48%;"/>
</div>
