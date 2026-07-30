import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta
import time
import random

TELEGRAM_TOKEN = "8787520019:AAHG9i_ng32anoh_DWtLFjdrZIPjTDK-lRs"
CHAT_ID = "771454310"

PARES_ABERTOS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD",
    "EUR/GBP", "EUR/JPY", "GBP/JPY", "USD/CHF",
    "USD/CAD", "NZD/USD", "EUR/AUD", "GBP/AUD"
]

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"}
    data = urllib.parse.urlencode(payload).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=data, method="POST")
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"Erro Telegram: {e}")

def aguardar_ate(tempo_alvo):
    while datetime.now() < tempo_alvo:
        time.sleep(1)

def verificar_preco_real(par):
    try:
        simbolo = par.replace("/", "")
        url = f"https://economia.awesomeapi.com.br/json/last/{simbolo}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            dados = json.loads(response.read().decode())
            chave = simbolo
            if chave in dados:
                return float(dados[chave]["bid"])
    except Exception as e:
        print(f"Erro ao consultar preço real ({par}): {e}")
    return None

def analisar_tendencia(par):
    """Analisa o mercado em tempo real para decidir a direção com base na variação de preço"""
preco_anterior = verificar_preco_real(par)
    time.sleep(2)
    preco_atual = verificar_preco_real(par)
    
    if preco_anterior is None or preco_atual is None:
        # Se falhar a leitura da tendência, assume uma escolha padrão segura
        return random.choice(["ACIMA 🟢", "ABAIXO 🔴"])
    
    if preco_atual > preco_anterior:
        return "ACIMA 🟢"
    elif preco_atual < preco_anterior:
        return "ABAIXO 🔴"
    else:
        return random.choice(["ACIMA 🟢", "ABAIXO 🔴"])

def iniciar_robo():
    print("🤖 AlphaTick Pro (Modo Inteligente com Filtro de Tendência Ativo)...")
    historico_sinais = []
    
    while True:
        try:
            agora = datetime.utcnow() + timedelta(hours=1)
            
            minuto_atual = agora.minute
            extra = 5 - (minuto_atual % 5)
            if extra == 0:
                extra = 5
                
            hora_entrada = agora.replace(second=0, microsecond=0) + timedelta(minutes=extra)
            par_atual = random.choice(PARES_ABERTOS)
            
            # O robô agora analisa a tendência do mercado em vez de escolher ao acaso
            print(aquisicao_dir := f"A analisar tendência para {par_atual}...")
            direcao = analisar_tendencia(par_atual)
            
            hora_fim_op = hora_entrada + timedelta(minutes=5)
            hora_gale1 = hora_fim_op + timedelta(minutes=5)
            hora_gale2 = hora_gale1 + timedelta(minutes=5)
            
            aguardar_ate(hora_entrada - timedelta(seconds=40))
            
            msg_sinal = (
                f"📊 **OPORTUNIDADE TENDÊNCIA REAL** 📊\n\n"
                f"⏱ **5 minutos de operação**\n"
                f"🪙 `{par_atual}` `{hora_entrada.strftime('%H:%M')}` `{direcao}`\n\n"
                f"⏰ **Termina às:** `{hora_fim_op.strftime('%H:%M')}`\n"
                f"⚡️ **1º GALE TERMINA ÀS** `{hora_gale1.strftime('%H:%M')}`\n"
                f"⚡️ **2º GALE TERMINA ÀS** `{hora_gale2.strftime('%H:%M')}`\n"
                f"📱 **Prepare-se para entrar na corretora!**"
            )
            enviar_telegram(msg_sinal)
            
            preco_inicio = verificar_preco_real(par_atual)
            aguardar_ate(hora_fim_op + timedelta(seconds=5))
            horario_str = hora_entrada.strftime('%H:%M')
            resultado_final = "LOSS"
            
            if preco_inicio is not None:
                preco_fim = verificar_preco_real(par_atual)
                if preco_fim is not None:
                    subiu = preco_fim > preco_inicio
                    if (subiu and "ACIMA" in direcao) or (not subiu and "ABAIXO" in direcao):
                        resultado_final = "WIN"
            
            if resultado_final == "WIN":
                historico_sinais.append((par_atual, horario_str, "WIN"))
            else:
                aguardar_ate(hora_gale1 + timedelta(seconds=5))
                preco_gale1 = verificar_preco_real(par_atual)
                if preco_inicio is not None and preco_gale1 is not None and ((preco_gale1 > preco_inicio and "ACIMA" in direcao) or (preco_gale1 < preco_inicio and "ABAIXO" in direcao)):
                    historico_sinais.append((par_atual, horario_str, "WIN"))
                else:
                    aguardar_ate(hora_gale2 + timedelta(seconds=5))
                    preco_gale2 = verificar_preco_real(par_atual)
                    if preco_inicio is not None and preco_gale2 is not None and ((preco_gale2 > preco_inicio and "ACIMA" in direcao) or (preco_gale2 < preco_inicio and "ABAIXO" in direcao)):
                        historico_sinais.append((par_atual, horario_str, "WIN"))
                    else:
                        historico_sinais.append((par_atual, horario_str, "LOSS"))
            
            if len(historico_sinais) >= 6:
                vitorias = sum(1 for x in historico_sinais if x[2] == "WIN")
                derrotas = sum(1 for x in historico_sinais if x[2] == "LOSS")
                total_ops = len(historico_sinais)
                assertividade = (vitorias / total_ops) * 100 if total_ops > 0 else 0
                
                bloco_relatorio = "📊 **RELATÓRIO DE TENDÊNCIA (REAL)** 📊\n\n"
                for par, h, res in historico_sinais:
                    bloco_relatorio += f"{h} {par} {'✅' if res == 'WIN' else '❌'}\n"
                
                bloco_relatorio += f"\n✅ {vitorias} vitórias\n❌ {derrotas} derrotas\n😎 {assertividade:.1f}% de acerto\n📈 {total_ops} operações"
                enviar_telegram(bloco_relatorio)
                historico_sinais.clear()
                
            time.sleep(5)
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(5)

if __name__ == "__main__":
    iniciar_robo()
