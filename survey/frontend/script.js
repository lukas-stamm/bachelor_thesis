let bilder = [];
let index = 0;
let alter = null;
let betrachtungsDauer = 0;
let evaluation = [];

function startUmfrage() {
  alter = document.getElementById("alter").value;
  if (!alter || alter < 5 || alter > 120) {
    alert("Bitte gib ein gültiges Alter ein.");
    return;
  }

  document.getElementById("step-alter").classList.add("hidden");
  document.getElementById("step-umfrage").classList.remove("hidden");

  ladeBilder();
}

async function ladeBilder() {
  const res = await fetch("/api/get_images");
  bilder = await res.json();
  console.log("Geladene Bilder:", bilder);
  zeigeBild();
}

function zeigeBild() {
  if (index >= bilder.length) {
    document.getElementById("step-umfrage").classList.add("hidden");
    document.getElementById("step-danke").classList.remove("hidden");
    zeigeErgebnisTabelle();
    return;
  }

  const img = new Image();
  img.src = bilder[index].url;

  img.onload = () => {
    // Set viewing time AFTER image is loaded
    betrachtungsDauer = Math.random() * (4 - 2) + 2;

    // Set actual image in the DOM
    document.getElementById("bild").src = img.src;
    document.getElementById("bild-container").classList.remove("hidden");
    document.getElementById("entscheidung-container").classList.add("hidden");

    // Now start timer
    setTimeout(() => {
      document.getElementById("bild-container").classList.add("hidden");
      document.getElementById("entscheidung-container").classList.remove("hidden");
    }, betrachtungsDauer * 1000);
  };

  img.onerror = () => {
    console.error("❌ Fehler beim Laden des Bildes:", bilder[index].url);
    index++;
    zeigeBild(); // Try next image
  };
}

async function vote(entscheidung) {
  await fetch("/api/save_response", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      class: bilder[index].class,
      bild: bilder[index].name,
      entscheidung: entscheidung,
      alter: alter,
      zeit: betrachtungsDauer
    })
  });

  let echteKlasse = bilder[index].class;
  let korrekt = echteKlasse === entscheidung;

  evaluation.push({
    url: bilder[index].url,
    name: bilder[index].name,
    echteKlasse: echteKlasse,
    userAntwort: entscheidung,
    korrekt: korrekt
  });

  index++;
  zeigeBild();
}

function zeigeErgebnisTabelle() {
  const tbody = document.getElementById("ergebnis-body");
  const tabelle = document.getElementById("ergebnis-tabelle");
  tabelle.classList.remove("hidden");

  const richtig = evaluation.filter(e => e.korrekt).length;
  const gesamt = evaluation.length;
  const quote = Math.round((richtig / gesamt) * 100);
  document.getElementById("trefferquote").textContent = 
    `Du hast ${richtig} von ${gesamt} richtig erkannt (${quote}%).`;

  evaluation.forEach(e => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>
        <img src="${e.url}" class="thumbnail" alt="Vorschau"
             onclick="oeffneLightbox('${e.url}')">
      </td>
      <td>${e.echteKlasse}</td>
      <td>${e.userAntwort}</td>
      <td style="color: ${e.korrekt ? 'green' : 'red'};">
        ${e.korrekt ? '✅' : '❌'}
      </td>
    `;

    tbody.appendChild(row);
  });
}

function oeffneLightbox(bildSrc) {
  const lightbox = document.getElementById("lightbox");
  const img = document.getElementById("lightbox-img");
  img.src = bildSrc;
  lightbox.classList.remove("hidden");
}

function schliesseLightbox() {
  const lightbox = document.getElementById("lightbox");
  const img = document.getElementById("lightbox-img");
  img.src = "";
  lightbox.classList.add("hidden");
}