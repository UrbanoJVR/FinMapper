package com.urbanojvr.finmapper.acceptance.steps;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;

import static com.codeborne.selenide.Condition.text;
import static com.codeborne.selenide.Selenide.$;
import static com.codeborne.selenide.Selenide.open;

public class HomeSteps {

    @Given("abro la home")
    public void abroLaHome() {
        open("/");
    }

    @Then("veo el mensaje de bienvenida")
    public void veoElMensaje() {
        $("#welcome").shouldHave(text("Bienvenido a Finmapper"));
    }
}
