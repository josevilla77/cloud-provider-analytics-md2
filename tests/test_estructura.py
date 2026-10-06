import unittest
from pathlib import Path


class TestEstructuraRepositorio(unittest.TestCase):
    def test_archivos_minimos(self):
        raiz = Path(__file__).resolve().parents[1]
        esperados = [
            "README.md",
            "DECISIONS.md",
            "requirements.txt",
            "config/config.example.yaml",
            "data/README.md",
            "docs/arquitectura.md",
            "docs/matriz_requisitos.md",
            "evidence/resumen_exploracion.csv",
            "src/exploracion_inicial.py",
        ]
        faltantes = [ruta for ruta in esperados if not (raiz / ruta).exists()]
        self.assertEqual([], faltantes, f"Faltan archivos: {faltantes}")


if __name__ == "__main__":
    unittest.main()

