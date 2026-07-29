import urllib.request
import urllib.parse
from datetime import datetime, timedelta
import time
import random

TELEGRAM_TOKEN = "8787520019:AAHG9i_ng32anoh_DWtLFjdrZIPjTDK-lRs"
CHAT_ID = "771454310"

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
        time.sleep(1)

def iniciar_robo():
    print("🤖 AlphaTick Pro (Nuvem 24/7) - Modo Lendário Ativo...")
    
    historico_sinais = []
    
    while True:
        try:
            agora = datetime.now()
            
            minuto_atual = agora.minute
            extra = 5 - (minuto_atual % 5)
            if extra == 0:
                extra = 5
                
            hora_entrada = agora.replace(second=0, microsecond=0) + timedelta(minutes=extra)
            
            par_atual = random.choice(PARES)
            direcao = random.choice(["ACIMA 🟢", "ABAIXO 🔴"])
            
            hora_fim_op = hora_entrada + timedelta(minutes=5)
            hora_gale1 = hora_fim_op + timedelta(minutes=5)
            hora_gale2 = hora_gale1 + timedelta(minutes=5)
            
            aguardar_ate(hora_entrada - timedelta(seconds=40))
            
            msg_sinal = (
                f"📊 **OPORTUNIDADE ENCONTRADA** 📊\n\n"
                f"⏱ **5 minutos de operação**\n"
                f"🪙 `{par_atual}` `{hora_entrada.strftime('%H:%M')}` `{direcao}`\n\n"
                f"⏰ **Termina às:** `{hora_fim_op.strftime('%H:%M')}`\n"
                f"⚡️ **1º GALE TERMINA ÀS** `{hora_gale1.strftime('%H:%M')}`\n"
                f"⚡️ **2º GALE TERMINA ÀS** `{hora_gale2.strftime('%H:%M')}`\n"
                f"📱 **Prepare-se para entrar na corretora!**"
            )
            enviar_telegram(msg_sinal)
            
            aguardar_ate(hora_fim_op + timedelta(seconds=5))
            
            sorteio = random.random()
            horario_str = hora_entrada.strftime('%H:%M')
            
            if sorteio < 0.52:
                resultado_texto = f"`{horario_str} {par_atual}` - ✅ **WIN DIRETO**"
                historico_sinais.append((par_atual, horario_str, "WIN"))
            else:
                aguardar_ate(hora_gale1 + timedelta(seconds=5))
                if random.random() < 0.68:
                    resultado_texto = f"`{horario_str} {par_atual}` - ✅ **WIN NO 1º GALE**"
                    historico_sinais.append((par_atual, horario_str, "WIN"))
                else:
                    aguardar_ate(hora_gale2 + timedelta(seconds=5))
                    if random.random() < 0.58:
                        resultado_texto = f"`{horario_str} {par_atual}` - ✅ **WIN NO 2º GALE**"
                        historico_sinais.append((par_atual, horario_str, "WIN"))
                    else:
                        resultado_texto = f"`{horario_str} {par_atual}` - ❌ **LOSS**"
                        historico_sinais.append((par_atual, horario_str, "LOSS"))
            
            if len(historico_sinais) >= 6:
                vitorias = sum(1 for x in historico_sinais if x[2] == "WIN")
                derrotas = sum(1 for x in historico_sinais if x[2] == "LOSS")
                total_ops = len(historico_sinais)
                assertividade = (vitorias / total_ops) * 100 if total_ops > 0 else 0
                
                bloco_relatorio = "📊 **RELATÓRIO DE OPERAÇÕES** 📊\n\n"
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
            print(f"Erro no ciclo: {e}")
            time.sleep(5)

if __name__ == "__main__":
    iniciar_robo()
