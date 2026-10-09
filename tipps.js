// Zufällige Ladebildschirm-Tipps und "Wusstest du schon?"-Sprüche.
// Neue Einträge einfach in die Listen schreiben. Gilt für alle Seiten.
(function(){
  var TIPS=[
    "Ein guter Raid beginnt mit einem guten Plan. Ein sehr guter Raid beginnt damit, dass alle im Discord sind.",
    "Das Mikrofon vor Raidbeginn zu testen erspart allen die Frage: „Hört mich jemand?“",
    "Reparieren nicht vergessen: Die Rüstung rostet schneller als die Moral.",
    "Loot-Diskussionen bitte nach dem Boss. Nicht währenddessen. Und schon gar nicht im Pull.",
    "Der Ruhestein bringt dich nach Hause, aber leider nicht pünktlich in den Raid.",
    "Wer die Aggro des Tanks überholt, fährt ohne Fahrschein in den Wipe.",
    "Ein Wipe ist nur ein Bossversuch mit zusätzlicher Lernkurve.",
    "Verbrauchsgüter sind keine Dekoration. Sie wirken nur, wenn man sie auch benutzt.",
    "Gleis 3 ist gesperrt. Bitte weichen Sie auf Gleis 4 aus oder auf die Reparaturkosten.",
    "Buffs laufen ab. Die Geduld des Raidleiters beim dritten „noch kurz AFK“ auch.",
    "Wenn Ulf „Ich pulle gleich“ sagt, ist jetzt der richtige Moment für Buffs, Gebete und letzte Wünsche.",
    "Schau auf den Boden: Wer im Feuer steht, hat meistens Gesellschaft, aber selten Heilung.",
    "Der Heiler heilt, der Tank tankt, der Schaden schadet. Die Rollenverteilung ist kein Vorschlag.",
    "Vor Hyjal ist nach Hyjal: Lieber einmal mehr die Taktik lesen als einmal mehr wipen."
];
  var FACTS=[
    "Unsere Gilde hat mehr Verspätungen als Erfolge — und das will bei uns etwas heißen.",
    "Wir sind eine 30 Mann RP Gilde..",
    "Wir hatten mal ein Karaoke-Event in Karazhan.",
    "Rohtbard ist hinter dem Dunklen Portal und braucht Hilfe.",
    "Livic ist auf dem Stuhl eingeschlafen.",
    "Nicht auf Mond.",
    "Laut Raidprotokoll #001 begann der Raid um 18:07 Uhr statt um 18:00 Uhr. Das gilt bei uns als pünktlich.",
    "Im selben Protokoll wurden 7 Wipes festgehalten und trotzdem „allgemeine Zufriedenheit“.",
    "Unser Fahrplan kennt vier Raidtage pro Woche und einen Offi-Abend. Ruhetage sind eher Gerüchte.",
    "WoW Classic erschien am 26. August 2019. Die ersten Verspätungen der Gilde folgten kurz darauf.",
    "Diese Seite ist für 1024×768 und den Internet Explorer 8 optimiert. Wir wissen, was wichtig ist.",
    "Das Gildenmotto lautet: „Gemeinsam raiden. Gemeinsam wachsen. Gemeinsam durchhalten.“",
    "Ulf darf pullen. Ob er pullen sollte, steht seit jeher in den Gildenregeln.",
    "Im Gildenradio läuft unter anderem „Lootdrama“, der inoffizielle Soundtrack jedes Raidabends.",
    "Oben auf der Startseite läuft der Countdown bis zum Release von WoW Forever. Sekunde für Sekunde.",
    "Unser Discord ist rund um die Uhr geöffnet. Anders als der Bahnhofskiosk.",
    "Die Galerie reicht von Classic bis nach Nordend. Der Weg dorthin war lang und hatte einige Wipes."
];
  function pick(a){return a[Math.floor(Math.random()*a.length)]}
  function init(){
    var t=document.getElementById('tip-text'),f=document.getElementById('fact-text');
    if(t)t.textContent=pick(TIPS);
    if(f)f.textContent=pick(FACTS);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
