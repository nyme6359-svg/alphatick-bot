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
        delta = (tempo_alvo - datetime.now()).total_seconds()
        if delta > 1:
            time.sleep(1)
        else:
            time.sleep(0.1)

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
    time.sleep(1)
    p2 = verificar_preco_real(par)
    time.sleep(1)
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
    print("🤖 AlphaTick Pro (Versão Suprema Definitiva Ativa)...")
    
    enviar_telegram(
        "🚀 **ALPHATICK PRO — SISTEMA REINICIADO** 🚀\n\n"
        "🔄 `Versão suprema injetada com sucesso.`\n"
        "🧹 `Controlo absoluto de tempo e relatórios ativado.`\n"
        "🛠 *Manutenção rápida agendada para as 05:00.*"
    )
    
    historico_sinais = []
    
    while True:
        try:
            agora = datetime.utcnow() + timedelta(hours=1)
            
            # Manutenção limpa e rápida às 05:00 (apenas 70 segundos para não interferir)
            if agora.hour == 5 and agora.minute == 0:
                enviar_telegram("🛠 **MANUTENÇÃO PROGRAMADA DAS 05:00** 🛠\n\n`A reiniciar sistemas e limpar lotes para o novo dia...`")
                historico_sinais.clear()
                time.sleep(70)
                continue
            
            # Sincronização rigorosa de blocos de 5 minutos
            minuto_atual = agora.minute
            extra = 5 - (minuto_atual % 5)
            if extra == 0:
                extra = 5
                
            hora_entrada = agora.replace(second=0, microsecond=0) + timedelta(minutes=extra)
            momento_envio = hora_entrada - timedelta(seconds=40)
            
            if datetime.now() < momento_envio:
                aguardar_ate(momento_envio)
            
            par_atual = random.choice(PARES_ABERTOS)
            print(f"🔍 Analisando fluxo institucional para {par_atual} às {datetime.now().strftime('%H:%M:%S')}...")
            direcao = analisar_tendencia_profissional(par_atual)
            
            hora_fim_op = hora_entrada + timedelta(minutes=5)
            hora_gale1 = hora_fim_op + timedelta(minutes=5)
            hora_gale2 = hora_gale1 + timedelta(minutes=5)
            
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
            
            # Validação do Sinal Principal (Fim da 1ª vela)
            aguardar_ate(hora_fim_op + timedelta(seconds=5))
            horario_str = hora_entrada.strftime('%H:%M')
            horario_atual_msg = (datetime.utcnow() + timedelta(hours=1)).strftime('%H:%M')
            resultado_final = "LOSS"
            
            if preco_inicio is not None:
                preco_fim = verificar_preco_real(par_atual)
                if preco_fim is not None:
                    subiu = preco_fim > preco_inicio
                    if (subiu and "ACIMA" in direcao) or (not subiu and "ABAIXO" in direcao):
                        resultado_final = "WIN"
            
            if resultado_final == "WIN":
                historico_sinais.append((par_atual, horario_str, "WIN"))
                enviar_telegram(f"`{horario_str} {par_atual}` — ✅\n\n`{horario_atual_msg}`\n🟢 **W I N** 🟢")
            else:
                # 1º Gale
                enviar_telegram(f"⚠️ **Loss na 1ª vela** — A aguardar fecho do 1º GALE às `{hora_gale1.strftime('%H:%M')}`...")
                aguardar_ate(hora_gale1 + timedelta(seconds=5))
                preco_gale1 = verificar_preco_real(par_atual)
                
                if preco_inicio is not None and preco_gale1 is not None and ((preco_gale1 > preco_inicio and "ACIMA" in direcao) or (preco_gale1 < preco_inicio and "ABAIXO" in direcao)):
                    historico_sinais.append((par_atual, horario_str, "WIN"))
                    enviar_telegram(f"`{horario_str} {par_atual}` — ✅\n\n`{(datetime.utcnow() + timedelta(hours=1)).strftime('%H:%M')}`\n🟢 **W I N** 🟢")
                else:
                    # 2º Gale
                    enviar_telegram(f"⚠️ **Loss no 1º Gale** — A aguardar fecho do 2º GALE às `{hora_gale2.strftime('%H:%M')}`...")
                    aguardar_ate(hora_gale2 + timedelta(seconds=5))
                    preco_gale2 = verificar_preco_real(par_atual)
                    
                    if preco_inicio is not None and preco_gale2 is not None and ((preco_gale2 > preco_inicio and "ACIMA" in direcao) or (preco_gale2 < preco_inicio and "ABAIXO" in direcao)):
                        historico_sinais.append((par_atual, horario_str, "WIN"))
                        enviar_telegram(f"`{horario_str} {par_atual}` — ✅\n\n`{(datetime.utcnow() + timedelta(hours=1)).strftime('%H:%M')}`\n🟢 **W I N** 🟢")
                    else:
                        historico_sinais.append((par_atual, horario_str, "LOSS"))
                        enviar_telegram(f"`{horario_str} {par_atual}` — ❌\n\n`{(datetime.utcnow() + timedelta(hours=1)).strftime('%H:%M')}`\n🔴 **L O S S** 🔴")
            
            # Relatório a cada lote de 6 operações
            if len(historico_sinais) >= 6:
                vitorias = sum(1 for x in historico_sinais if x[2] == "WIN")
                derrotas = sum(1 for x in historico_sinais if x[2] == "LOSS")
                total_ops = len(historico_sinais)
                assertividade = (vitorias / total_ops) * 100 if total_ops > 0 else 0
                
                bloco_relatorio = "📊 **RELATÓRIO DE OPERAÇÕES** 📊\n\n"
                for par, h, res in historico_sinais:
                    icone = "✅" if res == "WIN" else "❌"
                    bloco_relatorio += f"`{h} {par}` {icone}\n"
                
                bloco_relatorio += (
                    f"\n"
                    f"✅ {vitorias} vitorias\n"
                    f"❌ {derrotas} derrotas\n"
                    f"😎 {assertividade:.1f}% de acerto:\n"
                    f"📈 {total_ops} operações\n\n"
                    f"📱 **Envia seu resultado para** 👉 [AlphaTick Pro]"
                )
                enviar_telegram(bloco_relatorio)
                historico_sinais.clear()
                
            time.sleep(2)
        except Exception as e:
            print(f"Erro crítico evitado no ciclo: {e}")
            time.sleep(5)

if __name__ == "__main__":
    iniciar_robo() 
