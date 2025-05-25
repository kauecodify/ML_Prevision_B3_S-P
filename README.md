# Monitor de Mercado Inteligente

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Status](https://img.shields.io/badge/Status-Ativo-green.svg)

Um monitor de mercado em tempo real com capacidade de previsão de preços usando regressão linear, atualizando a cada 5 segundos.

## 📌 Funcionalidades Principais

- **Monitoramento em tempo real** de ações, moedas e índices
- **Previsão de preços** usando modelos de regressão linear individuais para cada ativo
- **Atualização automática** a cada 5 segundos
- **Visualização intuitiva** no console com:
  - Preço atual
  - Variação percentual
  - Previsão do próximo preço
  - Erro percentual da última previsão
- **Armazenamento de dados** em arquivo Excel na área de trabalho

## 📋 Ativos Monitorados

### Moedas e Índices
- EUR/USD
- USD/BRL
- IBOVESPA
- S&P 500

### Ações Brasileiras
- Petrobras (PETR4)
- Vale (VALE3)
- Itaú (ITUB4)

### Ações Americanas
- Apple (AAPL)
- Microsoft (MSFT)
- Tesla (TSLA)

## ⚙️ Requisitos

- Python 3.8+
- Pacotes necessários (instalados automaticamente):
  ```bash
  pip install pandas yfinance scikit-learn numpy
  ```

## 🚀 Como Usar

1. Clone o repositório ou copie o código para um arquivo `.py`
2. Execute o script:
   ```bash
   python monitor_mercado.py
   ```
3. O sistema iniciará automaticamente o monitoramento
4. Pressione `Ctrl+C` para encerrar

## 📊 Saída Exemplo

```
14:30:15 - Dados atualizados
          Nome  Último Variação (%) Previsão Erro (%)
      EUR/USD   5.4321       0.12%    5.4412   0.17%
      USD/BRL   4.8765      -0.23%    4.8821   0.11%
     IBOVESPA 112345.67     0.45% 112400.20   0.05%
      S&P 500   4123.45     0.32%   4125.10   0.04%
    Petrobras    32.50      1.25%     32.45   -0.15%
         Vale    67.89     -0.15%     67.95    0.09%
        Itaú    25.30      0.40%     25.28   -0.08%
       Apple   175.43      0.87%    175.50    0.04%
   Microsoft   328.90      0.65%    328.75   -0.05%
       Tesla   895.32     -1.20%    894.50   -0.09%

Arquivo salvo em: C:\Users\[usuário]\Desktop\dados_mercado_inteligente.xlsx
```

## 📈 Sobre o Modelo Preditivo

- Utiliza **Regressão Linear** do scikit-learn
- Cada ativo tem seu próprio modelo treinado
- Requer mínimo de 10 pontos históricos para começar a prever
- Dados são normalizados com `MinMaxScaler` antes do treinamento
- Calcula e exibe o erro percentual das previsões

## 📂 Estrutura de Arquivos

- `dados_mercado_inteligente.xlsx`: Dados completos salvos na área de trabalho
- `historico_analises.json` (opcional): Histórico de análises (se implementado)

## 🔄 Atualizações Futuras

- [ ] Adicionar mais ativos
- [ ] Implementar outros modelos (Random Forest, LSTM)
- [ ] Criar sistema de alertas
- [ ] Adicionar interface gráfica

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
