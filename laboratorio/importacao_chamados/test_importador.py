import unittest

from importador import importar_csv


class ImportacaoChamadosTest(unittest.TestCase):
    def test_linha_valida_preserva_campos_e_abre_chamado(self):
        csv_texto = (
            "id_externo,data,categoria,descricao,status\n"
            "T-100,2026-10-21,erro,Falha ao entrar,aberto\n"
        )

        chamados = importar_csv(csv_texto)

        self.assertEqual(
            {
                ("T-100", "2026-10-21"): {
                    "id_externo": "T-100",
                    "data": "2026-10-21",
                    "categoria": "erro",
                    "descricao": "Falha ao entrar",
                    "status": "aberto",
                }
            },
            chamados,
        )

    def test_nova_importacao_preserva_chamados_existentes(self):
        cabecalho = "id_externo,data,categoria,descricao,status\n"
        primeiro = importar_csv(cabecalho + "T-100,2026-10-21,erro,Falha A,aberto\n")

        resultado = importar_csv(
            cabecalho + "T-101,2026-10-21,acesso,Falha B,aberto\n", primeiro
        )

        self.assertEqual(set(resultado), {("T-100", "2026-10-21"), ("T-101", "2026-10-21")})
        self.assertEqual(len(primeiro), 1)

    def test_descricao_vazia_rejeita_linha_sem_alterar_existentes(self):
        cabecalho = "id_externo,data,categoria,descricao,status\n"
        existentes = importar_csv(cabecalho + "T-100,2026-10-21,erro,Falha A,aberto\n")
        antes = dict(existentes)

        with self.assertRaisesRegex(ValueError, "linha 2.*descricao"):
            importar_csv(cabecalho + "T-101,2026-10-21,erro,,aberto\n", existentes)

        self.assertEqual(existentes, antes)

    def test_categoria_desconhecida_nao_e_convertida_silenciosamente(self):
        csv_texto = (
            "id_externo,data,categoria,descricao,status\n"
            "T-102,2026-10-21,financeiro,Outro problema,aberto\n"
        )

        with self.assertRaisesRegex(ValueError, "linha 2.*categoria"):
            importar_csv(csv_texto)

    def test_mesma_chave_com_conteudo_diferente_exige_revisao(self):
        cabecalho = "id_externo,data,categoria,descricao,status\n"
        existentes = importar_csv(cabecalho + "T-100,2026-10-21,erro,Falha A,aberto\n")

        with self.assertRaisesRegex(ValueError, "linha 2.*conflito"):
            importar_csv(cabecalho + "T-100,2026-10-21,erro,Falha B,aberto\n", existentes)

        self.assertEqual(existentes[("T-100", "2026-10-21")]["descricao"], "Falha A")

    def test_data_invalida_nao_entra_na_base(self):
        csv_texto = (
            "id_externo,data,categoria,descricao,status\n"
            "T-103,2026-02-30,erro,Falha A,aberto\n"
        )

        with self.assertRaisesRegex(ValueError, "linha 2.*data"):
            importar_csv(csv_texto)

    def test_status_inicial_diferente_de_aberto_e_rejeitado(self):
        csv_texto = (
            "id_externo,data,categoria,descricao,status\n"
            "T-104,2026-10-21,erro,Falha A,fechado\n"
        )

        with self.assertRaisesRegex(ValueError, "linha 2.*status"):
            importar_csv(csv_texto)

    def test_identificador_vazio_nao_e_aceito(self):
        csv_texto = (
            "id_externo,data,categoria,descricao,status\n"
            ",2026-10-21,erro,Falha A,aberto\n"
        )

        with self.assertRaisesRegex(ValueError, "linha 2.*id_externo"):
            importar_csv(csv_texto)

    def test_cabecalho_incompleto_tem_erro_legivel(self):
        csv_texto = "id_externo,data,categoria,status\nT-105,2026-10-21,erro,aberto\n"

        with self.assertRaisesRegex(ValueError, "cabecalho.*descricao"):
            importar_csv(csv_texto)

    def test_cabecalho_duplicado_nao_oculta_uma_coluna(self):
        csv_texto = (
            "id_externo,data,categoria,descricao,status,descricao\n"
            "T-105,2026-10-21,erro,Falha real,aberto,Outra descricao\n"
        )

        with self.assertRaisesRegex(ValueError, "cabecalho.*duplicada"):
            importar_csv(csv_texto)

    def test_reimportacao_igual_e_idempotente(self):
        csv_texto = (
            "id_externo,data,categoria,descricao,status\n"
            "T-100,2026-10-21,erro,Falha A,aberto\n"
        )

        primeira = importar_csv(csv_texto)
        segunda = importar_csv(csv_texto, primeira)

        self.assertEqual(len(segunda), 1)
        self.assertEqual(segunda, primeira)

    def test_mesmo_id_em_outra_data_e_outra_ocorrencia(self):
        csv_texto = (
            "id_externo,data,categoria,descricao,status\n"
            "T-100,2026-10-21,erro,Falha A,aberto\n"
            "T-100,2026-10-22,erro,Falha A,aberto\n"
        )

        chamados = importar_csv(csv_texto)

        self.assertEqual(set(chamados), {("T-100", "2026-10-21"), ("T-100", "2026-10-22")})

    def test_lote_misto_nao_altera_base_quando_uma_linha_falha(self):
        cabecalho = "id_externo,data,categoria,descricao,status\n"
        existentes = importar_csv(cabecalho + "T-100,2026-10-21,erro,Falha A,aberto\n")
        lote = (
            cabecalho
            + "T-101,2026-10-21,acesso,Falha B,aberto\n"
            + "T-102,2026-10-21,financeiro,Falha C,aberto\n"
        )

        with self.assertRaisesRegex(ValueError, "linha 3.*categoria"):
            importar_csv(lote, existentes)

        self.assertEqual(set(existentes), {("T-100", "2026-10-21")})

    def test_linha_truncada_retorna_erro_de_campo(self):
        csv_texto = (
            "id_externo,data,categoria,descricao,status\n"
            "T-106,2026-10-21,erro\n"
        )

        with self.assertRaisesRegex(ValueError, "linha 2.*descricao"):
            importar_csv(csv_texto)

    def test_coluna_extra_retorna_erro_em_vez_de_ignorar_dados(self):
        csv_texto = (
            "id_externo,data,categoria,descricao,status\n"
            "T-107,2026-10-21,erro,Falha A,aberto,dado inesperado\n"
        )

        with self.assertRaisesRegex(ValueError, "linha 2.*colunas extras"):
            importar_csv(csv_texto)


if __name__ == "__main__":
    unittest.main()
