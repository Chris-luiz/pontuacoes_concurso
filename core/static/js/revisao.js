const menuFlutuante = document.getElementById('menuFlutuante');
const btnMinimizar = document.getElementById('btnMinimizar');
const btnLimparCorretas = document.getElementById('btnLimparCorretas');
const btnLimparInseridas = document.getElementById('btnLimparInseridas');
const btnLimparTudo = document.getElementById('btnLimparTudo');
const btnVoltarTopo = document.getElementById('btnVoltarTopo');
const btnIrFinal = document.getElementById('btnIrFinal');
const btnOcultarRespostasCertas = document.getElementById('btnOcultarRespostasCertas');
const btnOcultarRespostasInseridas = document.getElementById('btnOcultarRespostasInseridas');
const btnOcultarAcertos = document.getElementById('btnOcultarAcertos');

btnVoltarTopo.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    })
});

btnIrFinal.addEventListener('click', () => {
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });
});

btnOcultarRespostasCertas.addEventListener('click', (e) => {
    e.target.innerText = 'Exibir Respostas Corretas';
    document.querySelectorAll('.td-resposta-correta').forEach(el => {
        el.classList.toggle('is-hidden');
    });
});

btnOcultarRespostasInseridas.addEventListener('click', (e) => {
    e.target.innerText = 'Exibir Respostas Inseridas';
    document.querySelectorAll('.td-resposta-inserida').forEach(el => {
        el.classList.toggle('is-hidden');
    });
});

btnOcultarAcertos.addEventListener('click', (e) => {
    e.target.innerText = 'Exibir Acertos';
    document.querySelectorAll('.td-valor').forEach(el => {
        el.classList.toggle('is-hidden');
    });
});


btnMinimizar.addEventListener('click', function () {
    menuFlutuante.classList.toggle('minimizado');

    if (menuFlutuante.classList.contains('minimizado')) {
        btnMinimizar.textContent = '+';
        btnMinimizar.title = 'Expandir';

    } else {
        btnMinimizar.textContent = '−';
        btnMinimizar.title = 'Minimizar';

    }
});

btnLimparCorretas.addEventListener('click', function () {
    const selects = document.querySelectorAll('.select-resposta-correta');

    selects.forEach(function (select) {
        select.value = '';
    });

});

btnLimparInseridas.addEventListener('click', function () {
    const selects = document.querySelectorAll('.select-resposta-inserida');

    selects.forEach(function (select) {
        select.value = '';
    });
});

btnLimparTudo.addEventListener('click', function () {
    const selects = document.querySelectorAll('.select-resposta-correta, .select-resposta-inserida');

    selects.forEach(function (select) {
        select.value = '';
    });
});

const atualizarMetricas = () => {
    let erros = 0;
    let acertos = 0;
    let quantidade = document.querySelectorAll('.td-valor').length;

    document.querySelectorAll('.td-valor').forEach(el => {
        const span = el.querySelector('span');

        if (span.innerText == 'ACERTO') {
            acertos += 1;
        }

        if (span.innerText == 'ERRO') {
            erros += 1;
        }
    });

    document.querySelector("#qtdAcertos").innerText = `${acertos} acertos`;
    document.querySelector("#qtdErros").innerText = `${erros} acertos`;
    document.querySelector("#percentAcertos").innerText = `${Math.round(acertos * 100 / quantidade)}% acertos`;
}

const alterarTag = (tag, alterar) => {
    if (alterar) {
        tag.innerText = 'ACERTO';
        tag.classList.add('is-primary');
        tag.classList.remove('is-danger');
    } else {
        tag.innerText = 'ERRO';
        tag.classList.remove('is-primary');
        tag.classList.add('is-danger');
    }
}
document.querySelectorAll('.select-resposta-correta').forEach(select => {
    select.addEventListener('change', (e) => {
        const responstaCorreta = e.target;
        const nameNumero = responstaCorreta.getAttribute('name').split('_')[2];

        const respostaInserida = document.querySelector(`[name=resposta_inserida_${nameNumero}]`).value

        const td = document.querySelector(`[data-id="${nameNumero}"]`).querySelector('span');

        alterarTag(td, responstaCorreta.value == respostaInserida);

        atualizarMetricas();
    });
});



document.querySelectorAll('.select-resposta-inserida').forEach(select => {
    select.addEventListener('change', (e) => {
        const respostaInserida = e.target;
        const nameNumero = respostaInserida.getAttribute('name').split('_')[2];

        const respostaCorreta = document.querySelector(`[name=resposta_correta_${nameNumero}]`).value

        const td = document.querySelector(`[data-id="${nameNumero}"]`).querySelector('span');

        alterarTag(td, respostaInserida.value == respostaCorreta);

        atualizarMetricas();
    });
});

atualizarMetricas();