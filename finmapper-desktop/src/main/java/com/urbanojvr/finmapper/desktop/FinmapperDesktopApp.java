package com.urbanojvr.finmapper.desktop;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.web.WebView;
import javafx.stage.Stage;
import org.springframework.context.ConfigurableApplicationContext;

/**
 * Contenedor JavaFX con WebView; carga la app Spring servida por el embebido Tomcat local.
 */
public class FinmapperDesktopApp extends Application {

    private static ConfigurableApplicationContext springContext;
    private static String startUrl;

    /**
     * Debe llamarse antes de {@link Application#launch(Class, String...)} porque launch instancia
     * esta clase por reflexión.
     */
    public static void bootstrap(ConfigurableApplicationContext context, String url) {
        springContext = context;
        startUrl = url;
    }

    @Override
    public void start(Stage stage) {
        if (springContext == null || startUrl == null) {
            throw new IllegalStateException("Llama primero a FinmapperDesktopApp.bootstrap()");
        }

        WebView webView = new WebView();
        webView.getEngine().load(startUrl);

        Scene scene = new Scene(webView, 1200, 800);
        stage.setTitle("Finmapper");
        stage.setScene(scene);
        stage.show();
    }

    @Override
    public void stop() throws Exception {
        if (springContext != null && springContext.isActive()) {
            springContext.close();
        }
        springContext = null;
        super.stop();
    }
}
