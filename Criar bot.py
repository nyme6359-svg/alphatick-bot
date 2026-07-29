import urllib.request
import urllib.parse
from datetime import datetime, timedelta
import time
import random

TELEGRAM_TOKEN = "8787520019:AAHG9I_nG32anoh_9MsLFjdrZIPjTDK-IRs"
CHAT_ID = "7714545310"

PARES = [
    "USD/PHP (OTC)", "USD/BDT (OTC)", "USD/IDR (OTC)", "USD/PKR (OTC)", 
    "USD/JPY (OTC)", "USD/BRL (OTC)", "USD/ARS (OTC)", "USD/EGP (OTC)", 
    "GBP/JPY (OTC)", "USD/TRY (OTC)", "USD/CAD (OTC)", "GBP/USD (OTC)",
    "GBP/NZD (OTC)", "USD/COP (OTC)", "AUD/USD (OTC)", "USD/NGN (OTC)"
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
        time.sleep(0.5)

def iniciar_robo():
    print("🤖 AlphaTick Pro (Nuvem 24/7) Ativo...")
    
    while True:
        try:
            agora = datetime.now()
            
            # Alinha ao próximo múltiplo de 5 minutos
            minuto_atual = agora.minute
            proximo_minuto = minuto_atual + (5 - (minuto_atual % 5))
            if proximo_minuto >= 60:
                proximo_minuto = 0
                
            hora_entrada = agora.replace(minute=proximo_minuto, second=0, microsecond=0)
            if hora_entrada <= agora:
                hora_entrada += timedelta(minutes=5)

            par_atual = random.choice(PARES)
            direcao = random.choice(["ACIMA 🟢", "ABAIXO 🔴"])
            
            hora_fim_op = hora_entrada + timedelta(minutes=5)
            hora_gale1 = hora_fim_op + timedelta(minutes=5)
            hora_gale2 = hora_gale1 + timedelta(minutes=5)

            # Aguarda até faltarem 40 segundos para a entrada
            aguardar_ate(hora_entrada - timedelta(seconds=40))

            # Envia o Sinal
            msg_sinal = (
                f"💲 **OPORTUNIDADE ENCONTRADA** 💲\n\n"
                f"⏱️ **5 minutos de operação**\n"
                f"📊 `{par_atual}` {hora_entrada.strftime('%H:%M')} {direcao}\n\n"
                f"⏰ **Termina às:** `{hora_fim_op.strftime('%H:%M')}`\n"
                f"⚡ **1º GALE TERMINA ÀS** `{hora_gale1.strftime('%H:%M')}`\n"
                f"⚡ **2º GALE TERMINA ÀS** `{hora_gale2.strftime('%H:%M')}`\n\n"
                f"📲 *Prepare-se para entrar na corretora!*"
            )
            enviar_telegram(msg_sinal)

            # Aguarda o fecho da operação principal (5 min)
            aguardar_ate(hora_fim_op)

            sorteio = random.random()
            horario_str = hora_entrada.strftime('%H:%M')

            if sorteio < 0.55:
                enviar_telegram(
                    f"📊 **RELATÓRIO DE OPERAÇÃO** 📊\n"
                    f"🕒 `{horario_str}` `{par_atual}` — ✅ **WIN DIRETO**\n\n"
                    f"🟩 **G A I N** 🟩"
                )
            else:
                enviar_telegram(f"⚠️ **Loss na 1ª vela** — A aguardar fecho do **1º GALE** às `{hora_gale1.strftime('%H:%M')}`...")
                aguardar_ate(hora_gale1)

                if random.random() < 0.70:
                    enviar_telegram(
                        f"📊 **RELATÓRIO DE OPERAÇÃO** 📊\n"
                        f"🕒 `{horario_str}` `{par_atual}` — ✅ **WIN NO 1º GALE**\n\n"
                        f"🟩 **G A I N** 🟩"
                    )
                else:
                    enviar_telegram(f"⚠️ **Loss no 1º Gale** — A aguardar fecho do **2º GALE (FINAL)** às `{hora_gale2.strftime('%H:%M')}`...")
                    aguardar_ate(hora_gale2)

                    if random.random() < 0.60:
                        enviar_telegram(
                            f"📊 **RELATÓRIO DE OPERAÇÃO** 📊\n"
                            f"🕒 `{horario_str}` `{par_atual}` — ✅ **WIN NO 2º GALE**\n\n"
                            f"🟩 **G A I N** 🟩"
                        )
                    else:
                        enviar_telegram(
                            f"📊 **RELATÓRIO DE OPERAÇÃO** 📊\n"
                            f"🕒 `{horario_str}` `{par_atual}` — ❌ **LOSS**\n\n"
                            f"🟥 **DERROTA** 🟥"
                        )

            time.sleep(1)

        except Exception as e:
            print(f"Erro no ciclo: {e}")
            time.sleep(2)

if __name__ == "__main__":
    iniciar_robo()
    
