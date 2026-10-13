"""Testes do assistente: a chave vem do ambiente e a resposta do modelo é só texto."""
import io
import os
import unittest
from unittest import mock

import assistente


class AssistenteTest(unittest.TestCase):
    def test_chave_vem_do_ambiente(self):
        with mock.patch.dict(os.environ, {"ASSISTENTE_API_KEY": "valor-de-teste"}):
            self.assertEqual(assistente.chave(), "valor-de-teste")

    def test_sem_chave_recusa_perguntar(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit):
                assistente.perguntar("oi")

    def test_pergunta_vai_inteira_e_a_resposta_e_so_impressa(self):
        saida = io.StringIO()
        with mock.patch.object(assistente, "perguntar", return_value="resposta") as perguntar:
            with mock.patch("sys.argv", ["assistente.py", "qual", "a", "hora"]), mock.patch("sys.stdout", saida):
                assistente.main()
        perguntar.assert_called_once_with("qual a hora")
        self.assertEqual(saida.getvalue(), "resposta\n")

    def test_sem_argumentos_usa_a_pergunta_padrao(self):
        with mock.patch.object(assistente, "perguntar", return_value="oi") as perguntar:
            with mock.patch("sys.argv", ["assistente.py"]), mock.patch("sys.stdout", io.StringIO()):
                assistente.main()
        perguntar.assert_called_once_with("Olá! O que você sabe fazer?")


if __name__ == "__main__":
    unittest.main()
