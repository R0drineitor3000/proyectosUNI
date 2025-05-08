document.querySelectorAll('area').forEach(area => {
        area.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);

            closePanel();

            document.getElementById(targetId).classList.add('active');
            document.getElementById('computerImage').classList.add('active');
        });
    });

    function closePanel() {
        document.querySelectorAll('.info-panel').forEach(panel => {
            panel.classList.remove('active');
        });
        document.getElementById('computerImage').classList.remove('active');
    }