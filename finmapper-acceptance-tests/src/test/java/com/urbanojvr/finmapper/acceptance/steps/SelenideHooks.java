package com.urbanojvr.finmapper.acceptance.steps;

import com.codeborne.selenide.Configuration;
import io.cucumber.java.Before;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.server.context.WebServerApplicationContext;

/**
 * Hook de Cucumber. No usar {@code @Bean} aquí: acceder al {@code WebServer} durante el refresh
 * del contexto provoca un segundo conector Tomcat (8080 + puerto efímero) en Spring Boot 4.
 */
public class SelenideHooks {

    @Autowired
    private WebServerApplicationContext applicationContext;

    @Before
    public void configureSelenide() {
        int port = applicationContext.getWebServer().getPort();
        Configuration.browser = "chrome";
        Configuration.headless = true;
        Configuration.baseUrl = "http://127.0.0.1:" + port;
    }
}
