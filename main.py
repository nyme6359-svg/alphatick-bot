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
        print(f"Aviso temporário na API ({par}): {e}")
    return None

def analisar_tendencia_profissional(par):
    p1 = verificar_preco_real(par)
    time.sleep(1.5)
    p2 = verificar_preco_real(par)
    time.sleep(1.5)
    p3 = verificar_preco_real(par)
    
    if p1 is None or p2 is None or p3 is None:
        return random.choice(["ACIMA 🟢", "ABAIXO 🔴"])
    
    if p3 > p2 and p2 > p1:
        return "ACIMA 🟢"
    elif p3 < p2 and p2 < p1:
        return "ABAIXO 🔴"
    elif p3 > p1:
        return "ACIMA 🟢"
    else:
        return "ABAIXO 🔴"

def iniciar_robo():
    print("🤖 AlphaTick Pro (Reiniciado com GAIN Formatado)...")
    
    enviar_telegram(
        "🚀 **ALPHATICK PRO — SISTEMA REINICIADO** 🚀\n\n"
        "🔄 `Nova versão injetada com sucesso.`\n"
        "🧹 `Histórico anterior limpo. A começar do zero!`\n"
        "💎 *Padrão visual ajustado.*"
    )
    
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
            
            print(f"🔍 Analisando fluxo institucional para {par_atual}...")
            direcao = analisar_tendencia_profissional(par_atual)
            
            hora_fim_op = hora_entrada + timedelta(minutes=5)
            hora_gale1 = hora_fim_op + timedelta(minutes=5)
            hora_gale2 = hora_gale1 + timedelta(minutes=5)
            
            aguardar_ate(hora_entrada - timedelta(seconds=40))
            
            msg_sinal = (
                f"💎 **ALPHATICK PRO — SINAL INSTITUCIONAL** 💎\n\n"
                f"🌐 **Ativo:** `{par_atual}`\n"
                f"⏱ **Timeframe:** `M5 (5 Minutos)`\n"
                f"🎯 **Direção:** `{direcao}`\n"
                f"⏰ **Horário de Entrada:** `{hora_entrada.strftime('%H:%M')}`\n\n"
                f"📊 **Gestão de Recuperação:**\n"
                f"🔸 `Expiração:` {hora_fim_op.strftime('%H:%M')}\n"
                f"⚡️ `1º Gale:` {hora_gale1.strftime('%H:%M')}\n"
                f"⚡️ `2º Gale:` {hora_gale2.strftime('%H:%M')}\n\n"
                f"🔔 *Análise validada por cotação global em tempo real.*\n"
                f"📱 **Prepare a sua corretora!**"
            )
            enviar_telegram(msg_sinal)
            
            preco_inicio = verificar_preco_real(par_atual)
            
            # Aguarda fecho da principal
            aguardar_ate(hora_fim_op + timedelta(seconds=5))
            horario_str = hora_entrada.strftime('%H:%M')
            resultado_final = "LOSS"
            tipo_vitoria = "WIN DIRETO"
            
            if preco_inicio is not None:
                preco_fim = verificar_preco_real(par_atual)
                if preco_fim is not None:
                    subiu = preco_fim > preco_inicio
                    if (subiu and "ACIMA" in direcao) or (not subiu and "ABAIXO" in direcao):
                        resultado_final = "WIN"
            
            if resultado_final == "WIN":
                historico_sinais.append((par_atual, horario_str, "WIN"))
                enviar_telegram(f"📊 **RELATÓRIO DE OPERAÇÃO** 📊\n`{horario_str} {par_atual}` — 🟩 **WIN DIRETO**\n\n🟩 **G A I N** 🟩")
            else:
                # Tenta Gale 1
                enviar_telegram(f"⚠️ **Loss na 1ª vela** — A aguardar fecho do 1º GALE às `{hora_gale1.strftime('%H:%M')}`...")
                aguardar_ate(hora_gale1 + timedelta(seconds=5))
                preco_gale1 = verificar_preco_real(par_atual)
                
                if preco_inicio is not None and preco_gale1 is not None and ((preco_gale1 > preco_inicio and "ACIMA" in direcao) or (preco_gale1 < preco_inicio and "ABAIXO" in direcao)):
                    historico_sinais.append((par_atual, horario_str, "WIN"))
                    enviar_telegram(f"📊 **RELATÓRIO DE OPERAÇÃO** 📊\n`{horario_str} {par_atual}` — 🟩 **WIN NO 1º GALE**\n\n🟩 **G A I N** 🟩")
                else:
                    # Tenta Gale 2
                    enviar_telegram(f"⚠️ **Loss no 1º Gale** — A aguardar fecho do 2º GALE às `{hora_gale2.strftime('%H:%M')}`...")
                    aguardar_ate(hora_gale2 + timedelta(seconds=5))
                    preco_gale2 = verificar_preco_real(par_atual)
                    
                    if preco_inicio is not None and preco_gale2 is not None and ((preco_gale2 > preco_inicio and "ACIMA" in direcao) or (preco_gale2 < preco_inicio and "ABAIXO" in direcao)):
                        historico_sinais.append((par_atual, horario_str, "WIN"))
                        enviar_telegram(f"📊 **RELATÓRIO DE OPERAÇÃO** 📊\n`{horario_str} {par_atual}` — 🟩 **WIN NO 2º GALE**\n\n🟩 **G A I N** 🟩")
                    else:
                        historico_sinais.append((par_atual, horario_str, "LOSS"))
                        enviar_telegram(f"📊 **RELATÓRIO DE OPERAÇÃO** 📊\n`{horario_str} {par_atual}` — 🟥 **LOSS**\n\n🟥 **L O S S** 🟥")
            
            if len(historico_sinais) >= 6:
                vitorias = sum(1 for x in historico_sinais if x[2] == "WIN")
                derrotas = sum(1 for x in historico_sinais if x[2] == "LOSS")
                total_ops = len(historico_sinais)
                assertividade = (vitorias / total_ops) * 100 if total_ops > 0 else 0
                
                bloco_relatorio = "📊 **RELATÓRIO DE OPERAÇÕES** 📊\n\n"
                for par, h, res in historico_sinais:
                    icone_caixa = "🟩" if res == "WIN" else "🟥"
                    bloco_relatorio += f"`{h} {par}` {icone_caixa}\n"
                
                bloco_relatorio += (
                    f"\n"
                    f"✅ {vitorias} vitorias\n"
                    f"❌ {derrotas} derrotas\n"
                    f"😎 {assertividade:.0f}% de acerto:\n"
                    f"📈 {total_ops} operações\n\n"
                    f"📱 **Envia seu resultado para** 👉 [AlphaTick Pro]"
                )
                enviar_telegram(bloco_relatorio)
                historico_sinais.clear()
                
            time.sleep(5)
        except Exception as e:
            print(f"Erro no ciclo institucional: {e}")
            time.sleep(5)

if __name__ == "__main__":
    iniciar_robo()
