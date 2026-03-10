(function() {
    window.isGeoValid = false;
    const alertBox = document.getElementById('geo-alert');
    const statusTxt = document.getElementById('geo-status-text');
    const btnSubmit = document.getElementById('btn-submit');
    const latSpan   = document.getElementById('lat-val');

    if (!alertBox || !navigator.geolocation) return;

    alertBox.className = "alert geo-wait d-flex align-items-center gap-3 py-3 mb-4 rounded-3 shadow-sm border-0";

    navigator.geolocation.getCurrentPosition(
        async (pos) => {
            const { latitude, longitude } = pos.coords;
            latSpan.innerText = latitude.toFixed(4);

            try {
                const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;
                const resp = await fetch('/pointages/api/verifier-zone/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
                    body: JSON.stringify({ lat: latitude, lng: longitude })
                });
                const data = await resp.json();

                if (data.autorise || data.bypass) {
                    window.isGeoValid = true;
                    alertBox.className = "alert geo-ok d-flex align-items-center gap-3 py-3 mb-4 rounded-3 shadow-sm border-0";
                    alertBox.innerHTML = `<i class="bi bi-check-circle-fill fs-4"></i> <span><b>Position Validée.</b> ${data.message || 'Dans la zone.'}</span>`;
                    
                    // Si un employé est choisi, activer le bouton
                    const empSelect = document.getElementById('employe_id');
                    if (empSelect.value) btnSubmit.classList.remove('disabled');
                    
                } else {
                    alertBox.className = "alert geo-err d-flex align-items-center gap-3 py-3 mb-4 rounded-3 shadow-sm border-0";
                    alertBox.innerHTML = `<i class="bi bi-geo-alt-fill fs-4"></i> <span><b>Hors périmètre.</b> ${data.message}</span>`;
                    btnSubmit.innerHTML = `<i class="bi bi-slash-circle me-2"></i> POINTAGE DÉSACTIVÉ (HORS ZONE)`;
                }
            } catch (err) {
                alertBox.innerHTML = `<i class="bi bi-wifi-off fs-4"></i> <span>Erreur de connexion serveur.</span>`;
            }
        },
        (err) => {
            alertBox.className = "alert geo-err d-flex align-items-center gap-3 py-3 mb-4 rounded-3 shadow-sm border-0";
            alertBox.innerHTML = `<i class="bi bi-exclamation-triangle-fill fs-4"></i> <span>Désolé, l'accès GPS est requis pour pointer.</span>`;
        },
        { enableHighAccuracy: true, timeout: 10000 }
    );
})();
