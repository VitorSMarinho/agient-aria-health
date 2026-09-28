# Manual Financeiro — Gestão de Inadimplência (fictício)

> Documento interno fictício, criado para demonstrar a camada de RAG do ARIA.

## Classificação de atraso

Pagamentos são classificados como "pendentes" até 15 dias após o vencimento
e como "atrasados" a partir do 16º dia, quando entram no fluxo de cobrança.

## Fluxo de cobrança

O fluxo de cobrança tem três etapas: lembrete automático (dia 16), contato
direto do financeiro (dia 30) e renegociação formal (dia 45). Contas acima
de R$ 10.000 pulam direto para contato direto do financeiro.

## Projeção de risco

Convênios com mais de 20% dos pagamentos atrasados no trimestre entram em
revisão de contrato. Pacientes particulares com dois atrasos consecutivos
passam a exigir pagamento antecipado para novos procedimentos eletivos.
