class TestEmptyDashboard():

    def test_given_no_transactions_then_show_empty_dashboard_page(self, client):
        response = client.get('/dashboard', follow_redirects=True)

        # Check that the empty dashboard message is shown
        assert "No hay datos para este año" in response.data.decode('utf-8'), "Should show empty dashboard message"
        
        # Check that quick actions are present
        assert "Acciones Rápidas" in response.data.decode('utf-8'), "Should show quick actions section"
        
        # Check that year selector is shown
        assert "Resumen financiero del año" in response.data.decode('utf-8'), "Should show year header"
