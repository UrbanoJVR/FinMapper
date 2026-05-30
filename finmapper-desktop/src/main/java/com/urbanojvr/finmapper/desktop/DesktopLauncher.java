package com.urbanojvr.finmapper.desktop;

import com.urbanojvr.finmapper.FinmapperAppApplication;
import javafx.application.Application;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.server.context.WebServerApplicationContext;
import org.springframework.context.ConfigurableApplicationContext;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Optional;

/**
 * Punto de entrada del escritorio: arranca Spring primero (forma clásica) y luego JavaFX.
 */
public final class DesktopLauncher {

    private DesktopLauncher() {
    }

    public static void main(String[] args) {
        System.setProperty("java.awt.headless", "false");
        // Puerto efímero explícito: evita el default 8080 de Spring Boot en desarrollo web standalone.
        var mergedArgs = new ArrayList<String>();
        mergedArgs.add("--server.port=0");
        mergedArgs.add("--server.address=127.0.0.1");
        mergedArgs.addAll(Arrays.asList(args));

        ConfigurableApplicationContext ctx = new SpringApplicationBuilder(FinmapperAppApplication.class)
                .headless(false)
                .run(mergedArgs.toArray(String[]::new));
        final var webServer = Optional
                .ofNullable(((WebServerApplicationContext) ctx).getWebServer())
                .orElseThrow(() -> new IllegalStateException("No WebServer configured"));

        final int port = webServer.getPort();
        String startUrl = "http://127.0.0.1:" + port + "/";
        FinmapperDesktopApp.bootstrap(ctx, startUrl);
        Application.launch(FinmapperDesktopApp.class, args);
    }
}
