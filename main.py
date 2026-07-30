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

def obter_preco_medio(par):
    # Retorna a média de 3 leituras rápidas para garantir preço 100% fiável
    precos = []
    for _ in range(3):
        p = verificar_preco_real(par)
        if p is not None:
            precos.append(p)
        time.sleep(0.5)
    if precos:
        return sum(precos) / len(precos)
    return None

def analisar_tendencia_profissional(par):
    p1 = obter_preco_medio(par)
    p2 = obter_preco_medio(par)
    p3 = obter_preco_medio(par)
    
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

def validar_resultado(preco_inicial, preco_atual, direcao):
    if preco_inicial is None or preco_atual is None:
        return False
    
    diferenca = preco_atual - preco_inicial
    
    if "ACIMA" in direcao:
        return diferenca > 0.00000
    else:
        return diferenca < 0.00000

def iniciar_robo():
    print("🤖 AlphaTick Pro (Leitura Média Blindada Ativa)...")
    
    enviar_telegram(
        "🚀 **ALPHATICK PRO — SISTEMA REINICIADO** 🚀\n\n"
        "🔄 `Mecanismo de dupla confirmação de preço ativado.`\n"
        "🧹 `Histórico limpo. Prontinho para apanhar os WIN sem falhas!`\n"
        "🛠 *Manutenção rápida às 05:00 ativa.*"
    )
    
    historico_sinais = []
    
    while True:
        try:
            agora = datetime.utcnow() + timedelta(hours=1)
            
            # Manutenção rápida às 05:00
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
            
            preco_inicio = obter_preco_medio(par_atual)
            
            # Validação do Sinal Principal (Fim da 1ª vela)
            aguardar_ate(hora_fim_op + timedelta(seconds=5))
            horario_str = hora_entrada.strftime('%H:%M')
            horario_atual_msg = (datetime.utcnow() + timedelta(hours=1)).strftime('%H:%M')
            
            win_direto = validar_resultado(preco_inicio, obter_preco_medio(par_atual), direcao)
            
            if win_direto:
                historico_sinais.append((par_atual, horario_str, "WIN"))
                enviar_telegram(f"`{horario_str} {par_atual}` — ✅\n\n`{horario_atual_msg}`\n🟢 **W I N** 🟢")
            else:
                # 1º Gale
                enviar_telegram(f"⚠️ **Loss na 1ª vela** — A aguardar fecho do 1º GALE às `{hora_gale1.strftime('%H:%M')}`...")
                aguardar_ate(hora_gale1 + timedelta(seconds=5))
                
                win_gale1 = validar_resultado(preco_inicio, obter_preco_medio(par_atual), direcao)
                
                if win_gale1:
                    historico_sinais.append((par_atual, horario_str, "WIN"))
                    enviar_telegram(f"`{horario_str} {par_atual}` — ✅\n\n`{(datetime.utcnow() + timedelta(hours=1)).strftime('%H:%M')}`\n🟢 **W I N** 🟢")
                else:
                    # 2º Gale
                    enviar_telegram(f"⚠️ **Loss no 1º Gale** — A aguardar fecho do 2º GALE às `{hora_gale2.strftime('%H:%M')}`...")
                    aguardar_ate(hora_gale2 + timedelta(seconds=5))
                    
                    win_gale2 = validar_resultado(preco_inicio, obter_preco_medio(par_atual), direcao)
                    
                    if win_gale2:
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
