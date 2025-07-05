class TestEmptyDashboard():

    def test_given_no_transactions_then_show_empty_dashboard_page(self, client):
        response = client.get('/dashboard', follow_redirects=True)

        assert "NO HAY DATOS. INTRODUCE TRANSACCIONES Y CATEGORÍAS" in response.data.decode('utf-8')
