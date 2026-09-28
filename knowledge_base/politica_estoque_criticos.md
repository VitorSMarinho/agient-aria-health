# Política de Estoque — Itens Críticos (fictício)

> Documento interno fictício, criado para demonstrar a camada de RAG do ARIA.

## Classificação de criticidade

Um item entra na lista de "críticos" quando o estoque atual fica abaixo de
15% da média de consumo dos últimos 30 dias, ou quando resta menos de 7 dias
de cobertura projetada.

## Quimioterápicos

Itens da categoria quimioterápico têm reposição obrigatória em até 48h após
entrarem em criticidade, dada a impossibilidade de substituição rápida por
fornecedor alternativo.

## Itens vencendo

Itens com validade em até 30 dias devem ser sinalizados para uso prioritário
(FEFO — first expired, first out) antes de qualquer novo lote ser aberto.

## Reposição automática

Analgésicos e antieméticos têm ponto de pedido automático configurado;
insumos gerais dependem de aprovação manual do responsável de suprimentos.
