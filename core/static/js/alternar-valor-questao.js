const alternarValorQuestao = async (id) => {
    const res = await fetch(`/provas/alternar_valor_questao/${id}`, );
    const response = await res.json();
    
    if (response && response.status) {
        const { questaoId, valor } = response;
        const questao = document.querySelector(`[data-id='${questaoId}']`).querySelector('span');
        questao.innerText = valor ? "SIM" : "NÃO" ;
        questao.classList.toggle('is-primary');
        questao.classList.toggle('is-danger');
    }
}