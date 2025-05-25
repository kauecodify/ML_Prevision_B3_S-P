# -*- coding: utf-8 -*-
"""
Monitoramento com Regressão Linear para Previsão (atualização a cada 5 segundos)
"""

import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime
import time
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler

class MonitorInteligente:
    def __init__(self):
        self.arquivo_dados = os.path.join(os.path.expanduser('~'), 'Desktop', 'dados_mercado_inteligente.xlsx')
        self.ativos = {
            
# --------------------------------------------------------------------------- #
            # Moedas e Índices
            "EURUSD=X": "EUR/USD",
            "BRL=X": "USD/BRL",
            "^BVSP": "IBOVESPA",
            "^GSPC": "S&P 500",
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
            # Ações Brasileiras
            "PETR4.SA": "Petrobras",
            "VALE3.SA": "Vale",
            "ITUB4.SA": "Itaú",
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
            # Ações Americanas
            "AAPL": "Apple",
            "MSFT": "Microsoft",
            "TSLA": "Tesla"
        }
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
        self.modelos = {ticker: LinearRegression() for ticker in self.ativos}
        self.scalers = {ticker: MinMaxScaler() for ticker in self.ativos}
        self.historico = {ticker: pd.DataFrame() for ticker in self.ativos}
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
    def preparar_dados_treinamento(self, dados_historicos):
        """Prepara dados para o modelo de ML"""
        X = np.arange(len(dados_historicos)).reshape(-1, 1)
        y = dados_historicos['Close'].values.reshape(-1, 1)
        
        # Normalização
        X_scaled = self.scalers[dados_historicos['Ticker'].iloc[0]].fit_transform(X)
        
        return X_scaled, y
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
    def treinar_modelo(self, ticker):
        """Treina o modelo com os dados históricos"""
        if len(self.historico[ticker]) < 10:  # Mínimo de 10 pontos para treino
            return
        
        try:
            X, y = self.preparar_dados_treinamento(self.historico[ticker])
            self.modelos[ticker].fit(X, y)
        except Exception as e:
            print(f"Erro ao treinar modelo para {ticker}: {str(e)}")
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
    def prever_proximo_preco(self, ticker):
        """Faz a previsão do próximo preço"""
        if len(self.historico[ticker]) < 10:
            return None
        
        try:
            ultimo_idx = len(self.historico[ticker])
            X_proximo = np.array([[ultimo_idx]])
            X_proximo_scaled = self.scalers[ticker].transform(X_proximo)
            return self.modelos[ticker].predict(X_proximo_scaled)[0][0]
        except:
            return None
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
    def baixar_dados_rapido(self):
        """Baixa e processa dados do mercado"""
        try:
            dados = yf.download(
                tickers=list(self.ativos.keys()),
                period="1d",
                interval="1m",
                group_by='ticker'
            )
            
            resultados = []
            for ticker, nome in self.ativos.items():
                if ticker in dados:
                    df = dados[ticker].copy()
                    df['Ticker'] = ticker
                    df['Nome'] = nome
                    
                    # Atualiza histórico
                    self.historico[ticker] = pd.concat([self.historico[ticker], df.tail(1)])
                    
                    # Treina modelo
                    self.treinar_modelo(ticker)
                    
                    # Faz previsão
                    previsao = self.prever_proximo_preco(ticker)
                    
                    # Calcula variação
                    df['Último'] = df['Close']
                    df['Variação (%)'] = df['Close'].pct_change() * 100
                    df['Previsão'] = previsao if previsao else np.nan
                    df['Erro (%)'] = ((previsao - df['Close'].iloc[-1]) / df['Close'].iloc[-1]) * 100 if previsao else np.nan
                    
                    resultados.append(df[['Ticker', 'Nome', 'Último', 'Variação (%)', 'Previsão', 'Erro (%)']].tail(1))
            
            return pd.concat(resultados) if resultados else pd.DataFrame()
            
        except Exception as e:
            print(f"Erro ao baixar dados: {e}")
            return pd.DataFrame()
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
    def salvar_dados(self, dados):
        """Salva os dados e mostra resumo"""
        if not dados.empty:
            try:
                dados.to_excel(self.arquivo_dados)
                print(f"\n{datetime.now().strftime('%H:%M:%S')} - Dados atualizados")
                
                # Formata saída para melhor legibilidade
                dados_exibir = dados.copy()
                dados_exibir['Último'] = dados_exibir['Último'].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "N/A")
                dados_exibir['Variação (%)'] = dados_exibir['Variação (%)'].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else "N/A")
                dados_exibir['Previsão'] = dados_exibir['Previsão'].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "N/A")
                dados_exibir['Erro (%)'] = dados_exibir['Erro (%)'].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else "N/A")
                
                print(dados_exibir[['Nome', 'Último', 'Variação (%)', 'Previsão', 'Erro (%)']].to_string(index=False))
                print(f"\nArquivo salvo em: {self.arquivo_dados}")
            except Exception as e:
                print(f"Erro ao salvar: {e}")
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
    def monitorar(self):
        """Loop principal de monitoramento"""
        print("\n=== MONITOR INTELIGENTE - ATUALIZAÇÃO A CADA 5 SEGUNDOS ===")
        print("Ativos monitorados:")
        for nome in self.ativos.values():
            print(f"- {nome}")
        print("\nPressione Ctrl+C para parar\n")
        
        try:
            while True:
                inicio = time.time()
                dados = self.baixar_dados_rapido()
                self.salvar_dados(dados)
                
                tempo_execucao = time.time() - inicio
                espera = max(0.1, 5 - tempo_execucao)
                time.sleep(espera)
                
        except KeyboardInterrupt:
            print("\nMonitoramento encerrado")

if __name__ == "__main__":
    monitor = MonitorInteligente()
# --------------------------------------------------------------------------- #

# --------------------------------------------------RUN---------------------- #
    monitor.monitorar()
# --------------------------------------------------------------------------- #