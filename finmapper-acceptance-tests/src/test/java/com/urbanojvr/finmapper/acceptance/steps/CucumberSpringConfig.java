package com.urbanojvr.finmapper.acceptance.steps;

import com.urbanojvr.finmapper.FinmapperAppApplication;
import io.cucumber.spring.CucumberContextConfiguration;
import org.springframework.boot.test.context.SpringBootTest;

@CucumberContextConfiguration
@SpringBootTest(
        classes = FinmapperAppApplication.class,
        webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT,
        properties = {
                "server.address=127.0.0.1",
                "server.port=0"
        }
)
public class CucumberSpringConfig {
}
