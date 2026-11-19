import unittest
from calculadora_energia import calcular, PremissasEnergia

class TestCalculadoraEnergia(unittest.TestCase):
    def test_cenario_base(self):
        r = calcular()
        self.assertAlmostEqual(r['cenario_base']['consumo_kwh_mes'], 179.7)
        self.assertAlmostEqual(r['cenario_base']['custo_rs_mes'], 170.715)

    def test_eficiencia(self):
        r = calcular()
        self.assertAlmostEqual(r['eficiencia']['economia_kwh_mes'], 26.955)
        self.assertGreater(r['eficiencia']['retorno_simples_meses'], 0)

    def test_solar_limitada_ao_consumo(self):
        p = PremissasEnergia(consumo_mensal_kwh=100, potencia_solar_kwp=5)
        r = calcular(p)
        self.assertLessEqual(r['solar']['energia_aproveitada_estimada_kwh_mes'], 100)

    def test_tarifa_invalida(self):
        with self.assertRaises(ValueError):
            calcular(PremissasEnergia(tarifa_efetiva_rs_kwh=0))

if __name__ == '__main__':
    unittest.main()
