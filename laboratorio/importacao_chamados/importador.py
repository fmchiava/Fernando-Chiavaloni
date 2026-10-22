import csv
import io
from datetime import date


def importar_csv(texto, existentes=None):
    linhas = csv.DictReader(io.StringIO(texto))
    colunas = linhas.fieldnames or []
    if len(colunas) != len(set(colunas)):
        raise ValueError("cabecalho com coluna duplicada")
    obrigatorias = {"id_externo", "data", "categoria", "descricao", "status"}
    ausentes = obrigatorias - set(colunas)
    if ausentes:
        raise ValueError(f"cabecalho sem colunas: {', '.join(sorted(ausentes))}")
    resultado = dict(existentes or {})
    for numero, linha in enumerate(linhas, start=2):
        if None in linha:
            raise ValueError(f"linha {numero}: colunas extras")
        if not (linha["id_externo"] or "").strip():
            raise ValueError(f"linha {numero}: id_externo obrigatorio")
        if not (linha["descricao"] or "").strip():
            raise ValueError(f"linha {numero}: descricao obrigatoria")
        if linha["categoria"] not in {"acesso", "erro", "duvida"}:
            raise ValueError(f"linha {numero}: categoria desconhecida")
        if linha["status"] != "aberto":
            raise ValueError(f"linha {numero}: status inicial deve ser aberto")
        try:
            data_valida = date.fromisoformat(linha["data"])
        except (TypeError, ValueError) as erro:
            raise ValueError(f"linha {numero}: data invalida") from erro
        if data_valida.isoformat() != linha["data"]:
            raise ValueError(f"linha {numero}: data deve estar em AAAA-MM-DD")
        chave = (linha["id_externo"], linha["data"])
        if chave in resultado and resultado[chave] != linha:
            raise ValueError(f"linha {numero}: conflito com chamado existente")
        resultado[chave] = linha
    return resultado
