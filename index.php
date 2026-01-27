<?php

class Prova
{
    private array $questoes =  [
        'Lingua Portuguesa' => [
            'Q1' => false,
            'Q2' => false,
            'Q3' => true,
            'Q4' => true,
            'Q5' => false,
            'Q6' => false,
            'Q7' => false,
            'Q8' => true,
            'Q9' => false,
            'Q10' => true,
        ],

        'Raciocínio Lógico' => [
            'Q11' => true,
            'Q12' => false,
            'Q13' => false,
            'Q14' => false,
            'Q15' => false,
        ],

        'Administração Financeira Orçamentária' => [
            'Q16' => false,
            'Q17' => true,
            'Q18' => false,
            'Q19' => false,
            'Q20' => true,
            'Q21' => false,
            'Q22' => false,
            'Q23' => false,
            'Q24' => false,
            'Q25' => false,
        ],

        'Controle Interno e Externo' => [
            'Q26' => true,
            'Q27' => true,
            'Q28' => false,
            'Q29' => false,
            'Q30' => true,
            'Q31' => true,
            'Q32' => false,
            'Q33' => false,
            'Q34' => true,
            'Q35' => true,
        ],

        'Direto Administrativo' => [
            'Q36' => false,
            'Q37' => false,
            'Q38' => false,
            'Q39' => false,
            'Q40' => false,
            'Q41' => false,
            'Q42' => true,
            'Q43' => true,
            'Q44' => false,
            'Q45' => false,
        ],

        'Legislação Municipal' => [
            'Q46' => true,
            'Q47' => true,
            'Q48' => true,
            'Q49' => false,
            'Q50' => true,
        ],

        'Conhecimento Específico' => [
            'Q51' => true,
            'Q52' => true,
            'Q53' => true,
            'Q54' => true,
            'Q55' => false,
            'Q56' => true,
            'Q57' => false,
            'Q58' => true,
            'Q59' => false,
            'Q60' => false,
            'Q61' => true,
            'Q62' => true,
            'Q63' => false,
            'Q64' => true,
            'Q65' => true,
            'Q66' => true,
            'Q67' => true,
            'Q68' => true,
            'Q69' => true,
            'Q70' => false,
        ],
    ];

    public function obterQuestoes(): array
    {
        return $this->questoes;
    }

    public function obterTotais(): array
    {
        $total = [];

        foreach ($this->questoes as $key => $questoes) {
            $total[$key] = count(array_filter($questoes));
        }

        $total['total'] = array_sum($total);

        return $total;
    }
}

$prova = new Prova();
$totais = $prova->obterTotais();

?>

<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }


        body {
            background: #f5f7fa;
        }


        .container {
            background: #ffffff;
            border-radius: 12px;
            margin: 40px auto;
            padding: 24px;
            max-width: 1100px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        }


        h2 {
            margin: 24px 0 12px;
            color: #1f2937;
            border-left: 4px solid #2563eb;
            padding-left: 8px;
            font-size: 1.2rem;
        }


        .flex {
            display: grid;
            grid-template-columns: repeat(10, 1fr);
            gap: 10px;
            margin-bottom: 8px;
        }


        .block {
            height: 42px;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            cursor: default;
        }


        .block:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.12);
        }


        .acerto {
            background: #22c55e;
            color: #ffffff;
        }


        .erro {
            background: #ef4444;
            color: #ffffff;
        }


        p {
            margin: 6px 0 16px;
            font-weight: 500;
            color: #374151;
        }


        h3 {
            margin-top: 24px;
            font-size: 1.4rem;
            text-align: center;
        }


        .texto-acerto {
            color: #16a34a;
        }


        .texto-erro {
            color: #dc2626;
        }
    </style>
</head>

<body>
    <div class="container">
        <?php foreach ($prova->obterQuestoes() as $materia => $questoes): ?>

            <h2><?= $materia ?></h2>

            <div class="flex">
                <?php foreach ($questoes as $questao => $valor): ?>
                    <div class="block <?= $valor ? 'acerto' : 'erro' ?>"> <?= $questao ?>: <?= $valor ? 'Acertou' : "Errou" ?> </div>
                <?php endforeach; ?>
            </div>

            <p>Total: <?= $totais[$materia] ?> Pontos</p>

            <br>

        <?php endforeach; ?>

        <h3 class="<?= $totais['total'] > 48 ? 'texto-acerto' : 'texto-erro' ?>">Nota Final: <?= $totais['total'] ?></h3>
    </div>

</body>

</html>