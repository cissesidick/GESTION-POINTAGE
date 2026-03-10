document.addEventListener('DOMContentLoaded', () => {
    // Horloge temps réel
    function updateClock() {
        const h = document.getElementById('horloge');
        if (!h) return;
        const now = new Date();
        const str = now.toLocaleDateString('fr-FR', { weekday: 'short', day: '2-digit', month: 'short' }) + ' ' + now.toLocaleTimeString('fr-FR');
        h.innerText = str;
    }
    setInterval(updateClock, 1000);
    updateClock();

    // Toggle Sidebar Mobile
    const toggleBtn = document.getElementById('btn-sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            sidebar.classList.toggle('show');
        });
        document.addEventListener('click', () => {
            sidebar.classList.remove('show');
        });
        sidebar.addEventListener('click', (e) => e.stopPropagation());
    }

    // Auto-close alertes
    document.querySelectorAll('.alert').forEach(a => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(a);
            if (bsAlert) bsAlert.close();
        }, 5000);
    });
});
