document.addEventListener('DOMContentLoaded', () => {

    const checkbox = document.querySelector("#id_criar_varios");
    const deInput = document.querySelector("#id_de");
    const ateInput = document.querySelector("#id_ate");

    if (!checkbox || !deInput || !ateInput) return;

    const deContainer = deInput.closest('div');
    const ateContainer = ateInput.closest('div');

    const toggleFields = (show) => {
        [deContainer, ateContainer].forEach(el => {
            el.classList.toggle('is-hidden', !show);
        });

        if (!show) {
            deInput.value = '';
            ateInput.value = '';
        }
    };

    toggleFields(checkbox.checked);

    checkbox.addEventListener('change', (e) => {
        toggleFields(e.target.checked);
    });
});