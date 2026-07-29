import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta
import time
import random

TELEGRAM_TOKEN = "8787520019:AAHG9i_ng32anoh_DWtLFjdrZIPjTDK-lRs"
CHAT_ID = "771454310"

# Lista exclusiva de Pares de Mercado Aberto (Com cotação real na nuvem)
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
    """Consulta cotação real para validação exata do mercado"""
    try:
        simbolo = par.replace("/", "")
        url = f"https://economia.awesomeapi.com.br/json/last/{simbolo}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            dados = json.loads(response.read().decode())
            chave = simbolo
            if chave in dados:
                bid = float(dados[chave]["bid"])
                return bid
    except Exception as e:
        print(f"Erro ao consultar preço real ({par}): {e}")
    return None

def iniciar_robo():
    print("🤖 AlphaTick Pro (Modo Mercado 100% Real Ativo)...")
    
    historico_sinais = []
    
    while True:
        try:
            agora = datetime.now()
            
            # Alinha estritamente ao próximo múltiplo de 5 minutos
            minuto_atual = agora.minute
            extra = 5 - (minuto_atual % 5)
            if extra == 0:
                extra = 5
                
            hora_entrada = agora.replace(second=0, microsecond=0) + timedelta(minutes=extra)
            
            par_atual = random.choice(PARES_ABERTOS)
            direcao = random.choice(["ACIMA 🟢", "ABAIXO 🔴"])
            
            hora_fim_op = hora_entrada + timedelta(minutes=5)
            hora_gale1 = hora_fim_op + timedelta(minutes=5)
            hora_gale2 = hora_gale1 + timedelta(minutes=5)
            
            # Aguarda até faltarem 40 segundos para a entrada
            aguardar_ate(hora_entrada - timedelta(seconds=40))
            
            msg_sinal = (
                f"📊 **OPORTUNIDADE MERCADO REAL** 📊\n\n"
                f"⏱ **5 minutos de operação**\n"
                f"🪙 `{par_atual}` `{hora_entrada.strftime('%H:%M')}` `{direcao}`\n\n"
                f"⏰ **Termina às:** `{hora_fim_op.strftime('%H:%M')}`\n"
                f"⚡️ **1º GALE TERMINA ÀS** `{hora_gale1.strftime('%H:%M')}`\n"
                f"⚡️ **2º GALE TERMINA ÀS** `{hora_gale2.strftime('%H:%M')}`\n"
                f"📱 **Prepare-se para entrar na corretora!**"
            )
            enviar_telegram(msg_sinal)
            
            # Captura o preço exato de abertura da operação
            preco_inicio = verificar_preco_real(par_atual)
            
            # Aguarda o fecho da operação principal (5 min)
            aguardar_ate(hora_fim_op + timedelta(seconds=5))
            
            horario_str = hora_entrada.strftime('%H:%M')
            resultado_final = "LOSS"
            
            if preco_inicio is not None:
                preco_fim = verificar_preco_real(par_atual)
                if preco_fim is not None:
                    subiu = preco_fim > preco_inicio
                    acertou = (subiu and "ACIMA" in direcao) or (not subiu and "ABAIXO" in direcao)
                    if acertou:
                        resultado_final = "WIN"
            
            # Validação do resultado com base na cotação real ou ciclos de recuperação
            if resultado_final == "WIN":
                historico_sinais.append((par_atual, horario_str, "WIN"))
            else:
                # Se deu loss no direto, testa o Gale 1 com cotação atualizada
                aguardar_ate(hora_gale1 + timedelta(seconds=5))
                preco_gale1 = verificar_preco_real(par_atual)
                if preco_inicio is not None and preco_gale1 is not None and preco_gale1 > preco_inicio and "ACIMA" in direcao:
                    historico_sinais.append((par_atual, horario_str, "WIN"))
                elif preco_inicio is not None and preco_gale1 is not None and preco_gale1 < preco_inicio and "ABAIXO" in direcao:
                    historico_sinais.append((par_atual, horario_str, "WIN"))
                else:
                    # Tenta o Gale 2
                    aguardar_ate(hora_gale2 + timedelta(seconds=5))
                    preco_gale2 = verificar_preco_real(par_atual)
                    if preco_inicio is not None and preco_gale2 is not None and preco_gale2 > preco_inicio and "ACIMA" in direcao:
                        historico_sinais.append((par_atual, horario_str, "WIN"))
                    elif preco_inicio is not None and preco_gale2 is not None and preco_gale2 < preco_inicio and "ABAIXO" in direcao:
                        historico_sinais.append((par_atual, horario_str, "WIN"))
                    else:
                        historico_sinais.append((par_atual, horario_str, "LOSS"))
            
            # Relatório Profissional a cada 6 operações
            if len(historico_sinais) >= 6:
                vitorias = sum(1 for x in historico_sinais if x[2] == "WIN")
                derrotas = sum(1 for x in historico_sinais if x[2] == "LOSS")
                total_ops = len(historico_sinais)
                assertividade = (vitorias / total_ops) * 100 if total_ops > 0 else 0
                
                bloco_relatorio = "📊 **RELATÓRIO DE OPERAÇÕES (REAL)** 📊\n\n"
                for par, h, res in historico_sinais:
                    icone_res = "✅" if res == "WIN" else "❌"
                    bloco_relatorio += f"{h} {par} {icone_res}\n"
                
                bloco_relatorio += (
                    f"\n✅ {vitorias} vitórias\n"
                    f"❌ {derrotas} derrotas\n"
                    f"😎 {assertividade:.1f}% de acerto\n"
                    f"📈 {total_ops} operações"
                )
                enviar_telegram(bloco_relatorio)
                historico_sinais.clear()
                
            time.sleep(5)
            
        except Exception as e:
            print(f"Erro no ciclo real: {e}")
            time.sleep(5)

if __name__ == "__main__":
    iniciar_robo()
